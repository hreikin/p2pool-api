# P2Pool API

[![PyPi](https://img.shields.io/badge/PyPi-0.0.2-green?labelColor=026ab5&style=flat-square&logo=pypi&logoColor=ffffff&link=https://pypi.org/project/xmrig/)](https://pypi.org/project/p2pool-api/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/p2pool-api?label=PyPI%20Downloads)
![License](https://img.shields.io/github/license/hreikin/p2pool-api?label=License&color=green)

This module provides the `P2PoolAPI` object to allow interacting with the P2Pool API.

## Getting Started

A quick overview of how to install and use this module can be found on the [Usage](usage.md) page, for a more detailed overview use the [Reference](reference.md) page.

## Contributing

Contributions are both encouraged and greatly appreciated.

To contribute content, fork this repo and make a pull request to the master branch including your changes.

- On GitHub, fork the p2pool-api repo
- Clone your newly created repo. (Note: replace your-username with your GitHub username)

via ssh:

```
git clone git@github.com:your-username/p2pool-api
```

via https:

```
git clone https://github.com/your-username/p2pool-api
```

- Navigate to the repo and create a new topic branch

```
cd p2pool-api
git checkout -b foobar
```

- After making modifications, commit and push your changes to your topic branch
- Open a PR against the p2pool-api main branch

## Run the documentation server locally

This documentation can be built and run locally.

- The build process for mkdocs utilizes Python
- It is recommended to install python pip dependencies inside of a Virtual Environment [(venv)](https://squidfunk.github.io/mkdocs-material/guides/creating-a-reproduction/#environment)

Note: You may need to first install `python3-venv` or the equivalent for your distribution

- Navigate to your `p2pool-api` repo
- Create the python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Install mkdocs dependencies to the venv

```bash
pip install -r requirements.txt
```

- Run the documentation server locally

```bash
mkdocs serve
```

- View your changes at [http://localhost:8000](http://localhost:8000)

## Donations

If you'd like to support further development of P2PoolAPI, you're welcome to send any amount of XMR to the following address:

`49ipjnJgoRnPsX8v5LVzUvfpSou6agomvKZnqD8zqFVqG6aqeUvKPyJ4WXhodiBPSvAuPNEmhF5QSiaJ59ZgFKwq9bXzCjz`