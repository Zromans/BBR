from elasticsearch_dsl import Document, Keyword, Text, Integer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])

class ProductDocument(Document):
    name = Text()
    description = Text()
    price = Integer()
    category = Keyword()

    class Index:
        name = 'products'

def search_products(query, filters=None):
    s = ProductDocument.search()
    s = s.query("multi_match", query=query, fields=['name', 'description'])
    if filters:
        for key, value in filters.items():
            s = s.filter("term", **{key: value})
    return s.execute()
