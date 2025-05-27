"""
Git Repository Migration Tool

This script provides functionality to migrate Git repositories from one server
to another. It supports migrating multiple repositories, either specified
directly or read from a file.
The tool can use either HTTPS or SSH for Git operations.

Key features:
- Migrate repositories between different Git servers
- Support for both HTTPS and SSH protocols
- Ability to specify multiple repositories or read from a file
- Handling of all branches and tags during migration
- Command-line interface for easy use

Usage:
    python script_name.py -s SOURCE -t TARGET -r REPOS --source-group SOURCE_GROUP --target-group TARGET_GROUP [--ssh]

For detailed usage instructions, use the --help flag.

This script requires the following external libraries:
- argparse
- logging
- subprocess
- sys

Author: Jens Lordén
Date: [2025-05-27]
Version: 1.0
"""
import argparse
import logging
import shutil
import subprocess
import sys

import toml

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ConfigurationError(Exception):
    """Custom exception for configuration errors."""

    pass


def cleanup_repositories(repos):
    for path in repos:
        if delete_local_repo(path):
            logger.info(f"Cleaned up repository: {path}")
        else:
            logger.warning(f"Failed to clean up repository: {path}")


def delete_local_repo(repo_dir: str) -> bool:
    """
    Delete the local repository directory.

    Args:
    repo_dir (str): The directory of the repository to delete.

    Returns:
    bool: True if deletion was successful, False otherwise.
    """
    try:
        shutil.rmtree(repo_dir)
        logger.info(f"Deleted local repository: {repo_dir}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete local repository {repo_dir}: {e}")


def execute_git_command(command: list[str], cwd: str = None) \
        -> tuple[bool, str]:
    """
    Execute a git command using subprocess.

    Args:
    command (list[str]): The git command as a list of strings.
    cwd (str, optional): The current working directory for the command.

    Returns:
    tuple[bool, str]: A tuple containing a success flag and the command output.
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {e}")
        return False, e.stderr


def migrate_repo(repo: str, source: str, target: str, source_group: str,
                 target_group: str, use_ssh: bool) -> bool:
    """
    Migrate a git repository from source to target.

    Args:
    repo (str): The name of the repository.
    source (str): The source git server URL.
    target (str): The target git server URL.
    source_group (str): The group in the source server.
    target_group (str): The group in the target server.
    use_ssh (bool): Whether to use SSH for git operations.


    Returns:
    bool: True if migration was successful, False otherwise.
    """
    # Construct the source and target URLs based on the use_ssh flag
    source_url = f"git@{source}:{source_group}/{repo}.git" if use_ssh \
        else f"https://{source}/{source_group}/{repo}.git"
    target_url = f"git@{target}:{target_group}/{repo}.git" if use_ssh \
        else f"https://{target}/{target_group}/{repo}.git"
    logger.info(f'Start migrating {source_url} to {target_url}')

    # Clone the repository with all branches and tags
    logger.info(f'Cloning repo {source_url}')
    clone_cmd = ["git", "clone", "--bare", source_url]
    success, output = execute_git_command(clone_cmd)
    if not success:
        return False

    # # Change to the cloned repository directory
    # repo_dir = f"{repo}.git"

    # # Add the new remote
    # logger.info(f'Git remote add new-origin {source_url}')
    # add_remote_cmd = ["git", "remote", "add", "new-origin", target_url]
    # success, output = execute_git_command(add_remote_cmd, cwd=repo_dir)
    # if not success:
    #     return False

    # # Push all branches
    # logger.info('Git push branches to new-origin')
    # push_branches_cmd = ["git", "push", "new-origin", "--all"]
    # success, output = execute_git_command(push_branches_cmd, cwd=repo_dir)
    # if not success:
    #     return False

    # # Push all tags
    # logger.info('Git push tags to new-origin')
    # push_tags_cmd = ["git", "push", "new-origin", "--tags"]
    # success, output = execute_git_command(push_tags_cmd, cwd=repo_dir)
    # if not success:
    #     return False

    # logger.info(f"Successfully migrated repository: {repo}")
    return True


def readReposFromFile(path: str) -> list[str]:
    """
    Read repository names from a .txt file.

    Args:
        path (str): The path to the .txt file containing repository names.

    Returns:
        list[str]: A list of repository names.

    Raises:
        FileNotFoundError: If the specified file is not found.
        PermissionError: If there's no permission to access the file.
        Exception: For any other error while reading the file.
    """
    try:
        with open(path, 'r') as f:
            return [row.strip() for row in f]
    except FileNotFoundError:
        logger.error(f"File '{path}' not found.")
        sys.exit(1)
    except PermissionError:
        logger.error(f"Permission denied accessing file '{path}'.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error reading file '{path}': {str(e)}")
        sys.exit(1)


def read_toml_config(config_path: str) -> dict:
    try:
        with open(config_path, 'r') as f:
            return toml.load(f)
    except FileNotFoundError:
        logger.error(f"Config file '{config_path}' not found.")
        sys.exit(1)
    except toml.TomlDecodeError as e:
        logger.error(f"Error parsing TOML file: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error reading config file '{config_path}': {str(e)}")
        sys.exit(1)


def main():
    """
    Start function to orchestrate the repository migration process.

    This function parses command-line arguments, reads repository names,
    and initiates the migration process for each repository.
    """
    args = parse_args()
    if args.config:
        config = read_toml_config(args.config)
        source = config['Source']['source']
        source_group = config['Source']['source-group']
        target = config['Target']['target']
        target_group = config['Target']['target-group']
        repos = config['Repos']['reps']
        use_ssh = config.get('SSH', {}).get('use_ssh', False)  # Default to False if not specified
    else:
        check_args(args)
        source = args.source
        source_group = args.source_group
        target = args.target
        target_group = args.target_group
        if '.txt' in args.repos:
            repos = readReposFromFile(args.repos)
        else:
            repos = args.repos if isinstance(args.repos, list) else [args.repos]
        use_ssh = args.ssh
    """"""
    try:
        check_args(args)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

    print(repos)

    for repo in repos:
        success = migrate_repo(repo, source, target,
                               source_group, target_group, use_ssh)
        if not success:
            logger.error(f"Failed to migrate repository: {repo}")
        break

    # TODO Implment this
    # cleanup_repositories(repos)
    return


def check_args(args: argparse.ArgumentParser):
    """
    Check and validate command-line arguments.

    Args:
        args (argparse.ArgumentParser): Parsed command-line arguments.

    Raises:
        argparse.ArgumentTypeError: If source and target are the same.
    """
    try:
        if args.config:
            if any([args.source, args.target, args.repos,
                    args.source_group, args.target_group]):
                raise ValueError('When using a config file, do not specify \
                other arguments.')
        elif not all([args.source, args.target, args.repos,
                      args.source_group, args.target_group]):
            raise ValueError('All arguments are required when not using \
        a config file.')
        elif args.source == args.target:
            raise ValueError('Source and target cannot be equal')

    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)


def parse_args() -> argparse.Namespace():
    """
    Parse command-line arguments for the script.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        prog='Git-repo-migrater',
        description='Transfers git repos from one server to another.',
        epilog='Good luck and enjoy your coffee')

    parser.add_argument('-c', '--config', type=str,
                        help='Path to TOML configuration file')
    parser.add_argument('-s', '--source', type=str,
                        help='Source git server to migrate from')
    parser.add_argument('-t', '--target', type=str,
                        help='Target git server to migrate to')
    parser.add_argument('-r', '--repos', type=str, default=[],
                        help='List of repos to migrate.')
    parser.add_argument('--source-group', type=str, default=[],
                        help='Group which the repo belongs to in the source.')
    parser.add_argument('--target-group', type=str, default=[],
                        help='Group which the repo belongs to in the target.')
    parser.add_argument('--ssh', action='store_true',
                        help='Use SSH for git operations instead of HTTPS')
    return parser.parse_args()


if __name__ == '__main__':
    main()
