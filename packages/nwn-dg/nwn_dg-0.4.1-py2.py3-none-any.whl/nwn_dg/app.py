import os
import sys


def main():
    os.execvp("uvicorn", ["uvicron", "nwn_dg.app:app"] + sys.argv[1:])


if __name__ == "__main__":
    main()
else:
    from connexion import FlaskApp

    app = FlaskApp(__name__)
    app.add_api("api/openapi.yml")
