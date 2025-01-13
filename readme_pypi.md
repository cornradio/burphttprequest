# 发布到pypi

pip install twine build
python -m build
python -m twine upload dist/*
using api key from https://pypi.org/manage/account/token/

# 清理垃圾
rm -rf build dist burphttp.egg-info
win pwsh
Remove-Item -Recurse -Force build
Remove-Item -Recurse -Force dist
Remove-Item -Recurse -Force burphttp.egg-info

