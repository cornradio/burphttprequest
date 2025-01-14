# 本地测试
pip install -e .

# 发布到pypi

pip install twine build
python3 -m build
python3 -m twine upload dist/*
using api key from https://pypi.org/manage/account/token/


