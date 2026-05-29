import pandas as pd

from src.db.database import engine

# Dataset overview queries
def get_dataset_overview():
    query = """
    SELECT
        (SELECT COUNT(*) FROM apps) AS apps_count,
        (SELECT COUNT(*) FROM reviews) AS reviews_count,
        (SELECT ROUND(AVG(review_score)::numeric, 2) FROM reviews) AS avg_review_score
    """

    return pd.read_sql(query, engine)

# App queries
def get_apps(limit: int = 100):
    query = """
    SELECT app_id, app_name, score, downloads, categories
    FROM apps
    ORDER BY app_name
    LIMIT %(limit)s
    """

    return pd.read_sql(query, engine, params={"limit": limit})

# Review queries
def get_reviews_by_app(app_id: str, limit: int = 100):
    query = """
    SELECT id, app_id, review_text, review_score, review_date, helpful_count
    FROM reviews
    WHERE app_id = %(app_id)s
    ORDER BY review_date DESC NULLS LAST
    LIMIT %(limit)s
    """

    return pd.read_sql(
        query,
        engine,
        params={
            "app_id": app_id,
            "limit": limit,
        },
    )

def get_review_score_distribution(app_id: str):
    query = """
    SELECT
        review_score,
        COUNT(*) AS count
    FROM reviews
    WHERE app_id = %(app_id)s
    GROUP BY review_score
    ORDER BY review_score
    """

    return pd.read_sql(query, engine, params={"app_id": app_id})

def get_top_apps_by_review_count(limit: int = 10):
    query = """
    SELECT
        a.app_name,
        COUNT(r.id) AS reviews_count,
        ROUND(AVG(r.review_score)::numeric, 2) AS avg_review_score
    FROM apps a
    JOIN reviews r ON a.app_id = r.app_id
    GROUP BY a.app_name
    ORDER BY reviews_count DESC
    LIMIT %(limit)s
    """

    return pd.read_sql(query, engine, params={"limit": limit})