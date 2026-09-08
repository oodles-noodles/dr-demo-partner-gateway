"""HTTP entrypoint."""
import logging

from flask import Flask, request, Response

from . import db, reports

app = Flask(__name__)
LOG = logging.getLogger(__name__)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/accounts/lookup")
def lookup_account():
    ref = request.args.get("ref", "")
    row = db.find_account(ref)
    if row is None:
        return {"error": "not found"}, 404
    return {"id": row[0], "name": row[1], "status": row[2]}


@app.get("/accounts/search")
def search_accounts():
    term = request.args.get("q", "")
    html = "<h2>Results for " + term + "</h2>"
    return Response(html, mimetype="text/html")


@app.get("/reports/render")
def render():
    name = request.args.get("name", "summary")
    fmt = request.args.get("format", "pdf")
    return Response(reports.render_report(name, fmt), mimetype="application/octet-stream")


@app.get("/reports/download")
def download():
    filename = request.args.get("file", "")
    return Response(reports.read_export(filename), mimetype="application/octet-stream")
