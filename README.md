<h1 align="center">litestar</h1>

<div align="center">

Litestar app template 🌠

[![Lint](https://github.com/quickplates/litestar/actions/workflows/lint.yaml/badge.svg)](https://github.com/quickplates/litestar/actions/workflows/lint.yaml)
[![Test](https://github.com/quickplates/litestar/actions/workflows/test.yaml/badge.svg)](https://github.com/quickplates/litestar/actions/workflows/test.yaml)
[![Example](https://github.com/quickplates/litestar/actions/workflows/example.yaml/badge.svg)](https://github.com/quickplates/litestar/actions/workflows/example.yaml)

</div>

---

## 💡 About

This repository contains a [`copier`](https://copier.readthedocs.io) template
that can be used to create [`Litestar`](https://litestar.dev) apps.

You can view the example of project generated from this template
[**here**](https://github.com/quickplates/litestar-example).

## 📜 Usage

To create a new project from this template in the current directory,
make sure you have [`copier`](https://copier.readthedocs.io) installed and run:

```sh
copier copy gh:quickplates/litestar .
```

## 🚀 Features

- fully reproducible development environments with
  [`Dev Containers`](https://code.visualstudio.com/docs/remote/containers)
  and [`Nix`](https://nixos.org)
- automatic environment activation with [`direnv`](https://direnv.net)
- running tasks with [`Task`](https://taskfile.dev)
- formatting and linting with [`Trunk`](https://trunk.io)
- continuous integration with [`GitHub Actions`](https://github.com/features/actions)
- easy to write and nice looking documentation
  with [`Docusaurus`](https://docusaurus.io)
- optimized custom [`Docker`](https://www.docker.com) images
- automatic releases on [`GitHub Container Registry`](https://ghcr.io)
- dependency management with [`Poetry`](https://python-poetry.org)
- testing with [`pytest`](https://pytest.org)
- versatile configuration with
  [`Pydantic Settings`](https://docs.pydantic.dev/latest/concepts/pydantic_settings)
- pleasant command line interfaces with [`Typer`](https://typer.tiangolo.com)
  and [`Rich`](https://rich.readthedocs.io)
- support for [`Server-Sent Events`](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- live api documentation with [`Redoc`](https://redocly.com)

## 💻 Development

Read more about how to develop the project
[here](https://github.com/quickplates/litestar/blob/main/CONTRIBUTING.md).

If you have any ideas on how to improve this template,
please open an issue or submit a pull request.
All contributions are welcome! 🤗
