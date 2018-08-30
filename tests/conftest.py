# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from ciadmin.generate.ciconfig import get


@pytest.fixture
def mock_ciconfig_file(mocker):
    '''
    Set a mock value for `get_ciconfig_file`.
    '''
    def mocker(filename, content):
        get._cache[filename] = content
    yield mocker
    get._cache.clear()


def pytest_addoption(parser):
    parser.addoption(
        "--skip-slow", action="store_true", default=False, help="skip slow tests"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--skip-slow"):
        skip_slow = pytest.mark.skip(reason="skipping slow tests")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
