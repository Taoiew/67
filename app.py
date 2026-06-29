import os
import re
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Thammasat Data & AI Workshop",
    layout="wide"
)

BASE_FOLDER = "data_platform"

trusted_path = f"{BASE_FOLDER}/trusted/trusted_student_snapshot.csv"
audit_path = f"{BASE_FOLDER}/audit/batch_audit.csv"
quality_path = f"{BASE_FOLDER}/quality/quality_overall.csv"
numeric_quality_path = f"{BASE_FOLDER}/quality/numeric_quality_summary.csv"
rag_corpus_path = f"{BASE_FOLDER}/rag/rag_excel_document_chunk.csv"
governance_folder = f"{BASE_FOLDER}/governance"

st.title("Thammasat Data & AI Workshop Application")

menu = st.sidebar.radio(
    "Select Page",
    [
        "Overview",
        "Trusted Data",
        "Batch Audit",
        "Data Quality",
        "Analytics",
        "RAG Q&A",
        "Governance"
    ]
)

def load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

df_trusted = load_csv(trusted_path)
df_audit = load_csv(audit_path)
df_quality = load_csv(quality_path)
df_numeric_quality = load_csv(numeric_quality_path)
df_rag = load_csv(rag_corpus_path)

def tokenize(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9ก-๙\s]", " ", text)
    return set(text.split())

def retrieve(query, corpus, top_k=5):
    query_tokens = tokenize(query)
    results = []

    if corpus.empty:
        return pd.DataFrame()

    for _, row in corpus.iterrows():
        doc_text = str(row.get("document_text_full", ""))
        doc_tokens = tokenize(doc_text)
        score = len(query_tokens.intersection(doc_tokens))

        results.append({
            "score": score,
            "source_row_no": row.get("source_row_no"),
            "entity_id": row.get("entity_id"),
            "student_no": row.get("student_no"),
            "source_url": row.get("source_url"),
            "rag_document_title": row.get("rag_document_title"),
            "rag_keywords": row.get("rag_keywords"),
            "rag_expected_answer_hint": row.get("rag_expected_answer_hint"),
            "document_text_full": doc_text
        })

    result_df = pd.DataFrame(results).sort_values("score", ascending=False)
    return result_df[result_df["score"] > 0].head(top_k)

def answer_question(query, corpus, top_k=5):
    retrieved = retrieve(query, corpus, top_k)

    if retrieved.empty:
        return "ไม่พบข้อมูลที่รองรับคำตอบใน workbook นี้", "not found", retrieved

    hints = retrieved["rag_expected_answer_hint"].dropna().astype(str).unique()
    answer = "จากข้อมูลใน workbook: " + " ".join(hints[:3])
    return answer, "grounded", retrieved

if menu == "Overview":
    st.header("Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Trusted Rows", len(df_trusted))
    col2.metric("Columns", df_trusted.shape[1] if not df_trusted.empty else 0)
    col3.metric("Latest Status", df_audit.tail(1)["status"].values[0] if not df_audit.empty else "N/A")

    st.subheader("Architecture Summary")
    st.markdown("""
    **Excel Dataset → Ingestion Pipeline → Raw Layer → Staging Layer → Data Quality Check → Trusted Layer → Analytics / RAG**

    This application demonstrates:
    - Trusted dataset
    - Batch audit log
    - Data quality summary
    - Analytics visualization
    - RAG question answering with source references
    - Data governance and access control
    """)

elif menu == "Trusted Data":
    st.header("Trusted Data")

    if df_trusted.empty:
        st.warning("Trusted dataset not found. Please run `python main.py` first.")
    else:
        st.dataframe(df_trusted, use_container_width=True)

elif menu == "Batch Audit":
    st.header("Batch Audit Log")

    if df_audit.empty:
        st.warning("Audit log not found. Please run `python main.py` first.")
    else:
        st.dataframe(df_audit, use_container_width=True)

        latest = df_audit.tail(1).iloc[0]
        st.subheader("Latest Run Summary")
        st.write("Run ID:", latest.get("run_id"))
        st.write("Status:", latest.get("status"))
        st.write("Source Count:", latest.get("source_count"))
        st.write("Loaded Count:", latest.get("loaded_count"))
        st.write("Checksum:", latest.get("input_file_checksum"))

elif menu == "Data Quality":
    st.header("Data Quality Dashboard")

    if df_trusted.empty:
        st.warning("Trusted dataset not found. Please run `python main.py` first.")
        st.stop()

    col1, col2, col3 = st.columns(3)

    duplicate_count = df_trusted.duplicated().sum()
    missing_total = int(df_trusted.isnull().sum().sum())

    col1.metric("Total Records", len(df_trusted))
    col2.metric("Duplicate Records", duplicate_count)
    col3.metric("Total Missing Values", missing_total)

    if not df_quality.empty:
        st.subheader("Overall Quality Evidence")
        st.dataframe(df_quality, use_container_width=True)

    if not df_numeric_quality.empty:
        st.subheader("Numeric Quality Evidence")
        st.dataframe(df_numeric_quality, use_container_width=True)

    st.subheader("Missing Values")

    missing = pd.DataFrame({
        "Column": df_trusted.columns,
        "Missing": df_trusted.isnull().sum().values,
        "Percent": (df_trusted.isnull().mean().values * 100).round(2)
    })

    st.dataframe(
        missing.sort_values("Missing", ascending=False),
        use_container_width=True
    )

    st.subheader("Numeric Summary")

    numeric_df = df_trusted.copy()
    for col in ["gpa", "credit_earned", "expected_salary_thb", "year_of_study"]:
        if col in numeric_df.columns:
            numeric_df[col] = pd.to_numeric(numeric_df[col], errors="coerce")

    numeric = numeric_df.select_dtypes(include="number")

    if not numeric.empty:
        st.dataframe(numeric.describe().T, use_container_width=True)
    else:
        st.info("No numeric columns found.")

    st.subheader("Category Distribution")

    category_candidates = [
        "record_type",
        "campus",
        "level",
        "status",
        "program_id",
        "career_interest",
        "learning_preference",
        "teamwork_style",
        "program_name"
    ]

    available_categories = [col for col in category_candidates if col in df_trusted.columns]

    if available_categories:
        category = st.selectbox("Select Column", available_categories)
        st.bar_chart(df_trusted[category].value_counts())
    else:
        st.info("No category columns available.")

    st.subheader("Overall Quality Status")

    if duplicate_count == 0:
        st.success("PASS: No duplicate rows detected.")
    else:
        st.error("FAIL: Duplicate rows detected.")

elif menu == "Analytics":
    st.header("Analytics Dashboard")

    if df_trusted.empty:
        st.warning("Trusted dataset not found. Please run `python main.py` first.")
    else:
        df = df_trusted.copy()

        for col in ["gpa", "credit_earned", "expected_salary_thb"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        col1, col2, col3 = st.columns(3)

        col1.metric("Average GPA", round(df["gpa"].mean(), 2) if "gpa" in df.columns else "N/A")
        col2.metric(
            "Avg Expected Salary",
            round(df["expected_salary_thb"].mean(), 2) if "expected_salary_thb" in df.columns else "N/A"
        )
        col3.metric("Students", df["student_no"].count() if "student_no" in df.columns else len(df))

        if "career_interest" in df.columns:
            st.subheader("Career Interest")
            st.bar_chart(df["career_interest"].value_counts())

        if "learning_preference" in df.columns:
            st.subheader("Learning Preference")
            st.bar_chart(df["learning_preference"].value_counts())

        if "teamwork_style" in df.columns:
            st.subheader("Teamwork Style")
            st.bar_chart(df["teamwork_style"].value_counts())

        if "expected_salary_thb" in df.columns:
            st.subheader("Expected Salary")
            st.line_chart(df["expected_salary_thb"].dropna())

elif menu == "RAG Q&A":
    st.header("RAG Question Answering")

    if df_rag.empty:
        st.warning("RAG corpus not found. Please run `python main.py` first.")
    else:
        sample_questions = [
            "Which students are interested in Data Engineer, AI Engineer, or analytics-related careers?",
            "What is the expected salary range from the mock salary expectation column?",
            "Which teamwork styles and learning preferences appear in the dataset?",
            "What should the system answer when the workbook does not contain evidence?"
        ]

        question = st.text_input("Ask a question from the workbook", value=sample_questions[0])
        top_k = st.slider("Top K Retrieved Rows", 1, 10, 5)

        if st.button("Ask"):
            answer, grounding_status, retrieved = answer_question(question, df_rag, top_k)

            st.subheader("Answer")
            st.write(answer)

            st.subheader("Grounding Status")
            st.write(grounding_status)

            st.subheader("Retrieved Sources")
            if retrieved.empty:
                st.info("No retrieved source.")
            else:
                source_cols = [
                    "score",
                    "source_row_no",
                    "entity_id",
                    "student_no",
                    "source_url",
                    "rag_document_title",
                    "rag_expected_answer_hint"
                ]
                st.dataframe(
                    retrieved[[col for col in source_cols if col in retrieved.columns]],
                    use_container_width=True
                )

elif menu == "Governance":
    st.header("Data Governance")

    classification_path = f"{governance_folder}/data_classification.csv"
    access_path = f"{governance_folder}/access_control_matrix.csv"
    rag_safety_path = f"{governance_folder}/rag_safety_rules.csv"
    production_path = f"{governance_folder}/production_governance_controls.csv"

    st.subheader("Data Classification")
    if os.path.exists(classification_path):
        st.dataframe(pd.read_csv(classification_path), use_container_width=True)
    else:
        st.warning("Data classification file not found. Please run `python main.py` first.")

    st.subheader("Access Control Matrix")
    if os.path.exists(access_path):
        st.dataframe(pd.read_csv(access_path), use_container_width=True)
    else:
        st.warning("Access control matrix not found. Please run `python main.py` first.")

    st.subheader("RAG Safety Rules")
    if os.path.exists(rag_safety_path):
        st.dataframe(pd.read_csv(rag_safety_path), use_container_width=True)
    else:
        st.warning("RAG safety rules not found. Please run `python main.py` first.")

    st.subheader("Production Governance Controls")
    if os.path.exists(production_path):
        st.dataframe(pd.read_csv(production_path), use_container_width=True)
    else:
        st.warning("Production governance controls not found. Please run `python main.py` first.")

    st.info(
        "This workbook is synthetic/mock workshop data. No masking, hashing, or encryption is required for this exercise. "
        "For real student data, stronger governance such as RBAC, encryption, masking, consent, audit logging, and retention policy would be required."
    )