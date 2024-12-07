"""The fw_gear_persurfer_coreg package."""

from importlib.metadata import version
import logging

log = logging.getLogger(__name__)

try:
    __version__ = version(__package__)
except Exception as e:
    log.info("Failed with error:\n'%s'", e)
    pass
