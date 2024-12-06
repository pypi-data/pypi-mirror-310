# -*- coding: utf-8 -*-
# :Project:   package.qualified.name -- SA definition of table public.things
# :Created:   Sun 24 Nov 2024 11:57:53 CET
# :Author:    Lele Gaifax <lele@example.com>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2024 Lele Gaifax
#

import sqlalchemy as sa
from .. import meta, translatable_string as _


things = meta.TimeStampedTable('things', meta.metadata,
    #sa.Column('title', meta.text_t,
    #          nullable=False,
    #          info=dict(label=_('Title'),
    #                    hint=_('The title of the entry'))),
    schema='public')
