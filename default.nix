with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "covid19";
  buildInputs = [
    stdenv
    python38Packages.pip
    python38Packages.virtualenv
  ];
  src = null;
  shellHook = ''
    export GIT_SSL_CAINFO=/etc/ssl/certs/ca-bundle.crt
    export LD_LIBRARY_PATH=${stdenv.cc.cc.lib}/lib
    SOURCE_DATE_EPOCH=$(date +%s)
    virtualenv --no-setuptools venv
    source venv/bin/activate
    pip install -r requirements.txt --no-cache-dir
  '';
}
