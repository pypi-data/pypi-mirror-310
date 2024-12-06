import typer
from zenodo_api.retrieve import download_file_by_doi

cli = typer.Typer()


@cli.command()
def version():
    pass


@cli.command()
def download_from_geci_zenodo(
    doi: str = typer.Option(), is_sandbox: bool = typer.Option(False, "--is-sandbox")
):
    download_file_by_doi(doi, is_sandbox)
