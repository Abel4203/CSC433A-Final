import time, json, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .baseline import load_baseline
from .hashing import calculate_hash
from .logger import get_logger

logger = get_logger()

class FIMHandler(FileSystemEventHandler):
    def __init__(self, baseline):
        super().__init__()
        self.baseline = baseline or {'files': {}, 'algorithm': 'sha384'}

    def dispatch(self, event):
        # handle all events
        try:
            super().dispatch(event)
        except Exception as e:
            logger.error(f'Error dispatching event: {e}')

    def on_created(self, event):
        path = event.src_path
        logger.info(f'Created: {path}')
        # If new file not in baseline -> alert
        if path not in self.baseline['files']:
            logger.warning(f'New unexpected file detected: {path}')

    def on_deleted(self, event):
        path = event.src_path
        logger.info(f'Deleted: {path}')
        if path in self.baseline['files']:
            logger.warning(f'Baseline file removed: {path}')

    def on_modified(self, event):
        path = event.src_path
        logger.info(f'Modified: {path}')
        if os.path.isfile(path):
            algo = self.baseline.get('algorithm', 'sha384')
            try:
                current = calculate_hash(path, algo)
            except Exception as e:
                logger.error(f'Unable to hash {path}: {e}')
                return
            stored = self.baseline['files'].get(path)
            if stored and current != stored:
                logger.warning(f'File modified (hash mismatch): {path}')
            elif not stored:
                logger.warning(f'File modified but not in baseline: {path}')

def start_watcher(paths_to_watch=None, baseline_file='baseline.json'):
    baseline = load_baseline(baseline_file) or {'files': {}, 'algorithm': 'sha384'}
    if not paths_to_watch:
        # default to directories present in baseline
        dirs = set(os.path.dirname(p) for p in baseline['files'].keys() if os.path.dirname(p))
        paths_to_watch = list(dirs) or ['.']

    event_handler = FIMHandler(baseline)
    observer = Observer()
    for p in paths_to_watch:
        if os.path.exists(p):
            observer.schedule(event_handler, p, recursive=True)
            logger.info(f'Watching: {p}')
        else:
            logger.warning(f'Path does not exist, skipping: {p}')

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
