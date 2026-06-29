"""Analytics and reporting module."""

from config.settings import ANALYTICS_DIR, TRUSTED_DIR


def generate_analytics() -> None:
    """Create a simple analytics report artifact."""
    ANALYTICS_DIR.mkdir(parents=True, exist_ok=True)
    analytics_path = ANALYTICS_DIR / "analytics_summary.txt"

    trusted_path = TRUSTED_DIR / "trusted_student_snapshot.csv"
    row_count = 0
    if trusted_path.exists():
        with trusted_path.open("r", encoding="utf-8") as handle:
            row_count = sum(1 for _ in handle) - 1

    analytics_path.write_text(
        f"Trusted rows: {row_count}\nAnalytics generated successfully\n",
        encoding="utf-8",
    )
    print("Analytics generated")
