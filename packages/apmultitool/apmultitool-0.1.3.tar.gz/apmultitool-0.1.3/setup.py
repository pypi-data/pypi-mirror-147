import json
from setuptools import setup

meta = json.load(open("package.json", encoding="utf-8"))

setup(
    name=meta["name"],
    author=meta["author"],
    author_email=meta["email"],
    description=meta["description"],
    version=meta["version"],
    packages=["multitool"],
    package_dir={'multitool': 'multitool'},
    package_data={'multitool': ['assets/*']},
    include_package_data=True,
    license=open("LICENSE", encoding="utf-8").read(),
    long_description=open("README", encoding="utf-8").read(),
    keywords=meta["keywords"],
    url=meta["url"],
    entry_points={'console_scripts': [
        'multitool = multitool.__main__:main',
        'mtool = multitool.__main__:main'
    ]},
)
