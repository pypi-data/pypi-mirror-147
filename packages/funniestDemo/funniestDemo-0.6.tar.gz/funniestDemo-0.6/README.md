#README

Demo how to make a python package and upload it to PYPI

## 1. build the package and upload

```bash
python -m build

twine upload dist/*
```

## 2. Install the package from the pypi

```bash
python intall --upgrade funniestDemo
```

## 3. Execute the command

```bash
python -m funniestDemo
# or
funniest-joke
```

## Reference

- [如何打包你的Python代码](https://python-packaging-zh.readthedocs.io/zh_CN/latest/index.html)
- [Why you shouldn't invoke setup.py directly](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html)
- Youtube: [How to Build Python Packages for Pip](https://www.youtube.com/watch?v=JkeNVaiUq_c)
- [Aesthetic ASCII](https://github.com/jamescalam/aesthetic_ascii)
- [A sample Python project](https://github.com/pypa/sampleproject)