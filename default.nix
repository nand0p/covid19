with import <nixpkgs> {};
stdenv.mkDerivation {
  name = "covid19";
  buildInputs = [
    gcc8
    ncurses
    libstdcxx5
  ];
}
