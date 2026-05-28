import pandas as pd

from src.db.database import SessionLocal
from src.db.models import App
from scripts.text_cleaning import clean_text, clean_float, clean_int


CSV_PATH = "data/raw_data/apps_info.csv"

def load_apps_info_to_database():
    df = pd.read_csv(CSV_PATH)
    
    # Debug
    print("Apps columns:", df.columns.tolist())
    print("Apps rows:", len(df))

    session = SessionLocal()

    try:
        loaded_count = 0

        for _, row in df.iterrows():
            app_id = clean_text(row.get("app_id"))

            if not app_id:
                continue

            app = App(
                app_id=app_id,
                app_name=clean_text(row.get("app_name")) or "Unknown app",
                description=clean_text(row.get("description")),
                score=clean_float(row.get("score")),
                ratings_count=clean_int(row.get("ratings_count")),
                downloads=clean_int(row.get("downloads")),
                content_rating=clean_text(row.get("content_rating")),
                categories=clean_text(row.get("categories")),
            )

            session.merge(app)
            loaded_count += 1

        session.commit()
        print(f"Loaded/updated {loaded_count} apps")

    except Exception as e:
        session.rollback()
        print("Error while loading apps:", e)
        raise

    finally:
        session.close()
