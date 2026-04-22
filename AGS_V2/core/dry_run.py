import hashlib
import os
from sqlmodel import Session
from core.db import engine, ExecutionSnapshot

class DryRunEngine:
    """
    Coordinates the Two-Phase Commit boundary logic for safe sandbox mutations.
    Generates deterministic checksums BEFORE and AFTER an execution, enabling
    automatic rollback if Itachi Rejects the diff or the code fails.
    """

    def generate_directory_checksum(self, directory: str) -> str:
        """Creates an SHA-256 hash representing the absolute state of a directory."""
        hasher = hashlib.sha256()
        for root, dirs, files in os.walk(directory):
            # Skip python caching and git metadata
            if '.git' in root or '__pycache__' in root or 'venv' in root:
                continue
            for file in sorted(files):
                path = os.path.join(root, file)
                try:
                    with open(path, 'rb') as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            hasher.update(chunk)
                except Exception as e:
                    pass # ignore perm issues
        return hasher.hexdigest()

    def create_snapshot(self, task_id: str, paths_json: str = "[]") -> str:
        """Phase 1: Prepares the snapshot checksum."""
        checksum = self.generate_directory_checksum(".")
        
        with Session(engine) as session:
            snap = ExecutionSnapshot(
                task_id=task_id,
                pre_execution_checksum=checksum,
                paths_monitored_json=paths_json
            )
            session.add(snap)
            session.commit()
            
        print(f"[DRY-RUN] Snapshot committed for {task_id}: {checksum}")
        return checksum

dry_run_engine = DryRunEngine()
