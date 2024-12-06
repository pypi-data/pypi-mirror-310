# S3 Serve

<div align="center">

![Logo](docs/logo.png)

</div>

<div align="center">

[![Build Status](https://github.com/robvanderleek/s3serve/workflows/main/badge.svg)](https://github.com/robvanderleek/s3serve/actions)
[![Dependabot](https://badgen.net/badge/Dependabot/enabled/green?icon=dependabot)](https://dependabot.com/)

</div>

*A Simple S3 Server 🗄️*

# Development

After installing dependencies with `poetry install`, S3 Serve can be run from
the repository root like this:

```shell
poetry run s3serve
```

## Local installation using pipx

To install the development repository locally run:

```shell
pipx install .
```

To install the `main` branch locally run:

```shell
pipx install git+https://github.com/robvanderleek/s3serve.git
```

Or to install another branch locally run:

```shell
pip install git+https://github.com/robvanderleek/s3serve.git@issue-123
``` 
