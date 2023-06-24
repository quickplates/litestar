{
  inputs = {
    nixpkgs = {
      url = "github:NixOS/nixpkgs/nixos-unstable";
    };

    flake-parts = {
      url = "github:hercules-ci/flake-parts";
    };
  };

  outputs = inputs:
    inputs.flake-parts.lib.mkFlake {inherit inputs;} {
      # Import local override if it exists
      imports = [
        (
          if builtins.pathExists ./local.nix
          then ./local.nix
          else {}
        )
      ];

      # Sensible defaults
      systems = [
        "x86_64-linux"
        "i686-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      perSystem = {
        config,
        pkgs,
        system,
        ...
      }: let
        pytest = pkgs.python3.withPackages (ps: [ps.pytest ps.plumbum]);
        nil = pkgs.nil;
        task = pkgs.go-task;
        trunk = pkgs.trunk-io;
        # Build copier manually, because the nixpkgs version is outdated
        copier = pkgs.callPackage ./copier.nix {};
      in {
        # Override pkgs argument
        _module.args.pkgs = import inputs.nixpkgs {
          inherit system;
          config = {
            # Allow packages with non-free licenses
            allowUnfree = true;
            # Allow packages with broken dependencies
            allowBroken = true;
            # Allow packages with unsupported system
            allowUnsupportedSystem = true;
          };
        };

        # Set which formatter should be used
        formatter = pkgs.alejandra;

        # Define multiple development shells for different purposes
        devShells = {
          default = pkgs.mkShell {
            name = "dev";

            packages = [
              pytest
              nil
              task
              trunk
              copier
            ];
          };

          template = pkgs.mkShell {
            name = "template";

            packages = [
              task
              copier
            ];
          };

          lint = pkgs.mkShell {
            name = "lint";

            packages = [
              task
              trunk
            ];
          };

          test = pkgs.mkShell {
            name = "test";

            packages = [
              pytest
              task
              copier
            ];
          };
        };
      };
    };
}
