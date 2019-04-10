"""
Form for logging the current Client in.
"""
from wtforms import validators, Form, HiddenField

from salsa import labels
from salsa.server.admin.forms.fields import BootstrapTextField, \
    BootstrapPasswordField


l = labels['fitbit']


class FitbitForm(Form):
    """
    Form for logging the current Client in.
    """
    hr = HiddenField()

    event = HiddenField()

    record = HiddenField()
