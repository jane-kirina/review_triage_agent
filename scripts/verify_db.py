import pandas as pd

from src.db.database import engine


def run_query(query: str):
    return pd.read_sql(query, engine)


def main():
    print("\nApps count:")
    print(run_query("SELECT COUNT(*) AS apps_count FROM apps"))

    print("\nReviews count:")
    print(run_query("SELECT COUNT(*) AS reviews_count FROM reviews"))

    print("\nTop apps by review count:")
    print(
        run_query(
            """
            SELECT
                a.app_name,
                COUNT(r.id) AS reviews_count,
                ROUND(AVG(r.review_score)::numeric, 2) AS avg_review_score
            FROM apps a
            JOIN reviews r ON a.app_id = r.app_id
            GROUP BY a.app_name
            ORDER BY reviews_count DESC
            LIMIT 10
            """
        )
    )

    print("\nNull review text check:")
    print(
        run_query(
            """
            SELECT COUNT(*) AS empty_reviews
            FROM reviews
            WHERE review_text IS NULL OR LENGTH(TRIM(review_text)) = 0
            """
        )
    )


if __name__ == "__main__":
    main()