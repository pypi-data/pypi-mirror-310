import click

from config_kit import version_info, DEFAULT_SECTION, DEFAULT_CONFIG_FILE
from config_kit.core import ConfigKit


CONTEXT_SETTINGS = dict(help_option_names=['-?', '-h', '--help'])

@click.group(
    name=version_info['prog'],
    help=click.style(version_info['desc'], italic=True, fg='cyan', bold=True),
    context_settings=CONTEXT_SETTINGS,
    no_args_is_help=True,
)
@click.option('-c', '--config-file', help='Path to config file', default=DEFAULT_CONFIG_FILE, show_default=True)
@click.option('-s', '--section', help='Section to use', default=DEFAULT_SECTION, show_default=True)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
@click.pass_context
def cli(ctx, **kwargs):
    config = ConfigKit(**kwargs)
    ctx.obj = config


@cli.command(
    help='set a key-value pair'
)
@click.argument('key')
@click.argument('value')
@click.pass_context
def set(ctx, key, value):
    config = ctx.obj
    config.set(key, value)
    config.save()


@cli.command(
    help='get the value of a key'
)
@click.argument('key')
@click.pass_context
def get(ctx, key):
    config = ctx.obj
    click.echo(config.get(key))


@cli.command(
    help='remove a key from the config file'
)
@click.argument('key')
@click.pass_context
def remove(ctx, key):
    config = ctx.obj
    config.remove(key)
    config.save()


@cli.command(
    help='show the config file'
)
@click.pass_context
@click.option('-a', '--all-sections', help='Show all sections', is_flag=True)
def show(ctx, all_sections):
    config = ctx.obj
    config_file = config.config_file
    click.echo(f'Config file: {config_file}')
    if not config_file.exists():
        click.echo('Config file does not exist')
        return
    
    sections = config.config.sections() if all_sections else [config.section]
    for section in sections:
        click.echo(f'Section: {section}')
        for key, value in config.config.items(section):
            click.echo(f'  {key} = {value}')


def main():
    cli()


if __name__ == '__main__':
    main()
