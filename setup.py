import os
from setuptools import setup

maindir = os.path.dirname(os.path.abspath(__file__))
install_requires = [l.strip() for l in open(os.path.join(maindir, 'requirements.txt'))]

setup(
    name="deus_ex_machina",
    version='0.1',
    packages=["deus_ex_machina"],
    description="SSH layer to interact with spiders on cloud instances",
    entry_points={
        'console_scripts': [
            'deus=deus_ex_machina.cmd:ssh'
        ]
    },
    install_requires=install_requires,
)
