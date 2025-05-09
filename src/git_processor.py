# src/git_processor.py
from git import Repo, Commit, Actor
import config
from neo4j_driver import Neo4jDriver

def merge_parents(db, commit):
    for parent in commit.parents:
        db.process_commit(db, parent)
    

def process_commit(db: Neo4jDriver, commit: Commit):

    # if len(commit.parents) > 0:
    #     # breakpoint()
    #     for parent in commit.parents:
    #         print('parent processing')
    #         process_commit(db, parent)

    # Create the humans
    committer = commit.committer
    author = commit.author
    co_authors = list(commit.co_authors)

    committer_node = db.merge_actor(committer)
    author_node = db.merge_actor(author)
    co_author_nodes = list()
    for co_author in co_authors:
        # breakpoint()

        co_author_nodes.extend(db.merge_actor(co_author))

    db.merge_commit_step(commit, committer_node, author_node, co_author_nodes)
    # print(f"commit {commit.hexsha}")

def process_git_data():
    repo = Repo(config.LOCAL_REPO_PATH)
    db = Neo4jDriver()
    status_flag = db.get_import_status()
    print("Import Process Status Result:", status_flag)
    # db.clear_database()


    if not status_flag['git_import_complete']:
        commits = find_commits_in_repo(repo)
        print("Performing initial data import...")
        initial_process_commits_into_db(db, commits)
        db.merge_get_import_status_node()
    else:
        print("Skipping initial data import.")
        # TODO: try for file details import
    return


def find_commits_in_repo(repo):
    commits = list(repo.iter_commits())
    # Start with the first commit ever
    commits.reverse()
    return commits

def initial_process_commits_into_db(db: Neo4jDriver, commits):

    for commit in commits:
        process_commit(db, commit)
    print(f"Processed {len(commits)} commits into Neo4j.")
    
    db.close()

if __name__ == "__main__":
    process_git_data()