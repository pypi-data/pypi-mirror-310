# Pyqulator

![Static Badge](https://img.shields.io/badge/License-GNU_GPL_v3-blue)
![Static Badge](https://img.shields.io/badge/PyQt-6-green)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A fully functional Qt calculator written in Python using Sympy for calculations. The interface was created using Qt Designer and Qt Linguist.

## Features
+ Simple and lightweight
+ Standard, engineer and paper modes
+ Unit converter
+ Save journal as .txt
+ Move line up/down in paper mode
+ Available in 3 languages

## Installation
### From .deb file (Debian/Ubuntu/Linux Mint)
[Download .deb file](https://launchpad.net/~limafresh/+archive/ubuntu/pyqulator/+packages)

| Release filename | Build system | Compatible distributions |
| ---------------- | ------------ | ------------------------------------- |
| `pyqulator_<version>noble_all.deb` | Ubuntu Noble | Ubuntu Noble (24.04), Debian bookworm (12), Linux Mint 22, others based on Ubuntu 24.04 or Debian 12 |
| `pyqulator_<version>oracular_all.deb` | Ubuntu Oracular | Ubuntu Oracular (24.10) |
### From PPA (Ubuntu based distributions, 24.04 and newer)
```bash
sudo add-apt-repository ppa:limafresh/pyqulator
sudo apt update
sudo apt install pyqulator
```
### From PyPi via pip (any OS)
```bash
pip install pyqulator
```
### From sources via pip (any OS)
```bash
git clone https://github.com/limafresh/pyqulator.git
cd pyqulator
pip install .
```

## Usage
```bash
pyqulator
```
Or run it from the applications menu (it doesn't work from PyPi).

## Screenshots
*Standard mode*

![Screenshot](https://raw.githubusercontent.com/limafresh/pyqulator/main/screenshots/screenshot1.png)

*Engineer mode*

![Screenshot](https://raw.githubusercontent.com/limafresh/pyqulator/main/screenshots/screenshot2.png)

*Paper mode*

![Screenshot](https://raw.githubusercontent.com/limafresh/pyqulator/main/screenshots/screenshot3.png)

*Unit converter*

![Screenshot](https://raw.githubusercontent.com/limafresh/pyqulator/main/screenshots/screenshot4.png)

## Notes
### 05.11.2024
New release numbering: X.X.X.postX (Major, minor, patch, README update or something not related to code).
