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
TRAD_SNAPSHOT_PATH = INTERIM / "comentarios_traducidos_1.0.csv"

BERT_EMBEDDINGS = PROCESSED / "bert_embeddings.npy"

# Models
MODELS_DIR = PROJ_ROOT / "models"

CHECKPOINTS_DIR = MODELS_DIR / "checkpoints"

