from flask import render_template, abort, redirect, url_for
from app.errorhandling import blp


@blp.app_errorhandler(403)
def permission_denied(e):
    return render_template('403.html'), 403