import pandas as pd

from src.db.database import Base, engine
from scripts.load_apps_info import load_apps_info_to_database
from scripts.load_apps_reviews import load_apps_reviews_to_database

APPS_PATH = "data/raw_data/apps_info.csv"
REVIEWS_PATH = "data/raw_data/apps_reviews.csv"


def inspect_csv(path: str, name: str):
    print(f"\n=== {name} ===")
    df = pd.read_csv(path, nrows=5)
    print("Columns:")
    print(df.columns.tolist())
    print("\nSample:")
    print(df.head())

# TODO main
def main():
    inspect_csv(APPS_PATH, "apps_info.csv")
    inspect_csv(REVIEWS_PATH, "apps_reviews.csv")

if __name__ == "__main__":
    inspect_csv(APPS_PATH, "apps_info.csv")
    inspect_csv(REVIEWS_PATH, "apps_reviews.csv")
    
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")

    load_apps_info_to_database()
    print("Apps info loaded to database successfully")

    load_apps_reviews_to_database()
    print("Apps reviews loaded to database successfully")
    
