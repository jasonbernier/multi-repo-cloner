# Multi Repo Cloner
# This Python script enables the cloning of multiple Git repositories listed in a text file. It is designed to simplify the process of setting up an environment where multiple repositories need to be cloned simultaneously.
# Written by Jason Bernier

import argparse
import subprocess
import threading
import logging
import os
from time import sleep

# Setup logging to display both to the console and save to a log file
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("clone_repos.log"), logging.StreamHandler()])

def update_or_clone_repo(repo_url, max_retries, semaphore):
    repo_name = repo_url.split('/')[-1].replace('.git', '')  # Extract the repository name from URL
    try:
        if os.path.exists(repo_name) and os.path.isdir(repo_name):
            logging.info(f"Repository {repo_name} already exists. Checking for updates...")
            try:
                # Attempt to update the existing repository
                os.chdir(repo_name)  # Change directory to the repository
                subprocess.check_call(["git", "fetch", "--all"])
                subprocess.check_call(["git", "reset", "--hard", "origin/master"])
                os.chdir('..')  # Change back to the original directory
                logging.info(f"Repository {repo_name} updated successfully.")
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to update {repo_name}. Error: {e}")
                os.chdir('..')  # Ensure we change back even if an error occurs
        else:
            # Clone the repository if it does not exist
            clone_with_retries(repo_url, max_retries)
    finally:
        semaphore.release()  # Ensure semaphore is released in all cases

def clone_with_retries(repo_url, max_retries):
    retries = 0
    while retries < max_retries:
        try:
            logging.info(f"Attempting to clone {repo_url}, try {retries + 1}...")
            subprocess.check_call(["git", "clone", repo_url])
            logging.info(f"Successfully cloned {repo_url}")
            break
        except subprocess.CalledProcessError:
            logging.error(f"Failed to clone {repo_url}. Attempt {retries + 1}.")
            retries += 1
            if retries < max_retries:
                sleep(10)  # Wait for 10 seconds before retrying
            else:
                logging.error(f"Max retries exceeded for {repo_url}")

def handle_cloning(repositories, num_threads, max_retries):
    threads = []
    semaphore = threading.Semaphore(num_threads)  # Control the number of concurrent threads

    for repo_url in repositories:
        semaphore.acquire()
        thread = threading.Thread(target=update_or_clone_repo, args=(repo_url, max_retries, semaphore))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()  # Wait for all threads to complete

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
    parser = argparse.ArgumentParser(description="Clone or update multiple repositories listed in a file with configurable threading and retries.")
    parser.add_argument('-l', '--list', required=True, type=str, help='Path to the file containing repository URLs')
    parser.add_argument('-t', '--threads', type=int, default=4, help='Number of concurrent cloning threads')
    parser.add_argument('-r', '--retries', type=int, default=3, help='Maximum number of retries for each repository')
    args = parser.parse_args()

    main(args.list, args.threads, args.retries)
