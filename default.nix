with import <nixpkgs> {};
stdenv.mkDerivation {
  name = "covid19";
  buildInputs = [
    gcc6
    ncurses
    libstdcxx5
    stdenv.cc.cc.lib
    libgcc
  ];
}
