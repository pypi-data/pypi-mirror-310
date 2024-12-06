import setuptools

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
	name="Paolog_Pynecraft",
	version="0.1.1-112",
	include_package_data=True,
	package_data={"": ["*.*", "**/*.*"]},
	author="Paolog",
	description="A Minecraft recreation made with Ursina",
	packages=["Paolog_Pynecraft", "Paolog_Pynecraft.src.Games"],
	install_requires=['ursina', 'appdata', 'perlin_noise', 'screeninfo'],
	long_description=long_description,
    long_description_content_type='text/markdown'
)