import argparse, os
from .baseline import create_baseline
from .watcher import start_watcher
from .logger import get_logger

logger = get_logger()

def main():
    parser = argparse.ArgumentParser(description='Minimal FIM Daemon - Option A')
    parser.add_argument('--baseline', help='Comma-separated dirs/files to baseline', required=False)
    parser.add_argument('--watch', help='Comma-separated dirs to watch (overrides baseline dirs)', required=False)
    parser.add_argument('--baseline-file', help='Path to baseline file', default='baseline.json')
    args = parser.parse_args()

    if args.baseline:
        items = [p.strip() for p in args.baseline.split(',') if p.strip()]
        logger.info(f'Creating baseline for: {items}')
        create_baseline(items, baseline_file=args.baseline_file)
        return

    # determine watch paths
    watch_paths = None
    if args.watch:
        watch_paths = [p.strip() for p in args.watch.split(',') if p.strip()]

    logger.info('Starting FIM watcher...')
    start_watcher(watch_paths, baseline_file=args.baseline_file)

if __name__ == '__main__':
    main()
