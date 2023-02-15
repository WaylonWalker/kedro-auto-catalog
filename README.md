# Kedro Auto Catalog

A configurable version of the built in `kedro catalog create` cli. Default
types can be configured in the projects settings.py, to get these types rather
than `MemoryDataSets`.

[![PyPI - Version](https://img.shields.io/pypi/v/kedro-auto-catalog.svg)](https://pypi.org/project/kedro-auto-catalog)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kedro-auto-catalog.svg)](https://pypi.org/project/kedro-auto-catalog)

---

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install kedro-auto-catalog
```

## Configuration

Configure the project defaults in `src/<project_name>/settings.py` with this
dict.

```python
AUTO_CATALOG = {
    "directory": "data",
    "subdirs": ["raw", "intermediate", "primary"],
    "default_extension": "parquet",
    "default_type": "pandas.ParquetDataSet",
}
```

## Usage

To auto create catalog entries for the `__default__` pipeline, run this from the command line.

```bash
kedro auto-catalog -p __default__
```

If you want a reminder of what to do, use the `--help`.

```bash
❯ kedro auto-catalog --help❯
Usage: kedro auto-catalog [OPTIONS]

  Create Data Catalog YAML configuration with missing datasets.

  Add configurable datasets to Data Catalog YAML configuration file for each
  dataset in a registered pipeline if it is missing from the `DataCatalog`.

  The catalog configuration will be saved to
  `<conf_source>/<env>/catalog/<pipeline_name>.yml` file.

  Configure the project defaults in `src/<project_name>/settings.py` with this
  dict.

Options:
  -e, --env TEXT       Environment to create Data Catalog YAML file in.
                       Defaults to `base`.
  -p, --pipeline TEXT  Name of a pipeline.  [required]
  -h, --help           Show this message and exit.
```

## License

`kedro-auto-catalog` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
