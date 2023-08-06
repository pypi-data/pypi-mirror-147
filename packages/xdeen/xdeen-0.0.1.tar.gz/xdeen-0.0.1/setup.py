from setuptools import setup, find_packages

# also change in version.py
VERSION = '0.0.1'
DESCRIPTION = "AI trading network for cryptocurrencies"
with open("requirements.txt", "r", encoding="utf-8") as f:
    REQUIRED_PACKAGES = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='xdeen',
    version=VERSION,
    author="Sherif Light",
    author_email="sherif@xdeen.net",
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://xdeen.net",
    project_urls={
        'Documentation': 'https://docs.xdeen.net',
        'Say Thanks!': 'https://xdeen.net/discord',
        'Source': 'https://github.com/xdeen-ai/xdeen',
        'Tracker': 'https://github.com/xdeen-ai/xdeen/issues',
    },
    install_requires=REQUIRED_PACKAGES,
    entry_points='''
        [console_scripts]
        xdeen=xdeen.__init__:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    include_package_data=True,
)
