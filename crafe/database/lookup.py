import configuration
# import crafe.database.models
import logging
import models
import web


db = None
def connect_db():
    global db
    if not db:
        logging.info('Initializing %s' % configuration.DB_NAME)
        db = web.database(dbn='sqlite', db=configuration.DB_NAME)


def get_crawler_rule_by_name(rule_name):
    connect_db()
    rules_rs = db.where('crawler_rules', name=rule_name)
    rules = list(rules_rs)
    if not rules:
        return None
    # rule_name is a primary index, we should have no duplicates. So rules has
    # a length of 0 or 1
    assert(len(rules) == 1)
    return models.CrawlerRules(**rules[0])


def db_contains_production_data():
    """Returns true if this database contains production data.
    
    A database is said to contain production data if it contains the key
    'production' in the table 'configuration'. Use to token to prevent
    accidental deletion of this table in functions like update.init_test_data.
    """
    connect_db()
    production = False

    table_rs = db.where('sqlite_master', type='table', name='configuration')
    if list(table_rs):
      production_rs = db.where('configuration', key='production')
      production = len(list(production_rs)) > 0

    return bool(production)


def get_tables_in_db():
    """Returns a list of the names of the tables in this database.
    
    NOTE: This function only works for the SQLite engine.
    """
    connect_db()
    tables = db.select('sqlite_master', what='name', where='type = "table"')
    return tables
