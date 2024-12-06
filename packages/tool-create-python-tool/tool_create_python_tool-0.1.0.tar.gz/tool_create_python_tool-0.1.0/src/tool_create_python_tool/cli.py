import typer

from tool_create_python_tool.main import hello


app = typer.Typer()
app.command()(hello)


if __name__ == "__main__":
    app()