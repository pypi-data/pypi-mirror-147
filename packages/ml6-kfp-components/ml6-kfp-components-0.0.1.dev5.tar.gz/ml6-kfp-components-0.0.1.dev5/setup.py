import glob
import importlib
import types
from pathlib import Path
from typing import List

from setuptools import find_namespace_packages, setup

BASE_DIR = Path(__file__).parent

PACKAGE_DIR_NAME = "ml6_kfp_components"

loader = importlib.machinery.SourceFileLoader(
    fullname="version",
    path=str(Path(PACKAGE_DIR_NAME) / "__init__.py"),
)
version = types.ModuleType(loader.name)
loader.exec_module(version)


def read_requirements(base_dir: str) -> List[str]:
    with open(Path(base_dir, "requirements.txt")) as fh:
        return [ln.strip() for ln in fh.readlines()]


def read_long_description(base_dir: str) -> str:
    return open(Path(base_dir, "README.md"), encoding="utf-8").read()


test_packages = [
    "coverage[toml]==6.3.2",
    "pytest==7.1.1",
    "pytest-cov==3.0.0",
    "flake8==3.8.3",
    "bandit[toml]==1.7.4",
    "black==22.3.0",
    "isort==5.10.1",
]

dev_packages = ["google-cloud-pipeline-components==1.0.2"]

docs_packages = [
    "mkdocs==1.2.3",
    "mkdocs-material==8.2.7",
    "mkdocstrings[python,python-legacy]==0.18.1",
    "mkdocs-macros-plugin==0.7.0",
]

setup(
    name="ml6-kfp-components",
    version=version.__version__,
    license="Apache License 2.0",
    description="A compilation of ML6 shared KFP components.",
    long_description=read_long_description(BASE_DIR),
    author="Maximilian Gartz",
    author_email="maximilian.gartz@ml6.eu",
    url="",
    keywords=["kfp", "vertex-ai-pipelines", "components"],
    classifiers=[],
    python_requires=">=3.7",
    packages=find_namespace_packages(),
    include_package_data=True,
    package_data={
        PACKAGE_DIR_NAME: [
            x.replace(PACKAGE_DIR_NAME, "") for x in glob.glob(PACKAGE_DIR_NAME + "/**/*.yaml", recursive=True)
        ]
    },
    install_requires=read_requirements(BASE_DIR),
    extras_require={
        "dev": test_packages + dev_packages + docs_packages,
        "test": test_packages,
        "docs": docs_packages,
    },
)
