# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 Graz University of Technology.
# Copyright (C) 2024 Shared RDM.
#
# invenio-override is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""invenio module for sharedRDM theme."""

from . import config
from .views import locked


class InvenioOverride(object):
    """invenio-override extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        # add index route rule
        # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.add_url_rule
        # app.add_url_rule("/", "index", index)
        self.init_config(app)
        app.register_error_handler(423, locked)
        app.extensions["invenio-override"] = self
        app.config["THEME_LOGO"] = app.config.get("OVERRIDE_LOGO")

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("INVENIO_OVERRIDE_") or k.startswith("OVERRIDE_"):
                app.config.setdefault(k, getattr(config, k))
