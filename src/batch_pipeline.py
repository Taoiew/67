"""Batch pipeline orchestration module."""

from pathlib import Path
import json

from config.settings import RAW_DIR, STAGING_DIR, TRUSTED_DIR, AUDIT_DIR, INPUT_FILE, SHEET_NAME


def run_batch_pipeline() -> None:
    """Create placeholder raw, staging, and trusted outputs for the workshop pipeline."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    TRUSTED_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    raw_path = RAW_DIR / "raw_snapshot.json"
    staging_path = STAGING_DIR / "staging_snapshot.json"
    trusted_path = TRUSTED_DIR / "trusted_student_snapshot.csv"
    audit_path = AUDIT_DIR / "batch_audit.csv"

    payload = {
        "input_file": str(INPUT_FILE),
        "sheet_name": SHEET_NAME,
        "status": "processed",
    }

    raw_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    staging_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    trusted_path.write_text("student_no,program_id,program_name\n1,101,Data Science\n", encoding="utf-8")
    audit_path.write_text(
        "run_id,status,source_count,loaded_count,input_file_checksum\n1,success,1,1,placeholder\n",
        encoding="utf-8",
    )
    print("Batch pipeline completed")
