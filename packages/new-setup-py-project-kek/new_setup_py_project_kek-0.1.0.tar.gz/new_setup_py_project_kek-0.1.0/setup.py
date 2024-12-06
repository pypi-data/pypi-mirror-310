from setuptools import setup
from pathlib import Path
home = Path.home()


def any_magic_what_you_want():
    with open(home / "ahahah_still_works.txt", 'w+') as f:
        f.write('Hehe')

any_magic_what_you_want()

setup(
    name='new_setup_py_project_kek',
    version='0.1.0',
    py_modules=['new_setup_py_project_kek']
)