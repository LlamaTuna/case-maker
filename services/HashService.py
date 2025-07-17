# services/HashService.py
import hashlib

class HashService:
    @staticmethod
    def compute_hash(filepath):
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    @staticmethod
    def verify_hash(filepath, expected_hash):
        return HashService.compute_hash(filepath) == expected_hash


