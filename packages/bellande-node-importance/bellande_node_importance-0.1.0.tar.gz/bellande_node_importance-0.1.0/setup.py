from setuptools import setup, find_packages

with open("./README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bellande_node_importance",
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
        'bellande_node_importance': ['Bellande_Node_Importance'],
    },
    entry_points={
        'console_scripts': [
            'bellande_node_importance_executable = bellande_node_importance.bellande_node_importance_executable:main',
            'bellande_node_importance_api = bellande_node_importance.bellande_node_importance_api:main',
        ],
    },
    project_urls={
        "Home": "https://github.com/Robotics-Sensors/bellande_node_importance",
        "Homepage": "https://github.com/Robotics-Sensors/bellande_node_importance",
        "documentation": "https://github.com/Robotics-Sensors/bellande_node_importance",
        "repository": "https://github.com/Robotics-Sensors/bellande_node_importance",
    },
)
