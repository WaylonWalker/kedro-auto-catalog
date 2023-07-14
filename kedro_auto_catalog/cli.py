"""A collection of CLI commands for working with Kedro catalog."""

import click
from kedro.framework.cli.utils import KedroCliError, env_option
from kedro.framework.project import pipelines, settings
from kedro.framework.session import KedroSession
from kedro.framework.startup import ProjectMetadata
import yaml


def _create_session(package_name: str, **kwargs):
    kwargs.setdefault("save_on_close", False)
    try:
        return KedroSession.create(package_name, **kwargs)
    except Exception as exc:
        raise KedroCliError(
            f"Unable to instantiate Kedro session.\nError: {exc}"
        ) from exc


# pylint: disable=missing-function-docstring
@click.group(name="auto-catalog")
def auto_catalog_cli():  # pragma: no cover
    pass


@auto_catalog_cli.group()
def auto_catalog():
    """Commands for working with catalog."""


@auto_catalog.command("auto-catalog")
@env_option(help="Environment to create Data Catalog YAML file in. Defaults to `base`.")
@click.option(
    "--pipeline",
    "-p",
    "pipeline_name",
    type=str,
    required=True,
    help="Name of a pipeline.",
)
@click.pass_obj
def create_catalog(metadata: ProjectMetadata, pipeline_name, env):
    """Create Data Catalog YAML configuration with missing datasets.

    Add configurable datasets to Data Catalog YAML configuration file
    for each dataset in a registered pipeline if it is missing from
    the `DataCatalog`.

    The catalog configuration will be saved to
    `<conf_source>/<env>/catalog/<pipeline_name>.yml` file.

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
    """
    env = env or "base"
    session = _create_session(metadata.package_name, env=env)
    context = session.load_context()

    pipeline = pipelines.get(pipeline_name)

    if not pipeline:
        existing_pipelines = ", ".join(sorted(pipelines.keys()))
        raise KedroCliError(
            (
                f"'{pipeline_name}' pipeline not found!"
                f"Existing pipelines: {existing_pipelines}"
            )
        )

    pipe_datasets = {
        ds_name
        for ds_name in pipeline.data_sets()
        if not ds_name.startswith("params:") and ds_name != "parameters"
    }

    catalog_datasets = {
        ds_name
        for ds_name in context.catalog._data_sets.keys()
        if not ds_name.startswith("params:") and ds_name != "parameters"
    }

    # Datasets that are missing in Data Catalog
    missing_ds = sorted(pipe_datasets - catalog_datasets)
    if missing_ds:
        catalog_path = (
            context.project_path
            / settings.CONF_SOURCE
            / env
            / "catalog"
            / f"{pipeline_name}.yml"
        )
        _add_missing_datasets_to_catalog(missing_ds, catalog_path)
        click.echo(f"Data Catalog YAML configuration was created: {catalog_path}")
    else:
        click.echo("All datasets are already configured.")


def _add_missing_datasets_to_catalog(missing_ds, catalog_path):
    if catalog_path.is_file():
        catalog_config = yaml.safe_load(catalog_path.read_text()) or {}
    else:
        catalog_config = {}

    if not hasattr(settings, "AUTO_CATALOG"):
        settings["AUTO_CATALOG"] = {}

    directory = settings.AUTO_CATALOG.get("directory", "data")
    subdirs = settings.AUTO_CATALOG.get("subdirs", [])
    layers = settings.AUTO_CATALOG.get("layers", [])
    extension = settings.AUTO_CATALOG.get("default_extension", "parquet")
    _type = settings.AUTO_CATALOG.get("default_type", "pandas.ParquetDataSet")

    for ds_name in missing_ds:
        file_path = f"{directory}/{ds_name}.{extension}"
        config = {
            "type": _type,
            "filepath": str(file_path),
        }
        for _subdir in subdirs:
            if ds_name.startswith(_subdir):
                subdir = _subdir
                file_name = ds_name.replace(_subdir, "").strip("_")
                file_path = f"{directory}{subdir}/{file_name}.{extension}"

                config["filepath"] = str(file_path)
                break

        for layer in layers:
            if ds_name.startswith(layer):
                config["layer"] = layer
                break

        catalog_config[ds_name] = config

    # Create only `catalog` folder under existing environment
    # (all parent folders must exist).
    catalog_path.parent.mkdir(exist_ok=True)
    with catalog_path.open(mode="w") as catalog_file:
        yaml.safe_dump(catalog_config, catalog_file, default_flow_style=False)
