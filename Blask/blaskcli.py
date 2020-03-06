"""
Blask

Copyright (C) 2018  https://github.com/zerasul/blask

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
from os import makedirs, path, getcwd
from pkg_resources import get_distribution, DistributionNotFound
from pathlib import Path
import shutil

import click

from Blask import BlaskApp, blasksettings

LIB_DIR = Path(__file__).resolve().parents[0]


class CLIController:
    """
    Class that controls all the Command Line interface application
    """

    default_template_file = str(LIB_DIR / 'index_template.html')

    default_index = str(LIB_DIR / 'markdown_template.md')

    settings = str(LIB_DIR / 'default_env.env')

    not_found = str(LIB_DIR / 'default_404.md')

    def createdefaultindexfile(self, filepath):
        """
        create a new default index file.
        :param filepath: file path where the new index file is stored
        """
        shutil.copy(self.default_index, filepath)

    def createdefaulttemplatefile(self, filepath):
        """
        Create a new default template.
        :param filepath: file path where the new template file is stored.
        """
        shutil.copy(self.default_template_file, filepath)

    def createsettingsfile(self):
        """
        Create a new settings file
        """
        shutil.copy(self.settings, '.env')

    def createnotfoundpage(self, filepath):
        """
        Create a new page not found file.
        :param filepath: file path where the page not found is stored
        """
        shutil.copy(self.not_found, filepath)


blask = BlaskApp()
isdebug = False
cliController = CLIController()


@click.group()
def blaskcli():
    """
    Initialice the command Line Interface Objects.
    """
    try:
        version = get_distribution("Blask").version
    except DistributionNotFound:
        version = "test_version"
    click.echo("Blask (C) version %s" % version)


@blaskcli.command(help="Run the instance of blask")
@click.option("--debug", default=False, help="Init with de debug flag")
@click.option(
    "--port", default=5000, help="Port where the server is listening")
@click.option(
    "--host", default="127.0.0.1", help="Default Network interface listening")
def run(debug, port, host):
    """
    Run the current blask instance
    :param debug: initialice with debug options
    :param port: port where the port is opened
    """
    blask.run(debug=debug, port=port, host=host)


@blaskcli.command(help="Initialize a new Blask Project")
def init():
    """
    Inits a new Blask Instance; with the default options.
    """
    click.echo("Initializing new Blask Project")
    click.echo("Using default Settings")
    postdir = path.basename(
        path.dirname(str(blasksettings.DEFAULT_SETTINGS["postDir"] + "/")))
    templatedir = path.basename(
        path.dirname(str(blasksettings.DEFAULT_SETTINGS["templateDir"] + "/"))
    )
    try:
        makedirs(postdir)
        cliController.createdefaultindexfile(path.join(postdir, "index.md"))
        makedirs(templatedir)
        cliController.createdefaulttemplatefile(
            path.join(templatedir, "template.html"))
        cliController.createsettingsfile()
        cliController.createnotfoundpage(path.join(postdir, '404.md'))
        click.echo("Created new Blask project on %s" % getcwd())
        click.echo("Now you can execute: blaskcli run")
    except FileExistsError:
        click.echo("There is an existing Blask Project")


if __name__ == "__main__":
    blaskcli()
