from config.settings import ALL_DIRS
from src.specification import generate_data_specification
from src.batch_pipeline import run_batch_pipeline
from src.quality import run_quality_checks
from src.analytics import generate_analytics
from src.rag import build_rag_corpus
from src.governance import generate_governance_outputs


def prepare_folders():
    for folder in ALL_DIRS:
        folder.mkdir(parents=True, exist_ok=True)


def main():
    prepare_folders()

    print("Start Data & AI Workshop Pipeline")

    generate_data_specification()
    run_batch_pipeline()
    run_quality_checks()
    generate_analytics()
    build_rag_corpus()
    generate_governance_outputs()

    print("Pipeline completed successfully")


if __name__ == "__main__":
    main()