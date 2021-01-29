# oasa.py

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/elemongw/oasa.py/Python%20application)
![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)
![MIT License](https://img.shields.io/github/license/elemongw/oasa.py)

This package is meant to provide a simple python interface for interacting with the OASA Telematics API (WIP, not ready). It also provides a simple CLI tool, oasa.py, for searching upcoming buses (already usable).

## Using oasa.py

```
$ oasa.py --help
usage: oasa.py [-h] [--line LINE] [--route ROUTE] [--stop [STOP ...]] [-V]

Get upcoming buses.

optional arguments:
  -h, --help         show this help message and exit
  --line LINE        line number eg. 831. Returns list of stops
  --route ROUTE      route number. Returns available routes
  --stop [STOP ...]  stop code(s). Returns upcoming buses if route is provided as well
  -V, --version      show program's version number and exit

Example usage: "oasa.py --stop 80506" or search for stop code: "oasa.py --line 831"
```

## More Resources

[Unofficial documentation for OASA Telematics API](https://oasa-telematics-api.readthedocs.io/)

## License

Copyright &copy; 2020 Georgios Retsinas

This project is licensed under the MIT License - see the LICENSE file for details
