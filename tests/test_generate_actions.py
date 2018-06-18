# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

import attr
import pytest

from ciadmin.generate.actions import Action


@pytest.mark.asyncio
async def test_fetch_empty(ciconfig_get):
    ciconfig_get.fake_values['actions.yml'] = {}
    assert await Action.fetch_all() == []


@pytest.mark.asyncio
async def test_fetch_entry(ciconfig_get):
    ciconfig_get.fake_values['actions.yml'] = [
        {
            'trust_domain': 'gecko',
            'level': 1,
            'action_perm': 'generic',
            'groups': ['g1', 'g2'],
        }
    ]
    assert await Action.fetch_all() == [
        Action(trust_domain='gecko', level=1, action_perm='generic', groups=('g1', 'g2'))
    ]