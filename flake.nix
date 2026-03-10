{
  description = "A command-line interface for searching and streaming anime from multiple providers.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        kaizoku-cli = pkgs.python3Packages.buildPythonApplication {
          pname = "kaizoku-cli";
          version = "0.1.0";
          src = ./.;
          format = "setuptools";

          propagatedBuildInputs =
            with pkgs.python3Packages;
            [
              beautifulsoup4
              certifi
              charset-normalizer
              idna
              m3u8
              markdown-it-py
              mdurl
              prompt-toolkit
              pygments
              textual
              requests
              soupsieve
              typing-extensions
              urllib3
              wcwidth
            ]
            ++ [
              pkgs.mpv
            ];
        };
      in
      {
        packages.default = kaizoku-cli;

        apps.default = {
          type = "app";
          program = "${kaizoku-cli}/bin/kaizoku-cli";
        };
      }
    );
}
