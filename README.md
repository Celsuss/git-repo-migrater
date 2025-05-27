# Git Repository Migration Tool

A tool for migrating Git repositories from one server to another.

## Features

- Migrate multiple Git repositories between servers
- Support for both HTTPS and SSH protocols
- Ability to specify repositories directly, read from a file, or use a TOML configuration file
- Handles all branches and tags during migration
- Command-line interface for easy use
- Logging functionality for better tracking and debugging

## Installation

1. Clone this repository:

```bash
git clone https://github.com/Celsuss/git-repo-migrater.git
```


2. Navigate to the project directory:


```bash
cd git-repo-migrater
```


3. Ensure Python 3.6+ is installed on your system.
4. Install required dependencies:


```bash
pip install -r requirements.txt
```



Usage

There are two ways to use this tool:

1. Using command-line arguments:


```bash
python app/main.py -s SOURCE -t TARGET -r REPOS --source-group SOURCE_GROUP --target-group TARGET_GROUP [--ssh]
```


Options:

 • -s, --source: Source git server URL (required)<br>
 • -t, --target: Target git server URL (required)<br>
 • -r, --repos: List of repositories to migrate or path to a .txt file containing repository names (required)<br>
 • --source-group: Group which the repo belongs to in the source (required)<br>
 • --target-group: Group which the repo belongs to in the target (required)<br>
 • --ssh: Use SSH for git operations instead of HTTPS (optional)<br>

2. Using a TOML configuration file:


```bash
python app/main.py -c CONFIG_FILE
```


Options:

 • -c, --config: Path to TOML configuration file


Configuration File

You can use a TOML configuration file to specify the migration settings. Here's an example structure:


```toml
[General]
ssh = true

[Source]
source = "source-server.com"
source-group = "source-group"

[Target]
target = "target-server.com"
target-group = "target-group"

[Repos]
reps = ["repo1", "repo2", "repo3"]
```



Examples

1. Migrate a single repository using command-line arguments:


```bash
python app/main.py -s old.server.com -t new.server.com -r repo1 --source-group oldgroup --target-group newgroup
```


2. Migrate multiple repositories using command-line arguments:


```bash
python app/main.py -s old.server.com -t new.server.com -r repo1,repo2,repo3 --source-group oldgroup --target-group newgroup
```


3. Migrate repositories listed in a file using SSH:


```bash
python app/main.py -s old.server.com -t new.server.com -r repos.txt --source-group oldgroup --target-group newgroup --ssh
```


4. Migrate repositories using a TOML configuration file:


```bash
python app/main.py -c repos.toml
```



Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


License

This project is licensed under the MIT License - see the LICENSE file for details.
