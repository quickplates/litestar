# See https://github.com/NixOS/nixpkgs/blob/c081078/pkgs/tools/misc/copier/default.nix
{
  lib,
  git,
  python3,
  fetchFromGitHub,
}:
python3.pkgs.buildPythonApplication rec {
  pname = "copier";
  version = "8.0.0";
  format = "pyproject";

  src = fetchFromGitHub {
    owner = "copier-org";
    repo = "copier";
    rev = "v${version}";
    postFetch = ''
      rm -rf $out/.github $out/.vscode $out/docs $out/img $out/tests
    '';
    hash = "sha256-0bq+nhxhw6iisCqiK2R4XHg9d4TFw2+Cr0VEjLN7b4I=";
  };

  POETRY_DYNAMIC_VERSIONING_BYPASS = version;

  nativeBuildInputs = [
    python3.pkgs.poetry-core
    python3.pkgs.poetry-dynamic-versioning
  ];

  propagatedBuildInputs = with python3.pkgs; [
    colorama
    decorator
    dunamai
    funcy
    iteration-utilities
    jinja2
    jinja2-ansible-filters
    packaging
    pathspec
    plumbum
    pydantic
    pygments
    pyyaml
    pyyaml-include
    questionary
  ];

  makeWrapperArgs = [
    "--suffix PATH : ${lib.makeBinPath [git]}"
  ];
}
