from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJ_ROOT = Path(__file__).resolve().parents[1]

# Data
DATA_DIR = PROJ_ROOT / "data"

EXTERNAL = DATA_DIR / "external"
INTERIM = DATA_DIR / "interim"
PROCESSED = DATA_DIR / "processed"
RAW = DATA_DIR / "raw"

TIKTOK_COMMENTS = RAW / "comentarios_tiktok_consolidados_1.0.csv"

EXP_SNAPSHOT_PATH = INTERIM / "comentarios_explorados_1.0.csv"

GOLDEN_SET_PATH = INTERIM / "golden_set_to_label.csv"
GOLDEN_SET_LABELED_PATH = INTERIM / "golden_set_labeled.csv"

BERT_EMBEDDINGS = PROCESSED / "bert_embeddings.npy"
BERT_SENTIMENT_PATH = INTERIM / "comments_with_bert_sentiment.csv"

# Models
MODELS_DIR = PROJ_ROOT / "models"

CHECKPOINTS_DIR = MODELS_DIR / "checkpoints"

