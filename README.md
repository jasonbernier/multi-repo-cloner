# Multi-Repo Cloner
# Written by Jason Bernier
# https://github.com/jasonbernier

This Python script enables the cloning of multiple Git repositories listed in a text file. It is designed to simplify the process of setting up an environment where multiple repositories need to be cloned simultaneously.

## Features

- **Bulk Cloning**: Clone multiple repositories with a single command.
- **Real-time Progress**: Outputs real-time progress for each repository being cloned.
- **Error Handling**: Provides detailed error messages if cloning fails.

## Requirements

- **Python**: Python 3.6 or newer.
- **Git**: Git must be installed and accessible from the command line.

## Installation

Clone this repository to your local machine using Git:

```bash
git clone https://github.com/jasonbernier/multi-repo-cloner.git
```

Navigate to the script directory:

```bash
cd multi-repo-cloner
```

## Usage

1. **Prepare the List File**:
   Create a text file containing the URLs of the Git repositories you wish to clone, one URL per line. For example:

   ```
   https://github.com/user/repo1.git
   https://github.com/user/repo2.git
   ```

2. **Run the Script**:
   Execute the script by providing the path to your list file using the `-l` option:

   ```bash
   python clone_repos.py -l path/to/your/list.txt
   ```

   Replace `path/to/your/list.txt` with the actual path to your list file.

## Common Issues

- **File Not Found**: Ensure the path to the list file is correct.
- **Permission Denied**: Make sure you have the necessary permissions to clone the repositories.
- **Invalid Repository URL**: Verify that all URLs in your list file are correct and accessible.

## Contributing

Contributions to improve the script are welcome. Please feel free to fork the repository, make changes, and submit a pull request.


