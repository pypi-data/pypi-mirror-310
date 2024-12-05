import base64
import click


@click.group()
def cli():
    pass


@cli.group()
def ls():
    """List various Tableau resources"""


@ls.command()
def users():
    """List users"""
    click.echo("Listing users...")


@ls.command()
def groups():
    """List groups"""
    click.echo("Listing groups...")


@ls.command()
def workbooks():
    """List workbooks"""
    click.echo("Listing workbooks...")


@ls.command()
def datasources():
    """List datasources"""
    click.echo("Listing datasources...")


@ls.command()
def custom_views():
    """List custom views"""
    click.echo("Listing custom views...")


@ls.command()
def subscriptions():
    """List subscriptions"""
    click.echo("Listing subscriptions...")


@ls.command()
def favorites():
    """List favorites"""
    click.echo("Listing favorites...")


@ls.command()
def projects():
    """List projects"""
    click.echo("Listing projects...")


@cli.command()
@click.argument("string")
def encode(string):
    """Encode a string using Base64 encoding."""
    encoded_bytes = base64.b64encode(string.encode("utf-8"))
    encoded_str = encoded_bytes.decode("utf-8")
    click.echo(encoded_str)


@cli.command()
@click.argument("encoded_string")
def decode(encoded_string):
    """Decode a Base64 encoded string."""
    try:
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_str = decoded_bytes.decode("utf-8")
        click.echo(decoded_str)
    except UnicodeDecodeError as e:
        click.echo(f"Error decoding string: {e}")


if __name__ == "__main__":
    cli()
