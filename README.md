# Git Repository Migration Tool

A tool for migrating Git repositories from one server to another.

## Features

- Migrate multiple Git repositories between servers
- Support for both HTTPS and SSH protocols
- Ability to specify repositories directly or read from a file
- Handles all branches and tags during migration
- Command-line interface for easy use

## Installation

1. Clone this repository:


git clone https://github.com/celsuss/git-repo-migration-tool.git


2. Navigate to the project directory:


cd git-repo-migration-tool


3. Ensure Python 3.6+ is installed on your system.

4. Install required dependencies:


pip install -r requirements.txt



## Usage

Basic usage:

```bash
python main.py -s SOURCE -t TARGET -r REPOS --source-group SOURCE_GROUP --target-group TARGET_GROUP [--ssh]


Options:

 • -s, --source: Source git server URL (required)
 • -t, --target: Target git server URL (required)
 • -r, --repos: List of repositories to migrate or path to a .txt file containing repository names (required)
 • --source-group: Group which the repo belongs to in the source (required)
 • --target-group: Group which the repo belongs to in the target (required)
 • --ssh: Use SSH for git operations instead of HTTPS (optional)

Examples:

 1 Migrate a single repository:

   python main.py -s old.server.com -t new.server.com -r repo1 --source-group oldgroup --target-group newgroup

 2 Migrate multiple repositories:

   python main.py -s old.server.com -t new.server.com -r repo1,repo2,repo3 --source-group oldgroup --target-group newgroup

 3 Migrate repositories listed in a file using SSH:

   python main.py -s old.server.com -t new.server.com -r repos.txt --source-group oldgroup --target-group newgroup --ssh



Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


License

This project is licensed under the MIT License - see the LICENSE file for details.
