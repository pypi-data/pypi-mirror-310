from setuptools import setup, find_packages

with open("../../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bellande_limit",
    version="0.1.0",
    description="Robots Limit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="RonaldsonBellande",
    author_email="ronaldsonbellande@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
    ],
    keywords=["package", "setuptools"],
    python_requires=">=3.0",
    extras_require={
        "dev": ["pytest", "pytest-cov[all]", "mypy", "black"],
    },
    package_data={
        'bellande_limit': ['Bellande_Step'],
    },
    entry_points={
        'console_scripts': [
            'bellande_limit_executable = bellande_limit.bellande_limit_executable:main',
            'bellande_limit_api = bellande_limit.bellande_limit_api:main',
        ],
    },
    project_urls={
        "Home": "https://github.com/Robotics-Sensors/bellande_limit",
        "Homepage": "https://github.com/Robotics-Sensors/bellande_limit",
        "documentation": "https://github.com/Robotics-Sensors/bellande_limit",
        "repository": "https://github.com/Robotics-Sensors/bellande_limit",
    },
)
