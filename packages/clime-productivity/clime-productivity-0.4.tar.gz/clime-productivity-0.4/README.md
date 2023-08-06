# CLIME Productivity

> A tool to calculate the productivity of a Git repository

## Table of Contents

- [CLIME Productivity](#clime-productivity)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [Licensing](#licensing)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Shell Commands](#shell-commands)

## About

The Software Systems Laboratory (SSL) CLIME Productivity project is a tool to calculate the productivity of a Git repository.

### Licensing

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## How To Use

### Installation

You can install this tool with one of the following one liners:

- `pip install --upgrade pip clime-meta`
- `pip install --upgrade pip clime-productivity`

### Shell Commands

`clime-productivity-compute -h`

``` shell
options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        JSON file containing data formatted by ssl-metrics-git-commits-loc-extract
  -o OUTPUT, --output OUTPUT
                        JSON file containing data outputted by the application
```

`clime-productivity-graph -h`

``` shell
options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        The input data file that will be read to create the graphs
  -o OUTPUT, --output OUTPUT
                        The filename to output the bus factor graph to
  -m MAXIMUM_DEGREE_POLYNOMIAL, --maximum-degree-polynomial MAXIMUM_DEGREE_POLYNOMIAL
                        Estimated maximum degree of polynomial
  -r REPOSITORY_NAME, --repository-name REPOSITORY_NAME
                        Name of the repository that is being analyzed
  --x-window-min X_WINDOW_MIN
                        The smallest x value that will be plotted
  --x-window-max X_WINDOW_MAX
                        The largest x value that will be plotted
```
