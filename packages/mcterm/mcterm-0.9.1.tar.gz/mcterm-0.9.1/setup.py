from setuptools import setup, find_packages

setup(
    name='mcterm',
    version='0.9.1',
    py_modules=["mcterm"],
    url='https://newgit.inuxnet.org/devel/bettermcrcon',
    license='MIT',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(where="mcterm"),
    package_dir={'': 'mcterm'},
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),
    author='Jess Williams',
    keywords="minecraft mcrcon rcon remote command mojang cli mcterm terminal",
    author_email='devel@inuxnet.org',
    description='Better Minecraft Server Terminal',
    entry_points={"console_scripts": ["mcterm=mcterm:main"]},    
)
