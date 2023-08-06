# Copyright 2018 Databricks, Inc.
import re

VERSION = "0.0.6"


def is_release_version():
    return bool(re.match(r"^\d+\.\d+\.\d+$", VERSION))
