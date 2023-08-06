
import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
  name="arshipypiup",
  version="0.0.1",
  description="",
  long_description=README,
  long_description_content_type="text/markdown",
  author="arshi",
  author_email="arshi.khan67@gmail.com",
  license="MIT",
  packages=["arshipypiup"],
  zip_safe=False
)