import web

from server.database import connection
from server.database import models


def get_crawler_rule_by_name(rule_name):
    db = connection.get_db()
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
    db = connection.get_db()

    table_rs = db.where('sqlite_master', type='table', name='configuration')
    if list(table_rs):
      production_rs = db.where('configuration', key='production')
      for production_row in production_rs:
          if production_row.value == '0':
              return False
          else:
              return bool(production_row.value)

    return False


def get_tables_in_db():
    """Returns a list of the names of the tables in this database.
    
    NOTE: This function only works for the SQLite engine.
    """
    db = connection.get_db()
    tables = db.select('sqlite_master', what='name', where='type = "table"')
    return list(tables)
