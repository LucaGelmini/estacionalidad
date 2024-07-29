import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

PYPI_API_TOKEN = os.environ["PYPI_API_TOKEN"]

subprocess.run(
    ["twine", "upload", "--password", PYPI_API_TOKEN, "dist/*"], check=True
)  # type: ignore
