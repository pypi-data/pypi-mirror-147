from .callback import callback

def make_app():
    from typer import Typer

    app = Typer(help="A hata app generator", invoke_without_command=True)
    app.command()(callback)
    return app

def __main__():
    app = make_app()
    from sys import argv
    app(args=argv[2:], prog_name="hata init")
