fall_back_gitignore =  """

# Created by https://www.toptal.com/developers/gitignore/api/python,linux,windows,macos
# Edit at https://www.toptal.com/developers/gitignore?templates=python,linux,windows,macos

### Linux ###
*~

# temporary files which can be created if a process still has a handle open of a deleted file
.fuse_hidden*

# KDE directory preferences
.directory

# Linux trash folder which might appear on any partition or disk
.Trash-*

# .nfs files are created when an open file is removed but is still being accessed
.nfs*

### macOS ###
# General
.DS_Store
.AppleDouble
.LSOverride

# Icon must end with two \r
Icon


# Thumbnails
._*

# Files that might appear in the root of a volume
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
.com.apple.timemachine.donotpresent

# Directories potentially created on remote AFP share
.AppleDB
.AppleDesktop
Network Trash Folder
Temporary Items
.apdisk

### macOS Patch ###
# iCloud generated files
*.icloud

### Python ###
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

### Windows ###
# Windows thumbnail cache files
Thumbs.db
Thumbs.db:encryptable
ehthumbs.db
ehthumbs_vista.db

# Dump file
*.stackdump

# Folder config file
[Dd]esktop.ini

# Recycle Bin used on file shares
$RECYCLE.BIN/

# Windows Installer files
*.cab
*.msi
*.msix
*.msm
*.msp

# Windows shortcuts
*.lnk

# End of https://www.toptal.com/developers/gitignore/api/python,linux,windows,macos
"""

optional_ignore = """
# Optional Ignores

## Editor config folder ##

#.idea/
#.vs/
#.vscode/

# end of optional ignores
"""

README_TEMPLATE = """
# {name}

A hata app built with hata_init
"""
n = '\n'

def_vars = ("\n"
"def load_config():\n"
"    root = pathlib.Path(__file__).parent\n"
"    secret = root / \"secret.toml\"\n"
"    if secret.exists():\n"
"        return toml.load(secret)\n"
"    raise Exception(\"No valid toml configuaration file found\") from err\n"
"\n"
"config = load_config()\n"
)

def padding(content, top=1, bottom=1):
    return "" if content is None else f"{n*top}{content}{n*bottom}"

def main_py(app_creator, plugin_folder, imports=(None, None), clients=None):
    return f"""\"\"\"A discord API app made with Hata\"\"\"
import pathlib{
    padding(imports[0], bottom=0)}

from hata import Client, start_clients, wait_for_interruption
from hata.ext.extension_loader import EXTENSION_LOADER
{padding(imports[1], top=0)
}{def_vars if app_creator.config.name == "toml" else ""}{
clients
}
def add_default_vars(loader=EXTENSION_LOADER):
    # You may optimize this code
    loader.add_default_variables(**{{k: v for k, v in globals().items() if isinstance(v, Client)}})

def discover_extensions(loader=EXTENSION_LOADER):
    try:
        path = (pathlib.Path(__file__).parent / "{plugin_folder}").resolve(strict=True)
    except (FileNotFoundError, RuntimeError) as err:
        print("Cannot discover extension due to path resolution failure!")
        raise err from None

    loader.add(
        [f"{plugin_folder}.{{i.stem}}" for i in path.glob("./*.py")]
        + [f"{plugin_folder}.{{d.name}}" for d in path.iterdir() if d.is_dir()]
    )

def main():
    add_default_vars(EXTENSION_LOADER)
    discover_extensions(EXTENSION_LOADER)
    EXTENSION_LOADER.load_all()

    start_clients()

    try:
        wait_for_interruption()
    except KeyboardInterrupt:
        pass

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
"""
