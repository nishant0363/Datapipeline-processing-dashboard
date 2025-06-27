from src.ingestion import ingest_files
from src.transformation import preprocess, enrich
from src.validation import validate_and_profile
from src.loader import save_to_parquet

def run_pipeline():
    df = ingest_files()
    df = preprocess(df)
    df = enrich(df)
    validate_and_profile(df)
    save_to_parquet(df)

if __name__ == "__main__":
    run_pipeline()
