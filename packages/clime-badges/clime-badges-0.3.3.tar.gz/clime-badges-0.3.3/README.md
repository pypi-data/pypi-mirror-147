# CLIME Badges

> A tool to create custom badges displaying CLIME metrics

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6477908.svg)](https://doi.org/10.5281/zenodo.6477908)
[![Release Project](https://github.com/SoftwareSystemsLaboratory/clime-badges/actions/workflows/release.yml/badge.svg)](https://github.com/SoftwareSystemsLaboratory/clime-badges/actions/workflows/release.yml)

## Table of Contents

- [CLIME Badges](#clime-badges)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [Licensing](#licensing)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Command Line Options](#command-line-options)

## About

The Software Systems Laboratory (SSL) CLIME Badges project is a tool to create custom badges displaying CLIME metrics.

### Licensing

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## How To Use

### Installation

You can install the tool from PyPi with one of the following one liners:

- `pip install clime-metrics`
- `pip install clime-badges`

### Command Line Options

`clime-badges -h`

``` shell
usage: CLIME Metric Badge Creator [-h] [-g GRAPH] [-lc LEFT_COLOR]
                                  [-lt LEFT_TEXT] [-u LINK] [-o OUTPUT]
                                  [-rt RIGHT_TEXT]
                                  [-rc--right-color RC__RIGHT_COLOR] [-v]

A tool to create a badge from a metric's graph

options:
  -h, --help            show this help message and exit
  -g GRAPH, --graph GRAPH
                        The metric graph SVG file to be used as the badge
                        logo. DEFAULT: metric.svg
  -lc LEFT_COLOR, --left-color LEFT_COLOR
                        Left side color. DEFAULT: maroon
  -lt LEFT_TEXT, --left-text LEFT_TEXT
                        Text to go on the left side of the badge. DEAULT:
                        CLIME Metric
  -u LINK, --link LINK  Link to a specific URL that will open when the badge
                        is clicked/ DEFAULT: None
  -o OUTPUT, --output OUTPUT
                        The output filename of the badge. NOTE: Must end in
                        .svg. DEFAULT: badge.svg
  -rt RIGHT_TEXT, --right-text RIGHT_TEXT
                        Text to go on the right side of the badge. DEFAULT:
                        None
  -rc--right-color RC__RIGHT_COLOR
                        Right side color. DEFAULT: gold
  -v, --version         Display version of the tool

Author(s): Nicholas M. Synovic, George K. Thiruvathukal
```
