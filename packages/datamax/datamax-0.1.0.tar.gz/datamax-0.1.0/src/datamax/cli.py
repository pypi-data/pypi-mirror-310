import os
from pathlib import Path
from typing import Any, Literal

import click
from rich.table import Table

from datamax.build.builder import Builder
from datamax.console import console
from datamax.distribute.distributor import Distributor
from datamax.runtime.run import Runner


@click.group("cli")
def main(): ...


def validate_tag(ctx, param, value):
    try:
        tag_parts = value.split(":")
        return (
            (tag_parts[0], tag_parts[1])
            if len(tag_parts) > 1
            else (tag_parts[0], "")
            if len(tag_parts) == 1
            else ("", "")
        )
    except Exception:
        raise click.BadParameter("Tag must be in the format 'name:tag' or 'name'")


@main.command
def images():
    table_columns = ["name", "tag", "digest", "created"]
    console.log("Listing images...")
    table = Table(title="Datamax Images")
    images = Builder.list_images()
    if not images:
        console.log("No images found.")
        return
    for column in table_columns:
        table.add_column(column)
    for image in images:
        table.add_row(*[image[key] for key in table_columns])
    console.print(table)


@main.command
@click.option(
    "--file", "-f", help="cargofile to read from", type=click.Path(exists=True)
)
@click.option(
    "--tag",
    "-t",
    help="tag for the image",
    type=click.UNPROCESSED,
    callback=validate_tag,
)
@click.argument("context", type=click.Path(exists=True))
def build(file: os.PathLike, tag: Any, context: os.PathLike):
    absolute_filepath = Path(file).resolve()
    absolute_context = Path(context).resolve()
    image_name, image_tag = tag
    console.log(f"Building from {absolute_filepath} at {absolute_context}...")
    builder = Builder.from_file(absolute_filepath, image_name, image_tag)
    console.log("Running program...")
    builder.run_program()


@main.command
@click.argument("image_ref", type=click.STRING)
@click.option("--repo-url", "-r", help="repository url", type=click.STRING)
def push(image_ref: str, repo_url: str):
    console.log(f"Pushing image with tag {image_ref}...")
    distributor = Distributor(image_ref, repo_url)
    distributor.push()

@main.command
@click.argument("image_ref", type=click.STRING)
@click.option("--repo-url", "-r", help="repository url", type=click.STRING)
def pull(image_ref: str, repo_url: str):
    console.log(f"Pulling image with tag {image_ref}...")
    distributor = Distributor(image_ref, repo_url)
    distributor.pull()


@main.command
@click.option(
    "--runtime",
    "-r",
    help="runtime to use",
    type=click.Choice(["duckdb", "postgresql"]),
    default="duckdb",
)
@click.argument("image_ref", type=str)
def run(runtime: Literal["duckdb", "postgresql"], image_ref: str):
    console.log(f"Running image with tag {image_ref}...")
    conn = Runner(image_ref).run(runtime)
    console.log(conn)
