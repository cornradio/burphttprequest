# 本地测试
pip install -e .

# 发布到pypi

pip install twine build
python3 -m build
python -m build
python3 -m twine upload dist/*
python -m twine upload dist/*

using api key from https://pypi.org/manage/account/token/


# 清理 build 
linux
rm -rf build dist burphttp.egg-info
windows pwsh
Remove-Item -Recurse -Force build 
Remove-Item -Recurse -Force dist 
Remove-Item -Recurse -Force burphttp.egg-info
