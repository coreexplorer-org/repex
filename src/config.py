# config.py
NEO4J_URI = "bolt://localhost:7687"  # Bolt protocol (matches Docker port mapping)
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"  # Matches NEO4J_AUTH in docker-compose.yml
REPO_URL = "https://github.com/bitcoin/bitcoin.git"  # Bitcoin Repo
LOCAL_REPO_PATH = "data/user_supplied_repo"  # Where the repo will be cloned