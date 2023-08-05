#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for `pycdsl.shell`"""

import pytest

from pycdsl.shell import CDSLShell

###############################################################################


@pytest.fixture(scope="package")
def cdsl_shell(default_path, installation_list):
    return CDSLShell(data_dir=default_path, dict_ids=installation_list)


###############################################################################
