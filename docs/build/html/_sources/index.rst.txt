.. TextTales documentation master file, created by
   sphinx-quickstart on Sat Aug 24 22:34:23 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TextTales documentation
=======================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   utils
   app

Application Modules
===================

.. automodule:: app.models.user_model
   :members:

.. automodule:: app.models.user_profile_model
   :members:

.. automodule:: app.api.auth_routes
   :members:


Utilities
=========

.. automodule:: validate_email
   :members:

.. automodule:: validate_password
   :members:
