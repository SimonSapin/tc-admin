# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import click

from .options import decorate, with_click_options


def options(fn):
    return decorate(
        fn,
        click.option('--text/--json', default=True, help='output format'),
        click.option('--grep', help='regular expression limiting resources displayed'))


@with_click_options('text', 'grep')
def display_resources(resources, text, grep):
    if grep:
        resources = resources.filter(grep)
    if text:
        print(resources)
    else:
        print(repr(resources))