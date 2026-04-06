import sys
from pathlib import Path

# Корень проекта в PYTHONPATH для импорта app, models, …
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
