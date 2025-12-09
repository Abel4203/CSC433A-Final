import os, json
from .hashing import calculate_hash

def create_baseline(paths, baseline_file='baseline.json', algo='sha384'):
    """Create baseline dict for given files/directories and save to baseline_file."""
    baseline = {'algorithm': algo, 'files': {}}
    for path in paths:
        if os.path.isfile(path):
            try:
                baseline['files'][path] = calculate_hash(path, algo)
            except Exception as e:
                print(f"Skipping {path}: {e}")
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for fname in files:
                    fp = os.path.join(root, fname)
                    try:
                        baseline['files'][fp] = calculate_hash(fp, algo)
                    except Exception as e:
                        # skip unreadable files
                        continue
    with open(baseline_file, 'w') as fh:
        json.dump(baseline, fh, indent=2)
    print(f"Baseline saved to {baseline_file}")
    return baseline

def load_baseline(baseline_file='baseline.json'):
    if not os.path.exists(baseline_file):
        return None
    with open(baseline_file, 'r') as fh:
        return json.load(fh)
