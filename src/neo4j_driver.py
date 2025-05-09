# src/neo4j_driver.py
from neo4j import GraphDatabase, Record
from commit_details import CommitDetails
import config
import time
import json
from git import Repo, Commit, Actor


class Neo4jDriver:
    def __init__(self, max_retries=5, retry_delay=2):
        self.driver = None
        for attempt in range(max_retries):
            try:
                self.driver = GraphDatabase.driver(
                    config.NEO4J_URI,
                    auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
                )
                self.driver.verify_connectivity()  # Ensure connection works
                print("Connected to Neo4j successfully.")
                break
            except Exception as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    raise Exception("Failed to connect to Neo4j after retries.")

    def close(self):
        if self.driver:
            self.driver.close()

    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Database cleared.")

    def create_node(self, label, properties):
        with self.driver.session() as session:
            query = f"MERGE (n:{label} $props) RETURN n"
            result = session.run(query, props=properties)
            return result.single()["n"]
    
    def tx_insert_actor(tx, actor) -> str:
        result = tx.run("""
            MERGE (a: Actor {name: $name, email: $email})
            RETURN a.email as email
            """,
            name=actor.name,
            email=actor.email
        )
        return result.single()["email"]

    def merge_actor(self, actor: Actor) -> Actor:
        with self.driver.session() as session:
            query = """
            MERGE (a:Actor {name: $name, email: $email})
            RETURN elementId(a)
            """
            result = session.run(query, name=actor.name, email=actor.email)
            return result.single()["elementId(a)"]


        
    def merge_actor_node(self, properties) -> Record:
        with self.driver.session() as session:
            query = "MERGE (n:Actor {name: $props.name, email: $props.email}) RETURN n"
            result = session.run(query, props=properties)
            print(f"merge actor ${properties.name}")
            return result.single()
        
    def add_commit(self, author_props, commit_props):
        # breakpoint()
        self.driver.execute_query(
            "MERGE (a:Actor {name: $author.name, email: $author.email}) "
            "MERGE (c:Commit {hexsha: $commit.hexsha}) "
            "MERGE (a)-[:AUTHORED]->(c) "
            "return a.email as email",
            author=author_props, commit=commit_props
        )

    def merge_commit_step(self, commit: Commit, committer_node: str, author_node: str, co_author_nodes: list[str]):
        # print('commit merge processing')
        commit_details = CommitDetails(commit)
        self.driver.execute_query(
            "match (committer), (author)"
            "where elementId(author) = $author_id "
            "and elementId(committer) = $committer_id "
            "MERGE (c:Commit {commit_hash: $commit_hash}) "
            "ON CREATE SET c.parent_shas = $parent_shas, "
            " c.message = $message, "
            " c.summary = $summary "
            "MERGE (committer)-[cr:COMMITTED]->(c) "
            "ON CREATE SET cr.committed_date = $committed_date "
            "MERGE (author)-[ca:AUTHORED]->(c) "
            "ON CREATE SET ca.authored_date = $authored_date "
            , committer_id=committer_node,
              author_id=author_node,
              commit_hash=commit_details.commit_hash,
              parent_shas=commit_details.parent_shas,
              authored_date=commit_details.authored_date,
              committed_date=commit_details.committed_date,
              message=commit_details.message,
              summary=commit_details.summary,
              )

    def find_commit_and_add_date_details(self, commit):
        # open a driver session
        # find the commit in the db
        # Will `CommitDetails` support us for add date details to the commit?

    def create_relationship(self, from_id, to_id, rel_type):
        with self.driver.session() as session:
            query = """
            MATCH (a), (b)
            WHERE id(a) = $from_id AND id(b) = $to_id
            CREATE (a)-[:%s]->(b)
            """ % rel_type
            session.run(query, from_id=from_id, to_id=to_id)

if __name__ == "__main__":
    db = Neo4jDriver()
    # db.clear_database() # TODO make it clear again

    # Example usage: Process a repository
    repo_path = "downloaded_repo"  # Path to the local repository
    repo = Repo(repo_path)

    for commit in repo.iter_commits():
        db.merge_commit(commit)

    db.close()
