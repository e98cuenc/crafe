import csv
import logging
import web

from server import configuration
from server.database import connection
from server.database import lookup
from server.database import models


def init_db():
    db = connection.get_db()
    if lookup.db_contains_production_data():
        logging.warning('Cowardly refusing to whipe a production db.')
        return

    delete_all_tables()
    create_tables()
    fill_tables_with_testdata()

    
def create_tables():
    db = connection.get_db()
    db.query('CREATE TABLE "crawler_rules" ('
             '"name" TEXT PRIMARY KEY, '
             '"url_list_articles" BLOB, '
             '"css_article" TEXT, '
             '"css_common_properties" TEXT, '
             '"qps" REAL)')
    db.query('CREATE TABLE "configuration" ('
             '"key" TEXT PRIMARY KEY, '
             '"value" TEXT)')


def fill_tables_with_testdata():
    db = connection.get_db()
    db.insert('configuration', key='production', value=False)
    load_tables_from_csv()


def get_csv_filename_from_tablename(tablename):
    """Builds the filename of the file that contains the test data for a table.

    TODO: Return an absolute path.

    Args:
      tablename: (str) Name of the table that we want to import.
    """
    return 'testdata/%s.csv' % tablename


def load_tables_from_csv():
    db = connection.get_db()

    f = open(get_csv_filename_from_tablename('crawler_rules'), 'r')
    csv_reader = csv.DictReader(f)
    try:
        for d in csv_reader:
            insert_crawler_rule(models.CrawlerRules(d))
    finally:
        f.close()


def insert_crawler_rule(crawler_rule):
    db = connection.get_db()
    db.insert('crawler_rules', seqname=None, **crawler_rule)


def delete_all_tables():
    """Delete all the tables of the currently opened db.
    
    TODO: This function only deletes permanent tables, it should also delete
    temporary tables.
    """
    db = connection.get_db()
    tables = lookup.get_tables_in_db()
    for table in tables:
        # The commentted query gives the error:
        # sqlite3.OperationalError: near "?": syntax error
        # db.query('DROP TABLE $table_name', vars={'table_name': table.name})
        # TODO: Find out what's wrong with the previous line
        db.query('DROP TABLE %s' % table.name)
