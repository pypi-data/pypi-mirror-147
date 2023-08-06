import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name='pyvalo',
    version='0.2.2',
    packages=['valorant', 'valorant.utils'],
    url='https://github.com/vnpnh/Pyvalo',
    license='MIT',
    keywords="valorant tools",
    author='vnpnh',
    author_email='no@email.com',
    description='Unofficial Valorant Tools Library to Create Assistant Bot',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
    install_requires=["scikit-image", "opencv-python", 'pytesseract', 'numpy', 'PyAutoGUI'],
)



