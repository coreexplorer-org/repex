# src/main.py
from download import download_repository
from git_processor import process_git_data

def main():
    print("Starting Git Graph App...")


    # Check if the environment variable is set
    # do_initial_data_import = os.getenv('DO_INITIAL_DATA_IMPORT', '0')  # Default to '0' if not set



    process_git_data()

    print("Initialization complete. Ready for exploration!")

if __name__ == "__main__":
    main()