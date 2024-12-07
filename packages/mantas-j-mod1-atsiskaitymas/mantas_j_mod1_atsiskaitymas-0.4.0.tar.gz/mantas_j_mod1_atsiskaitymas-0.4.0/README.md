# Mantas J Mod1 Atsiskaitymas

![Python Unit Tests](https://github.com/MantasJankauskas/Mantas_J_Mod1_Atsiskaitymas/actions/workflows/python-tests.yml/badge.svg)
![PEP-8 Check](https://github.com/MantasJankauskas/Mantas_J_Mod1_Atsiskaitymas/actions/workflows/pep-8-check.yml/badge.svg)
[![codecov](https://codecov.io/github/MantasJankauskas/Mantas_J_Mod1_Atsiskaitymas/graph/badge.svg?token=ONTZWROC07)](https://codecov.io/github/MantasJankauskas/Mantas_J_Mod1_Atsiskaitymas)
[![PyPI version](https://img.shields.io/pypi/v/mantas-j-mod1-atsiskaitymas.svg)](https://pypi.org/project/mantas-j-mod1-atsiskaitymas/)

This Python package retrieves and parses data from two websites, offering the results in various formats.

---

## Installation

You can install the package from PyPI using the following command:

```bash
pip install mantas-j-mod1-atsiskaitymas
```

PyPI Link: [Mantas J Mod1 Atsiskaitymas](https://pypi.org/project/mantas-j-mod1-atsiskaitymas/)

---

## Usage

### Overview

The package's main method is `crawl()` from the `mantas_j_mod1_atsiskaitymas.web_crawler` module. This method fetches and parses data from the specified source and returns it in your preferred format.

### Parameters

- `source` (str): The source website to fetch data from. Supported options are:
  - `'eurovaistine'`
  - `'apotheka'`
- `timeout` (int): The maximum time (in seconds) to wait for a response.
- `return_format` (str): The format in which the data is returned. Supported options are:
  - `'json'`
  - `'csv'`
  - `'list'`

### Example

Here's a sample usage:

```python
from mantas_j_mod1_atsiskaitymas.web_crawler import crawl

data = crawl(source='eurovaistine', timeout=60, return_format='json')

print(data)
```