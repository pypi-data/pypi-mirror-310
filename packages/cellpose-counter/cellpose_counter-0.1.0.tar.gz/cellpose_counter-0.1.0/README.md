# cellpose-counter

[![License BSD-3](https://img.shields.io/pypi/l/cellpose-counter.svg?color=green)](https://github.com/szablowskilab/cellpose-counter/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/cellpose-counter.svg?color=green)](https://pypi.org/project/cellpose-counter)
[![Python Version](https://img.shields.io/pypi/pyversions/cellpose-counter.svg?color=green)](https://python.org)
[![tests](https://github.com/szablowskilab/cellpose-counter/workflows/tests/badge.svg)](https://github.com/szablowskilab/cellpose-counter/actions)
[![codecov](https://codecov.io/gh/szablowskilab/cellpose-counter/branch/main/graph/badge.svg)](https://codecov.io/gh/szablowskilab/cellpose-counter)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/cellpose-counter)](https://napari-hub.org/plugins/cellpose-counter)

A Napari plugin for cell/nuclei counting from a region or interest using
cellpose models.

----------------------------------

## Installation

Option 1: Install in Napari directly under the plugins tab and select
cellpose-counter.

Option 2: via [pip](https://pip.pypa.io/en/stable/)(or pip alternatives like
[uv](https://docs.astral.sh/uv/)):

```bash
# install napari and cellpose-counter plugin
pip install napari[all] cellpose-counter

# or if you prefer uv
uv add "napari[all]" cellpose-counter
```

## Usage

To start, napari, run the cli using `napari -w cellpose-counter`



## Contributing

All contributions are welcome. Please submit an issue for feedback or bugs.

## Citations

This plugin is built on top of the Cellpose segmentation and denoising models.
If you use this plugin, please cite the following paper:

```bitex
@article{stringer2021cellpose,
title={Cellpose: a generalist algorithm for cellular segmentation},
author={Stringer, Carsen and Wang, Tim and Michaelos, Michalis and Pachitariu, Marius},
journal={Nature Methods},
volume={18},
number={1},
pages={100--106},
year={2021},
publisher={Nature Publishing Group}
}
```

## License

[BSD-3](./LICENSE)
