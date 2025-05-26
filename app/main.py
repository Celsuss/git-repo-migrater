import argparse
import logging

logger = logging.getLogger(__name__)

def main():
    """Main function."""
    args = parse_args()
    try:
        check_arguments(args)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

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

  parser.add_argument('filename')
  parser.add_argument('-s', '--source', type=str, required=True, help='Source git server to migrate from')
  parser.add_argument('-t', '--target', type=str, required=True, help='Target git server to migrate to')
  parser.add_argument('-r', '--repos', type=str, default=[], required=True, help='List of repos to migrate.')
  return parser.parse_args()

if __name__ == '__main__':
    main()
