from src.instance_connect import command
import typer

app = typer.Typer()

@app.command()
def connect():
    command()
    print("Connecting to instance")


def main():
    app()

if __name__ == "__main__":
    main()