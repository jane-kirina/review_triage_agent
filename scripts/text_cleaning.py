import pandas as pd
import hashlib

def clean_text(value):
    if pd.isna(value):
        return None

    value = str(value).strip()
    value = value.replace(",", "")
    value = value.replace("+", "")

    return value if value else None


def clean_int(value):
    if pd.isna(value):
        return None

    value = str(value).strip()
    
    try:
        return int(float(value))
    except ValueError:
        return None


def clean_float(value):
    if pd.isna(value):
        return None

    try:
        return float(value)
    except ValueError:
        return None

def clean_datetime(value):
    if pd.isna(value):
        return None

    parsed = pd.to_datetime(value, errors="coerce")

    if pd.isna(parsed):
        return None

    return parsed.to_pydatetime()
