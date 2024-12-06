import itertools
import json
import os
import tempfile

from torxtools import testtools

from .. import cli


def with_tmpdir(fn):
    def wrap(*args, **kwargs):
        with tempfile.TemporaryDirectory(prefix="nwn-dg-", ignore_cleanup_errors=True) as dirname:
            return fn(*args, tmpdir=dirname, **kwargs)

    return wrap


@with_tmpdir
def post(payload, tmpdir):
    if payload is None:
        payload = {}

    filename = f"{tmpdir}/output"

    # Convert everything to strings
    payload = {str(x): str(y) for x, y in payload.items()}

    # For all arguments, replace underscore with dash, then prepend '--'
    payload = {"--" + x.replace("_", "-"): y for x, y in payload.items()}

    # Remove everything that starts with --output, since we'll control that
    payload = {x: y for x, y in payload.items() if not x.startswith("--output-")}
    payload = {x: y for x, y in payload.items() if not x.startswith("--no-output-")}

    # Verify the arguments a first time
    try:
        argv = list(itertools.chain.from_iterable([[x, y] for x, y in payload.items()]))
        argv += ["--output-tile-json", filename]
        with testtools.disable_outputs():
            args = cli.options(argv)
    except SystemExit as err:
        if str(err) == "2":
            # err is the sys.exit code
            return {"error": {"code": 400, "message": "payload argument error"}}, 400
        # "err" is already prefixed with "error:"
        return {"error": {"code": 400, "message": f"payload argument {err}"}}, 400

    # If '--seed' is present, then check that it doesn't correspond to a file
    # so that seed from a known file on the server is not possible.
    if args.get("seed"):
        if os.path.exists(str(args.get("seed"))):
            return {"error": {"code": 400, "message": '"seed" parameter may not be a filename'}}, 400

    try:
        cli.main(argv)
    except SystemExit as err:
        return {"error": {"code": 400, "message": f"{err}"}}, 400

    with open(filename + ".tile.json", encoding="UTF-8") as fd:
        output = json.loads(fd.read())

    return output, 200
