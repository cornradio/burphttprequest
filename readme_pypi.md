pip install twine build
python -m build
python -m twine upload dist/*
using api key from https://pypi.org/manage/account/token/