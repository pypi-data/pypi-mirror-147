import pathlib
import setuptools

long_description = (pathlib.Path(__file__).parent / "README.md").read_text()

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.readlines()

setuptools.setup(
    name='moviesViewEstimator',
    version='0.0.8',
    license='MIT',
    author="Joao Paulo Euko",
    url='https://github.com/Joaopeuko/moviesViewEstimator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    packages=setuptools.find_packages(),
    package_data={'moviesViewEstimator': ['linear_regression_model.pickle']},
    install_requires=[requirement for requirement in requirements],
)
