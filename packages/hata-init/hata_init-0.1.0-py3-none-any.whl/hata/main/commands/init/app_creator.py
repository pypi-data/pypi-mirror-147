from textwrap import indent
import pathlib

from hata import KOKORO
from scarletio.http_client import HTTPClient
from typer import Exit, colors, echo, style

from .constants import optional_ignore, README_TEMPLATE, main_py
from .utils import ConfigType, config_key_map

n = '\n'

class AppCreator:
    def __init__(self, name, path, bot_names = None, plugin_folder = "plugin", config = ConfigType.ENV):
        self.name = name
        self.path = pathlib.Path(path)
        self.plugin_folder = plugin_folder # lazy path init
        self.config = config

        if not bot_names:
            self.bots = ["client"]
        else:
            self.bots = bot_names

        try:
            for i in self.bots:
                assert i.isidentifier(), i
        except AssertionError as err:
            echo(f"{style('Invalid bot name: ', fg=colors.BRIGHT_RED)}{err.args[0]}")
            raise Exit(code=1)

        self.ensure_paths() # plugin_folder inited

    def ensure_paths(self):
        if self.name != self.path.name:
            self.path /= self.name
            self.path.mkdir(parents=True, exist_ok=True)

        self.plugin_folder = self.path / self.plugin_folder
        self.plugin_folder.mkdir(exist_ok=True)

    def make_gitignore(self):
        echo("Creating .gitignore")
        async def req():
            async with HTTPClient(KOKORO) as session:
                async with session.get("https://www.toptal.com/developers/gitignore/api/python,linux,windows,macos") as resp:
                    return await resp.read()

        try:
            gitignore = KOKORO.run(req()).decode() # i disabled the linting in workspace i think
        except Exception:
            from .constants import fall_back_gitignore as gitignore
        finally:
            KOKORO.stop()

        content = gitignore + optional_ignore
        with (self.path / ".gitignore").open("w") as fp:
            fp.write(content)

    def make_readme(self):
        echo("Creating README.md")
        with (self.path / "README.md").open("w") as fp:
            fp.write(README_TEMPLATE.format(name=self.name))

    def make_main(self):
        echo("Generating main.py file")
        code = main_py(self, self.plugin_folder.name, self.main_imports(), self.main_clients())
        echo("Creating main.py")
        with (self.path / "main.py").open("w") as fp:
            fp.write(code)

    def main_imports(self):
        code = ["", ""]
        if self.config == ConfigType.ENV:
            code[0] = "import os"
        elif self.config == ConfigType.DOTENV:
            code[0] = "import os"
            code[1] = "from dotenv import load_dotenv\n\nload_dotenv()"
        elif self.config == ConfigType.JSON:
            code[0] = "import json"
            code[1] = """\nconfig = json.load((pathlib.Path(__file__).parent / "secret.json").open("r"))"""
        elif self.config == ConfigType.TOML:
            code[1] = "import toml"
        elif self.config == ConfigType.PYTHON:
            code[1] = "\nimport config"
        else:
            raise ValueError("Invalid config value provided!")
        return code

    def main_clients(self):
        code = ""

        for client in self.bots:
            code_list = [
                self.get_config_key(client, "token"),
                f"# client_id = {self.get_config_key(client, 'client_id')} # The account's id # reccommended for multiple bots",
                f"# secret = {self.get_config_key(client, 'secret')} # For ouath Api"
            ]
            code += f"\n{client} = Client({n + indent(n.join(code_list), ' ' * 4) + n})\n"

        return code

    def get_config_key(self, bot, key):
        if self.config == ConfigType.ENV or self.config == ConfigType.DOTENV:
            return f"os.getenv(\"{bot.upper()}_{config_key_map.get(key, key).upper()}\")"
        elif self.config == ConfigType.JSON or self.config == ConfigType.TOML:
            return f"config[\"{bot}\"].get(\"{key}\")"
        elif self.config == ConfigType.PYTHON:
            return f"getattr(config, \"{bot.upper()}_{config_key_map.get(key, key).upper()}\")"
        else:
            raise ValueError("Invalid config value provided!")