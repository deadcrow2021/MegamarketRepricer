from pathlib import Path
import json
import sys
import os


if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

path = Path(application_path)

WORK_DIR = path.parent.absolute()

prices_dir = WORK_DIR / 'prices'


with open(WORK_DIR / 'keys.json', 'r') as f:
    keys = json.loads(f.read())
