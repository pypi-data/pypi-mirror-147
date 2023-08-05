# The torque app

This is the django app that should be deployed in a running django server.

Outside of installing the app, this should remain a black box.  The reason being
that none of the routes or uses for this should be accessed except
through the [Torque MediaWiki plugin](https://www.mediawiki.org/wiki/Extension:Torque).

For developers, look in the individual code files for details on the inner
workings.

See [INSTALL.md](https://code.librehq.com/ots/mediawiki/torque/-/blob/main/django-torque/INSTALL.md) for installation instructions.
