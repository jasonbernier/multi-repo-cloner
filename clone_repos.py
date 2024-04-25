# Multi Repo Cloner
# This Python script enables the cloning of multiple Git repositories listed in a text file. It is designed to simplify the process of setting up an environment where multiple repositories need to be cloned simultaneously.
# Written by Jason Bernier

import argparse
import subprocess
import threading
import logging
from time import sleep

# Setup logging to display both to the console and save to a log file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("clone_repos.log"), logging.StreamHandler()])

# Function to clone a repository with retry logic
def clone_repo(repo_url, max_retries):
    retries = 0
    while retries < max_retries:
        try:
            logging.info(f"Attempting to clone {repo_url}, try {retries + 1}...")
            with subprocess.Popen(["git", "clone", repo_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
                for line in proc.stdout:
                    logging.info(line.strip())  # Log output of git command
                _, stderr = proc.communicate()
                if proc.returncode == 0:
                    logging.info(f"Successfully cloned {repo_url}")
                    break
                else:
                    raise subprocess.CalledProcessError(proc.returncode, 'git clone', output=None, stderr=stderr)
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to clone {repo_url}. Attempt {retries + 1}. Error: {e.stderr}")
            retries += 1
            if retries < max_retries:
                sleep(10)  # Wait for 10 seconds before retrying
            else:
                logging.error(f"Max retries exceeded for {repo_url}")

# Function to manage cloning threads
def handle_cloning(repositories, num_threads, max_retries):
    threads = []
    semaphore = threading.Semaphore(num_threads)  # Control the number of concurrent threads

    for repo_url in repositories:
        semaphore.acquire()
        thread = threading.Thread(target=clone_repo, args=(repo_url, max_retries))
        thread.start()
        threads.append((thread, semaphore))

    for thread, semaphore in threads:
        thread.join()
        semaphore.release()

# Main function to read repository list and manage cloning
def main(repo_list_file, num_threads, max_retries):
    try:
        with open(repo_list_file, 'r') as file:
            repositories = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error(f"Error: The file {repo_list_file} does not exist.")
        return
    except Exception as e:
        logging.error(f"An error occurred while reading the file: {e}")
        return

    if not repositories:
        logging.warning("No repository URLs provided in the file.")
        return
    
    handle_cloning(repositories, num_threads, max_retries)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clone multiple repositories listed in a file with configurable threading and retries.")
    parser.add_argument('-l', '--list', required=True, type=str, help='Path to the file containing repository URLs')
    parser.add_argument('-t', '--threads', type=int, default=4, help='Number of concurrent cloning threads')
    parser.add_argument('-r', '--retries', type=int, default=3, help='Maximum number of retries for each repository')
    args = parser.parse_args()

    main(args.list, args.threads, args.retries)
