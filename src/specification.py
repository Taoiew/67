"""Data specification and schema definitions."""

from pathlib import Path
import json

from config.settings import DATA_PLATFORM_DIR


def generate_data_specification() -> None:
    """Create a simple data specification artifact for the workshop pipeline."""
    spec_path = DATA_PLATFORM_DIR / "governance" / "data_specification.json"
    spec_path.parent.mkdir(parents=True, exist_ok=True)

    specification = {
        "dataset": "thammasat_workshop_dataset.xlsx",
        "source": "workshop_data",
        "fields": [
            "student_no",
            "program_id",
            "program_name",
            "gpa",
            "credit_earned",
            "expected_salary_thb",
            "career_interest",
        ],
        "generated_by": "thammasat-data-ai-workshop",
    }

    spec_path.write_text(json.dumps(specification, indent=2), encoding="utf-8")
    print(f"Created data specification at {spec_path}")
