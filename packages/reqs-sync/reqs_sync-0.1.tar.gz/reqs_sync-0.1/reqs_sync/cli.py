import click
from pathlib import Path
from .r2toml import parse_requirements, update_pyproject_toml


@click.group()
@click.version_option(package_name="reqs-sync")
def cli():
    pass


@cli.command()
@click.argument('requirements_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='pyproject.toml',
              help='Output pyproject.toml file path')
@click.option('--group', '-g', help='Dependency group name (e.g., dev, prod)')
def reqs_to_toml(requirements_file, output, group):
    """Convert requirements.in to pyproject.toml dependencies."""
    dependencies = parse_requirements(requirements_file)
    update_pyproject_toml(dependencies, output, group)
    print(f"Successfully updated {output} with {len(dependencies)} dependencies")


if __name__ == '__main__':
    cli()
