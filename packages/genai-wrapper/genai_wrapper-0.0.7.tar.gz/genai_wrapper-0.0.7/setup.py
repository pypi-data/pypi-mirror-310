from setuptools import setup, find_packages
from pathlib import Path

current_dir = Path( __file__ ).parent
readme = (current_dir / "README.md" ).read_text()

setup(
    name="genai_wrapper",
    version="0.0.7",
    packages=find_packages(),
    install_requires=[
        "ai-api-client-sdk>=2.1.4",
        "ai-core-sdk>=2.3.11",
        "hdbcli>=2.21.28"
    ],
    author="Praveen Nair",
    author_email="",
    description="A user-friendly GenAI wrapper that leverages SAP's AI Core to seamlessly translate requests into LLM calls.",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    project_urls={
        "Source Repository": "https://github.com/praveen-nair/genai_wrapper",
        "Issues": "https://github.com/praveen-nair/genai_wrapper/issues"
    }
)
