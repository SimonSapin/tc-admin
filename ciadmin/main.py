# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import functools
import click
import asyncio

from .util import with_aiohttp_session
from . import generate
from . import current
from . import output
from . import diff
from . import apply


def run_async(fn):
    @functools.wraps(fn)
    def wrap(*args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(fn(*args, **kwargs))
        loop.close()
    return wrap


@click.group()
def main():
    'Manage runtime configuration for Firefox CI'


@main.command(name='generate')
@generate.options
@output.options
@run_async
@with_aiohttp_session
async def generateCommand(**kwargs):
    'Generate the the expected runtime configuration'
    output.display_resources(await generate.resources())


@main.command(name='current')
@generate.options
@output.options
@run_async
@with_aiohttp_session
async def currentCommand(**kwargs):
    'Fetch the current runtime configuration'
    # generate the expected resources so that we can limit the current
    # resources to only what we manage
    expected = await generate.resources()
    output.display_resources(await current.resources(expected.managed))


@main.command(name='diff')
@generate.options
@diff.options
@run_async
@with_aiohttp_session
async def diffCommand(**kwargs):
    'Compare the the current and expected runtime configuration'
    expected = await generate.resources()
    actual = await current.resources(expected.managed)
    diff.show_diff(expected, actual)


@main.command(name='apply')
@generate.options
@apply.options
@run_async
@with_aiohttp_session
async def applyCommand(**kwargs):
    'Compare the the current and expected runtime configuration'
    expected = await generate.resources()
    actual = await current.resources(expected.managed)
    await apply.apply_changes(expected, actual)