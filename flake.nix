{
  description = "Python env for PDF to image slides + OpenCV";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          pdf2image
          pillow
          opencv4
        ]);
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.poppler  # Needed for pdf2image (provides pdftoppm)
          ];

          shellHook = ''
            echo "📄 PDF + OpenCV environment ready!"
          '';
        };
      });
}
