from setuptools import setup, find_packages

setup(
    name="mantas_j_mod1_atsiskaitymas",
    version="0.1.0",
    author="Meskenaz",
    email="m.jankauskas123@gmail.com",
    packages=find_packages(),
    install_requires=[
        'lxml~=5.3.0',
        'selenium~=4.26.1',
        'pytest==8.3.3',
        'pytest-cov==6.0.0'
    ],
    python_requires=">=3.10"
)
