from setuptools import setup, find_packages

setup(
    name="census-consumer-complaint-ineuron",
    license="MIT",
    version="0.0.1",
    description="Project has been completed.",
    author="kaushal",
    packages=find_packages(),
    install_requires=['tfx==1.6.1', 'apache-beam[interactive]', 'apache-airflow']
)
