import hashlib

import pandas as pd
from sqlalchemy.dialects.postgresql import insert

from src.db.database import SessionLocal
from src.db.models import Review
from scripts.text_cleaning import clean_text, clean_int, clean_datetime


CSV_PATH = "data/raw_data/apps_reviews.csv"
CHUNK_SIZE = 10_000

def make_review_hash(app_id, review_text, review_date):
    raw = f"{app_id}|{review_date}|{review_text}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

def prepare_reviews_chunk(chunk: pd.DataFrame):
    records = []

    for _, row in chunk.iterrows():
        app_id = clean_text(row.get("app_id"))
        review_text = clean_text(row.get("review_text"))

        if not app_id or not review_text:
            continue

        review_date = clean_datetime(row.get("review_date"))

        review_hash = make_review_hash(
            app_id=app_id,
            review_text=review_text,
            review_date=review_date,
        )

        records.append(
            {
                "app_id": app_id,
                "review_text": review_text,
                "review_score": clean_int(row.get("review_score")),
                "review_date": review_date,
                "helpful_count": clean_int(row.get("helpful_count")),
                "review_hash": review_hash,
            }
        )

    return records


def insert_reviews(session, records):
    if not records:
        return 0

    stmt = insert(Review).values(records)

    stmt = stmt.on_conflict_do_nothing(
        index_elements=["review_hash"]
    )

    result = session.execute(stmt)
    return result.rowcount or 0


def load_apps_reviews_to_database():
    total_seen = 0
    total_inserted = 0

    session = SessionLocal()

    try:
        for chunk_number, chunk in enumerate(
            pd.read_csv(CSV_PATH, chunksize=CHUNK_SIZE),
            start=1,
        ):
            print(f"Processing chunk {chunk_number}...")

            records = prepare_reviews_chunk(chunk)

            inserted = insert_reviews(session, records)
            session.commit()

            total_seen += len(chunk)
            total_inserted += inserted

            print(
                f"Chunk {chunk_number}: "
                f"seen={len(chunk)}, prepared={len(records)}, inserted={inserted}"
            )

        # Debug
        print("Reviews loading finished")
        print(f"Total seen: {total_seen}")
        print(f"Total inserted: {total_inserted}")

    except Exception as e:
        session.rollback()
        print("Error while loading reviews: ", e)
        raise

    finally:
        session.close()
