# src/main.py
# from download import download_repository
from git_processor import process_git_data

def main():
    print("Starting Git Graph App...")
    # download_repository()
    process_git_data()
    print("Initialization complete. Ready for exploration!")

if __name__ == "__main__":
    main()