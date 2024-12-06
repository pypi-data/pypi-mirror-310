from setuptools import setup, find_packages

setup(
    name="bisanggu",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "dnspython",
        "fastapi",
        "joblib",
        "pandas",
        "pydantic",
        "pymongo",
        "python_whois",
        "Requests",
        "selenium",
        "tldextract",
        "webdriver_manager",
        "xgboost",
    ],
    entry_points={
        "console_scripts": [
            "bisanggu=bisanggu.analyzer:crawl_website",
        ],
    },
    author="bisanggu",
    author_email="HitAnt.Exit@gmail.com",
    description="Phishing detection library",
    url="https://github.com/ZINH00/bisanggu",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)