import imp
import os

import yaml

from ..common.constants import HANDLER_MODEL_MANIFEST_FILE, MODEL_VERSION
from .utils import validate_model_manifest_file_exists

#TODO: reintroduce when we add support for version
# def get_model_version():
#     validate_model_manifest_file_exists()
#     return f'{MODEL_VERSION}'

# # use this only for getting value from manifest file
# def get_model_name():
#     validate_model_manifest_file_exists()
#     return _get_param('name')

def _get_param(field):
    with open(HANDLER_MODEL_MANIFEST_FILE, 'r') as file:
        contents = yaml.safe_load(file)
        value = contents[field]
        if (
            (value is None)
            or (not isinstance(value, str))
            or (not value.strip())
        ):
            click.echo(
                f'Please set a valid model {field} in {HANDLER_MODEL_MANIFEST_FILE}')
        return value
