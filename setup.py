from setuptools import setup, find_packages

setup(
    name="tmdb",
    version="0.0.1",
    description="Rename Episodes Using the TMDB Database.",
    author="huhuhang",
    author_email="huhuhang#gmail.com",
    url="https://github.com/huhuhang/tmdb-renamer",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">3.8.0",
    install_requires=["Click", "requests", "rich", "retrying"],
    entry_points="""
        [console_scripts]
        tmdb=tmdb.cli:cli
    """,
)
