.. -*- coding: utf-8 -*-
.. :Project:   package.qualified.name -- Schema public
.. :Created:   Sun 24 Nov 2024 11:57:52 CET
.. :Author:    Lele Gaifax <lele@example.com>
.. :License:   GNU General Public License version 3 or later
.. :Copyright: © 2024 Lele Gaifax
..

===================
 Schema ``public``
===================

.. patchdb:script:: Schema public
   :description: Create schema ``public``
   :conditions: postgres
   :mimetype: text/x-postgresql

   CREATE SCHEMA public

.. patchdb:script:: Schema public grants
   :description: Permissions on the schema ``public``
   :conditions: postgres
   :mimetype: text/x-postgresql
   :depends: Schema public

   GRANT USAGE ON SCHEMA public TO public

.. toctree::
   :maxdepth: 1

   tables/index
   functions/index
