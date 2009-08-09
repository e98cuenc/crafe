from web import utils
# import crafe.database.properties


class CrawlerRules(utils.Storage):
    name = ''
    url_list_articles = []
    css_article = ''
    css_common_properties = ''
    qps = 0

# TODO: Check the values of the members
#    def __init__(**kw):
#        pass