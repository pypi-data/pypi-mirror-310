python -m venv .venv
source .venv/bin/activate
pip install -e .[dev] --only-binary :all:
pip freeze > requirements.txt