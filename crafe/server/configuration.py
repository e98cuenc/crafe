# Configuration options for Crafe.
#
# TODO: Generate automatically this file, or move part of these variables
# to a permanent storage.

STATIC_CONTENT_VERSION = 1

# We can't use :memory: as DB_NAME_TEST because webpy automatically deletes
# all the Storage objects still alive at the end of a request, so in the
# next request the connection will need to be recreated to store the
# connection information in web.db._ctx. The :memory: database only remains
# available until the next connection, and it's thus unusable for tests,
# except if we recreate the entire DB at the beginning of each test.
DB_NAME_TEST = 'test.db'
DB_NAME_DEVELOPMENT = 'development.db'
DB_NAME_PRODUCTION = '/var/lib/crafe.db'
DB_NAME = DB_NAME_DEVELOPMENT
