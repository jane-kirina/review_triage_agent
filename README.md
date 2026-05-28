# Review Triage Agent

- **Problem:** App teams receive thousands of reviews, but manually reading them is slow
- **Solution:** This tool uses an LLM workflow to classify app reviews, extract product issues, and generate actionable summaries


The user uploads a CSV of app reviews, and the system automatically sorts the reviews into categories: bug report, feature request, pricing complaint, UX issue, praise, spam/irrelevant. Then it generates a short summary and a list of actions for the product/support team

## Workflow
- Upload CSV
- Preview columns
- User вибирає колонку з review text
- LLM класифікує кожен review у structured JSON
- LangGraph вирішує route
    - bug -> get severity + affected feature
    - feature request -> get requested feature + user motivation
    - complaint -> get topic + sentiment
    - spam/unclear -> mark as low confidence
- UI:
    - table review -> category -> confidence -> extracted issue
    - summary by catgories
    - top 5 repeated issues
    - export CSV/Markdown

## Stack
- Python
- LangGraph
- OpenAI / Anthropic / Gemini API
- Pydantic structured outputs
- Pandas
- Streamlit
- SQLite OR PostgreSQL
- Docker (optional)

## Dataset

[Play Market 2025 - 1M Reviews, 500+ Titles](https://www.kaggle.com/datasets/dmytrobuhai/play-market-2025-1m-reviews-500-titles)

### Data Ingestion Pipeline

The project uses a simple ETL pipeline to load Kaggle CSV files into PostgreSQL. The reviews loader processes the CSV in chunks and uses a generated `review_hash` to avoid duplicate inserts

1. Load data to database:

```bash
python scripts/data_ingestion.py
```

5. Verify loaded data:

```bash
python scripts/verify_db.py
```



## LangGraph Workflow
<!-- diagram or text graph -->

## Database Schema
<!-- short description -->

## Demo
<!-- screenshots -->

## How to Run Locally
<!-- steps without Docker -->
<!-- then add Docker -->

## Future Improvements
<!-- FastAPI, RAG over app descriptions, clustering, Jira export, human review queue -->



