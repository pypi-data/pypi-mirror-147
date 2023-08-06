from setuptools import setup, find_packages

setup(
    name="blabpy",
    version="0.8.0",
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=['pandas', 'numpy', 'pyarrow', 'pympi-ling', 'pydub', 'StrEnum'],
    package_data={'blabpy': ['vihi/intervals/etf_templates/*.etf',
                             'vihi/intervals/etf_templates/*.pfsx']}
)
