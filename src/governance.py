import pandas as pd
from config.settings import GOVERNANCE_DIR


def generate_governance_outputs():
    classification_df = pd.DataFrame([
        {
            "data_group": "Traceability / Row Identity",
            "columns": "record_type, entity_id, source_row_no",
            "classification": "Lineage / Audit",
            "usage_rule": "Use for routing, lineage, source evidence, and rerun checks."
        },
        {
            "data_group": "Synthetic Student Profile",
            "columns": "student_no, citizen_id, email, mobile, student_name",
            "classification": "Synthetic Profile Data",
            "usage_rule": "Use as mock workshop fields. No masking, hashing, or encryption required."
        },
        {
            "data_group": "Academic Attributes",
            "columns": "level, faculty_or_school, program_id, program_name, campus, gpa, credit_earned",
            "classification": "Academic Mock Data",
            "usage_rule": "Use for grouping, filtering, analytics, and quality summary."
        },
        {
            "data_group": "Behavior and Career",
            "columns": "behavior_profile, teamwork_style, learning_preference, career_interest, internship_interest",
            "classification": "Behavior / Career Mock-up",
            "usage_rule": "Use for mock data product questions, visualization, and RAG examples."
        },
        {
            "data_group": "Expected Salary",
            "columns": "expected_salary_thb, salary_expectation_note",
            "classification": "Mock Salary Data",
            "usage_rule": "Use for analytics and RAG examples. Must state that it is not official salary data."
        },
        {
            "data_group": "RAG Fields",
            "columns": "rag_document_title, rag_document_text, rag_keywords, rag_sample_question, rag_expected_answer_hint",
            "classification": "RAG Corpus",
            "usage_rule": "Use directly as RAG corpus with source_row_no, entity_id, student_no, or source_url as evidence."
        },
        {
            "data_group": "Operational Metadata",
            "columns": "batch_date, snapshot_date, source_system, source_url, task_hint",
            "classification": "Operational / Source Metadata",
            "usage_rule": "Use for audit, lineage, citation, and run explanation."
        }
    ])

    access_control_df = pd.DataFrame([
        {
            "layer": "Raw Layer",
            "allowed_role": "Data Engineer, Governance Reviewer",
            "access_purpose": "Inspect original Excel rows and trace source evidence."
        },
        {
            "layer": "Staging Layer",
            "allowed_role": "Data Engineer",
            "access_purpose": "Validate schema, convert types, and clean data."
        },
        {
            "layer": "Trusted Layer",
            "allowed_role": "Data Team",
            "access_purpose": "Use clean trusted data for analytics and RAG preparation."
        },
        {
            "layer": "Analytics Layer",
            "allowed_role": "Business Analyst, Instructor, Student Team",
            "access_purpose": "View summary, dashboard, and visualization."
        },
        {
            "layer": "RAG Layer",
            "allowed_role": "End User, Instructor, Student Team",
            "access_purpose": "Ask questions from approved workbook context with source citation."
        },
        {
            "layer": "Audit / Metadata",
            "allowed_role": "Project Manager, Data Engineer, Governance Reviewer",
            "access_purpose": "Check run status, lineage, checksum, and quality evidence."
        }
    ])

    rag_safety_df = pd.DataFrame([
        {
            "rule": "Answer only from workbook evidence",
            "description": "The RAG response must use retrieved Excel context only."
        },
        {
            "rule": "Show source reference",
            "description": "Every answer should show source_row_no, entity_id, student_no, or source_url."
        },
        {
            "rule": "Do not guess",
            "description": "If no retrieved context supports the answer, return not found."
        },
        {
            "rule": "Mock data warning",
            "description": "Salary and behavior fields are mock workshop data, not official records."
        }
    ])

    production_control_df = pd.DataFrame([
        {
            "control": "Masking / Hashing",
            "workshop_decision": "Not required for this synthetic workbook.",
            "production_decision": "Required for real student identifiers or sensitive personal data."
        },
        {
            "control": "Encryption",
            "workshop_decision": "Not implemented.",
            "production_decision": "Encrypt data at rest and in transit."
        },
        {
            "control": "Access Control",
            "workshop_decision": "Defined as role-based assumption.",
            "production_decision": "Implement RBAC, approval workflow, and least privilege."
        },
        {
            "control": "Audit Log",
            "workshop_decision": "Implemented with batch_audit.csv.",
            "production_decision": "Centralized logging and monitoring."
        },
        {
            "control": "Data Retention",
            "workshop_decision": "Keep outputs for demo evidence.",
            "production_decision": "Define retention period and deletion policy."
        }
    ])

    classification_df.to_csv(GOVERNANCE_DIR / "data_classification.csv", index=False)
    access_control_df.to_csv(GOVERNANCE_DIR / "access_control_matrix.csv", index=False)
    rag_safety_df.to_csv(GOVERNANCE_DIR / "rag_safety_rules.csv", index=False)
    production_control_df.to_csv(GOVERNANCE_DIR / "production_governance_controls.csv", index=False)

    print("Governance outputs generated")