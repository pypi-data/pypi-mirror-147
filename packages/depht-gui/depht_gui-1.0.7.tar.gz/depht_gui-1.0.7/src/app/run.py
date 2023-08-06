"""Run the app."""
import sys

from signal import signal, SIGINT

from app.flask_app import create_app


def exit_handle(sig, frame):
    """Exit when CTRL+C is pressed."""
    sys.exit(0)


def main():
    """Run the app."""
    app = create_app()

    signal(SIGINT, exit_handle)

    app.run(debug=False, port=50000)


if __name__ == "__main__":
    main()
