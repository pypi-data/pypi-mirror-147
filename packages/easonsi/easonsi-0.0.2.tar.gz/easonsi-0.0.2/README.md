# 个人 package

- `mypackage` 尝试 pipenv 创建虚拟环境

```sh
python3 -m pip install --upgrade pip build twine

# Generating distribution archives
python3 -m build
# Uploading the distribution archives
python3 -m twine upload --repository pypi dist/*
```
