from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

INPUT_FILE = BASE_DIR / "data" / "thammasat_workshop_dataset.xlsx"
SHEET_NAME = "workshop_data"

BUSINESS_DATE = "2026-06-29"

DATA_PLATFORM_DIR = BASE_DIR / "data_platform"

RAW_DIR = DATA_PLATFORM_DIR / "raw"
STAGING_DIR = DATA_PLATFORM_DIR / "staging"
TRUSTED_DIR = DATA_PLATFORM_DIR / "trusted"
QUALITY_DIR = DATA_PLATFORM_DIR / "quality"
ANALYTICS_DIR = DATA_PLATFORM_DIR / "analytics"
RAG_DIR = DATA_PLATFORM_DIR / "rag"
GOVERNANCE_DIR = DATA_PLATFORM_DIR / "governance"
AUDIT_DIR = DATA_PLATFORM_DIR / "audit"
SUBMISSION_DIR = DATA_PLATFORM_DIR / "submission"

ALL_DIRS = [
    RAW_DIR,
    STAGING_DIR,
    TRUSTED_DIR,
    QUALITY_DIR,
    ANALYTICS_DIR,
    RAG_DIR,
    GOVERNANCE_DIR,
    AUDIT_DIR,
    SUBMISSION_DIR,
]