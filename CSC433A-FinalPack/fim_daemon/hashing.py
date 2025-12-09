import hashlib

def calculate_hash(path, algo='sha384'):
    """Calculate file hash using the specified algorithm (default sha384)."""
    if algo not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported hash algorithm: {algo}")
    h = hashlib.new(algo)
    with open(path, 'rb') as fh:
        while True:
            chunk = fh.read(4096)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()
