# Chrome Database

## Disclaimer

This script is for educational purposes only, I don't endorse or promote it's illegal usage

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Languages](#languages)
4. [Installations](#installations)
5. [Usage](#usage)
6. [Run](#run)

## Overview

This script scans the google chrome database and gets the password

## Features

- It gets the passwords saved in the google chrome

## Languages

- Python 3.9.7

## Installations

```shell
git clone https://github.com/favoursyre/chrome-db.git && cd chrome-db
```

```shell
pip install pycryptodome
```

## Usage

Instantiating the class

```python
attacker, target = "Uchiha Minato", "Konoha"
scan = ChromeDatabase(attacker, target).main()
```

## Run

```shell
python chrome_database.py
```
