import argparse
import logging

logger = logging.getLogger(__name__)

def readFromFile(path: str) -> list[str]:
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


def main():
    """Main function."""
    args = parse_args()
    try:
        check_arguments(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    if '.txt' in args.repos:
        repos = readReposFromFile(args.repos)
    else:
        repos = args.repos

    return


def check_args(args: argparse.ArgumentParser):
    if args.source == args.target:
        logger.error(f'Source and target are both {args.source}')
        raise argparse.ArgumentTypeError('Source and target can not be equal')


def parse_args() -> argparse.Namespace():
  parser = argparse.ArgumentParser(
      prog='Git-repo-migrater',
      description='Transfers git repos from one server to another.',
      epilog='Good luck and enjoy your coffee')

  parser.add_argument('-s', '--source', type=str, required=True, help='Source git server to migrate from')
  parser.add_argument('-t', '--target', type=str, required=True, help='Target git server to migrate to')
  parser.add_argument('-r', '--repos', type=str, default=[], required=True, help='List of repos to migrate.')
  return parser.parse_args()

if __name__ == '__main__':
    main()
