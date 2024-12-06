from setuptools import setup, find_packages
import os
with open(os.path.join(os.path.dirname(__file__),"README.md")) as f:
    long_desc = f.read()
with open(os.path.join(os.path.dirname(__file__),"requirements.txt")) as f:
    dependencies = f.read().splitlines()

setup(
    name='mcterm',
    version='0.9.7',
    py_modules=["mcterm"],
    url='https://newgit.inuxnet.org/devel/bettermcrcon',
    license='MIT',
    license_files = ('LICENSE',),
    long_description=long_desc,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    project_urls={
        "Documentation": "https://newgit.inuxnet.org/devel/bettermcrcon",
        "Source Code": "https://newgit.inuxnet.org/devel/bettermcrcon",
    },
    packages=find_packages(where="mcterm"),
    package_dir={'': 'mcterm'},
    include_package_data=True,
    install_requires=dependencies,
    author='Jess Williams',
    keywords="minecraft mcrcon rcon remote command mojang cli mcterm terminal",
    author_email='devel@inuxnet.org',
    description='Better Minecraft Server Terminal',
    entry_points={"console_scripts": ["mcterm=mcterm:main"]},    
)
