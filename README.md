# Balance checker

[![Build Status](https://api.travis-ci.com/PauliusU/balance_checker.svg?branch=master)](https://travis-ci.com/github/PauliusU/p2p_balance_checker)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/PauliusU/balance_checker/blob/master/LICENSE)

Balance checker tool scrapes balance data of European P2P platforms and saves it in SQLite database.

**Table of contents:**

- [Balance checker](#balance-checker)
  - [Supported P2P platforms](#supported-p2p-platforms)
  - [Run locally](#run-locally)

## Supported P2P platforms

- [Bondora](https://www.bondora.com/) (via public API, no scraping used)
- [Finbee](https://p2p.finbee.lt/)
- [Lenndy](https://lenndy.com)
- [Paskolų klubas (NEO finance)](https://www.paskoluklubas.lt/)
- [Robo.cash](https://robo.cash)
- [ViaInvest](https://viainvest.com/)
- [Viventor](https://www.viventor.com/)

## Run locally

1. Clone this repo:

```bash
git clone https://github.com/PauliusU/balance_checker.git
```

2. cd into project

```bash
cd balance_checker
```

3. Install requirements:

```bash
pip install -r requirements.txt
```

4. Rename ".env_sample" to ".env" file and provide required logins

```bash
mv .env.example .env
```

5. Download [ChromeDriver](https://sites.google.com/chromium.org/driver/) (WebDriver for Chrome) and place in the `/bin` folder

6. Run demo:

```bash
python demo.py
```
