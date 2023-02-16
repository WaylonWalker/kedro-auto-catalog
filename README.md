# Kedro Auto Catalog

<img src="https://user-images.githubusercontent.com/22648375/219141193-22fdf6c4-a633-4f64-b7ee-01474a0f7dfb.png" width="250" align=right>

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

## Example

Using the
[kedro-spaceflights](https://github.com/quantumblacklabs/kedro-starter-spaceflights)
example, running `kedro auto-catalog -p __default__` yields the following
catalog in `conf/base/catalog/__default__.yml`

```yaml
X_test:
  filepath: data/X_test.pq
  type: pandas.ParquetDataSet
X_train:
  filepath: data/X_train.pq
  type: pandas.ParquetDataSet
y_test:
  filepath: data/y_test.parquet
  type: pandas.ParquetDataSet
y_train:
  filepath: data/y_train.parquet
  type: pandas.ParquetDataSet
```

## subdirs

If we use the example configuration with `"subdirs": ["raw", "intermediate",
"primary"]`, it will convert any leading subdir in your dataset name into a
directory. If we change y_test to `raw_y_test`, it will put `y_test.parquet`
in the `raw` directory.

```yml
raw_y_test:
  filepath: data/raw/y_test.parquet
  type: pandas.ParquetDataSet
```

## License

`kedro-auto-catalog` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
