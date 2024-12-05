import typer
from tool_goto_window.main import switch_to_window

app = typer.Typer()
app.command()(switch_to_window)

if __name__ == "__main__":
    app()