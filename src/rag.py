"""RAG and retrieval module."""

import csv
from pathlib import Path

from config.settings import RAG_DIR, TRUSTED_DIR


def build_rag_corpus() -> None:
    """Create a RAG corpus artifact from the trusted dataset rows."""
    RAG_DIR.mkdir(parents=True, exist_ok=True)
    rag_path = RAG_DIR / "rag_excel_document_chunk.csv"

    trusted_path = TRUSTED_DIR / "trusted_student_snapshot.csv"
    if trusted_path.exists():
        with trusted_path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))

        output_rows = []
        for idx, row in enumerate(rows, start=1):
            student_no = row.get("student_no", "")
            program_name = row.get("program_name", "")
            career_interest = row.get("career_interest", "")
            gpa = row.get("gpa", "")
            expected_salary = row.get("expected_salary_thb", "")

            document_text = (
                f"Student {student_no} is recorded in the trusted dataset. "
                f"Program: {program_name}. "
                f"Career interest: {career_interest}. "
                f"GPA: {gpa}. "
                f"Expected salary: {expected_salary}."
            )
            output_rows.append({
                "source_row_no": idx,
                "entity_id": idx,
                "student_no": student_no,
                "source_url": "https://example.com/workshop",
                "rag_document_title": f"Trusted record for student {student_no}",
                "rag_keywords": f"student {student_no} {program_name} {career_interest}",
                "rag_expected_answer_hint": f"Student {student_no} is associated with {program_name}.",
                "document_text_full": document_text,
            })

        with rag_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "source_row_no",
                    "entity_id",
                    "student_no",
                    "source_url",
                    "rag_document_title",
                    "rag_keywords",
                    "rag_expected_answer_hint",
                    "document_text_full",
                ],
            )
            writer.writeheader()
            writer.writerows(output_rows)
    else:
        rag_path.write_text("", encoding="utf-8")
    print("RAG corpus built")
