# Git Repo Migrater

A tool to transfer Git repositories from one server to another.

## Features:
- migrate multiple Git repositories between servers

## Installation:
1. Clone this repository.
2. Make sure Python 3 is installed.

## Usage:
```bash
python main.py --source SOURCE --target TARGET --repos REPO1,REPO2,...
```

### Options:
- `-s`, `--source`: Source git server URL (required)
- `-t`, `--target`: Target git server URL (required)
- `-r`, `--repos`: List of repositories to migrate. Can be comma-separated or multiple arguments.

### Examples:
1. (Not yet implemented) Migrate a single repository:
```bash
python main.py --filename repos.txt --source https://old.server.com --target https://new.server.com --repos repo1
```

2. (Not yet implemented) Migrate multiple repositories from file:
```bash
python main.py --filename repos.txt --source https://old.server.com --target https://new.server.com
```
