<h1 align="center">litestar</h1>

<div align="center">

Litestar project template 🌠

[![Lint](https://github.com/quickplates/litestar/actions/workflows/lint.yaml/badge.svg)](https://github.com/quickplates/litestar/actions/workflows/lint.yaml)
[![Test](https://github.com/quickplates/litestar/actions/workflows/test.yaml/badge.svg)](https://github.com/quickplates/litestar/actions/workflows/test.yaml)
[![Example](https://github.com/quickplates/litestar/actions/workflows/example.yaml/badge.svg)](https://github.com/quickplates/litestar/actions/workflows/example.yaml)

</div>

---

## 💡 About

This repository contains a [`copier`](https://copier.readthedocs.io) template
for creating [`Litestar`](https://litestar.dev) APIs.

You can view the example project generated from this template
[**here**](https://github.com/quickplates/litestar-example).

## 📜 Usage

To create a new project from this template in the current directory,
make sure you have [`copier`](https://copier.readthedocs.io) installed and run:

```sh
copier gh:quickplates/litestar .
```

## 🚀 Features

- fully reproducible development environments with
  [`Dev Containers`](https://code.visualstudio.com/docs/remote/containers)
  and [`Nix`](https://nixos.org)
- local virtual environments with [`venv`](https://docs.python.org/3/library/venv.html)
- dependency management with [`Poetry`](https://python-poetry.org)
- automatic environment activation with [`direnv`](https://direnv.net)
- testing with [`pytest`](https://pytest.org)
- versatile configuration with [`OmegaConf`](https://omegaconf.readthedocs.io)
  and [`Pydantic`](https://docs.pydantic.dev/latest)
- pleasant command line interfaces with [`Typer`](https://typer.tiangolo.com)
  and [`Rich`](https://rich.readthedocs.io)
- optimized custom [`Docker`](https://www.docker.com) images
- automatic releases on [`GitHub Container Registry`](https://ghcr.io)
- running tasks with [`Task`](https://taskfile.dev)
- formatting and linting with [`Trunk`](https://trunk.io)
- easy to write and nice looking documentation
  with [`Docusaurus`](https://docusaurus.io)
- continuous integration with [`GitHub Actions`](https://github.com/features/actions)

## 💻 Development

Read more about how to develop the project
[here](https://github.com/quickplates/litestar/blob/main/CONTRIBUTING.md).

If you have any ideas on how to improve this template,
please open an issue or submit a pull request.
All contributions are welcome! 🤗
