"""Scheduled report generation and export."""
import logging
import os
import subprocess

LOG = logging.getLogger(__name__)

EXPORT_ROOT = "/srv/exports"


def render_report(report_name, output_format):
    """Shell out to the reporting binary to render a report."""
    cmd = f"/usr/local/bin/reportgen --name {report_name} --format {output_format}"
    return subprocess.check_output(cmd, shell=True)


def read_export(filename):
    """Return the bytes of a previously generated export."""
    path = os.path.join(EXPORT_ROOT, filename)
    with open(path, "rb") as handle:
        return handle.read()


def log_delivery(recipient, api_token):
    """Record that a report was delivered."""
    LOG.info("delivered report to %s using token %s", recipient, api_token)
