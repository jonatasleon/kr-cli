import os

import click
from tabulate import tabulate

from kr.consoles import list_consoles

from .download import download, retrieve_file_url
from .search import search, verify_console_name


def validate_console(ctx, param, value):
    try:
        console_code = verify_console_name(value)
    except KeyError:
        raise click.BadParameter(f"Console {value} is not available.")
    return console_code


def validate_query(ctx, param, value):
    return value or ("",)


order_by_choices = click.Choice(
    [
        "title",
        "genre",
        "rating",
        "downloads",
        "size",
    ]
)


def validate_order_by(ctx, param, value):
    replace_mapper = {
        "title": "file_name",
        "size": "file_size",
    }

    return replace_mapper.get(value, value)


def validate_urls(ctx, param, value):
    if not value and not click.get_text_stream("stdin").isatty():
        return tuple(click.get_text_stream("stdin").read().strip().split("\n")) or ("",)
    else:
        return value

def aria_download(urls, output_dir):
    dl_urls = []
    for url in urls:
        file_url = retrieve_file_url(url)
        if file_url[-2:] == '7z' or file_url[-2:] == '7Z':
            flag = click.prompt("File: " + file_url.split('/')[-1] + "\n7z detected! Press Z to include")
            if flag == "Z" or flag == "z":
                dl_urls.append(file_url)
        else:
            dl_urls.append(file_url)

    if len(dl_urls) != 0:
            click.echo("\nDownload Starting:")
    for x in dl_urls:
        click.echo(x.split('/')[-1])
        arg = ["aria2c","-s16","-x16","--dir",".\\","-Z"]
        arg.extend(dl_urls)
        subprocess.run(arg)

def defualt_download(urls, output_dir):
    for url in urls:
        file_url = retrieve_file_url(url)
        click.echo(file_url)
        chunks = download(file_url, output_dir=output_dir)
        with click.progressbar(length=next(chunks)) as bar:
            for size in chunks:
                bar.update(size)

@click.group()
def cli():
    pass


@cli.command("consoles")
def _consoles():
    """List available consoles to search and download from."""
    click.echo("\n".join(list_consoles()))


@cli.command("search")
@click.argument("console", callback=validate_console)
@click.argument("query", nargs=-1, type=click.UNPROCESSED, callback=validate_query)
@click.option(
    "--quiet",
    "-q",
    type=bool,
    default=False,
    is_flag=True,
    help="Only print link output",
)
@click.option(
    "--order-by",
    "-o",
    type=order_by_choices,
    default="downloads",
    callback=validate_order_by,
    help="Defines criteria order",
)
@click.option(
    "--asc/--desc",
    "-a/-d",
    "ascending",
    default=False,
    help="Defines ascending or descending order",
)
@click.option(
    "--page",
    "-p",
    type=int,
    default=1,
    callback=lambda ctx, param, value: value - 1,
    help="Page number",
    show_default=True,
)
def _search(console, query, quiet, order_by, ascending, page):
    """Search roms."""
    for q in query:
        result = search(console, q, order_by=order_by, asc=ascending, page=page)
        if quiet:
            output = "\n".join([r["link"] for r in result])
        else:
            output = tabulate(result, headers="keys")
        click.echo(output)


@cli.command("download")
@click.argument(
    "urls", nargs=-1, type=click.UNPROCESSED, required=False, callback=validate_urls
)
@click.option("--output_dir", "-d", default=os.path.abspath("."))
def _download(urls, output_dir):
    """Download roms."""
    command = ["aria2c", "--version"]
    try:
        # Try to execute the command and capture the return code
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        if result.returncode == 0:
            print("aria2c requirement is satisfied")
            aria_download(urls, output_dir)
        else:
            print("aria2c is not installed")
            defualt_download(urls, output_dir)
    except subprocess.CalledProcessError:
        print("aria2c is not installed")
        defualt_download(urls, output_dir)
    except FileNotFoundError:
        print("aria2c is not installed")
        defualt_download(urls, output_dir)
