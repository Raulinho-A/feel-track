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

# CLIPS = PROCESSED / "bboxes" / "clips"
# AUGMENTED = PROCESSED / "bboxes" / "augmented"

# Models
MODELS_DIR = PROJ_ROOT / "models"

CHECKPOINTS_DIR = MODELS_DIR / "checkpoints"

