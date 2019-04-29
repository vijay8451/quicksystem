import click


def echo_success(msg):
    click.echo(click.style(msg, fg='green'))


def echo_error(msg):
    click.echo(click.style(msg, fg='red', reverse=True))


def echo_skip(msg):
    click.echo(click.style(msg, fg='cyan'))


def echo_normal(msg):
    click.echo(click.style(msg, fg='blue'))
