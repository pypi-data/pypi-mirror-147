## Steps to build package

python3 -m pip install --upgrade build

python3 -m build


### Create test pypi accound
https://test.pypi.org/account/register/

### Create and save private token
https://test.pypi.org/manage/account/#api-tokens


python3 -m pip install --upgrade twine

python3 -m twine upload --repository testpypi dist/*







## Installation from test.pypi.org
```
$ python3 -m venv venv
$ source venv/bin/activate
$ python -m pip install --index-url https://test.pypi.org/simple/ --no-deps oscar-ai

```


## Test it
```
$ python

>>> from oscar_ai.actions.speak import Speaker
>>> oscar = Speaker()
>>> oscar.say_something()
```


## Unistall
```
$ pip uninstall oscar-ai
```
