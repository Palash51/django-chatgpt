
from django.conf import settings
import ujson
from elasticsearch import Elasticsearch


class ESQuery:
    """
    Base class for generating and executing ES queries
    """

    def __init__(self, url_parts, q_attribts=None):
        
        self.__q = {}
        self.__url_parts = {}
        self.es_settings = settings.DATABASES.get('elasticsearch', {})

        if not self.es_settings:
            raise ValueError("Unable to find ES configs in setting")
        
        url_defauts = {
            "proto": "http",
            "hosts": settings.ELASTICSEARCH_DSL.get('default', {}).get('hosts'),
            "index": None,
            "doc_type": None,
            "method": "_search",
            "is_scroll": False,
            "scroll": "3m",
            "export": False,
            "_id": None,
            "body": None
        }

        for url_key, url_value in url_defauts.items():
            self.__url_parts[url_key] = url_parts.get(url_key, url_value)

        if q_attribts:
            self.set_q_attributs(q_attribts)

    
    def set_q_attributs(self, q_attribts):
        """set attributes"""
        if q_attribts.get("is_filtered"):
            self.__q = {
                "query": {"filtered": {"query": {"match_all": {}}, "filter": {}}} 
            }
        
        else:
            self.__q = {"query": {"match_all": []}}
            
    def set_source(self, fields):
        """set query source"""
        self.__q["_source"] = fields

    def set_size(self, size):
        """set size"""
        self.__q["size"] = size

    def set_query(self, q):
        """set query"""
        self.__q = q

    def execute(self, method="GET"):

        serial_q = ujson.dumps(self.__q)
        index = ""

        if self.__url_parts.get("index"):

            index = self.__url_parts["index"]
            if not index.startswith(self.es_settings["ENVIRONMENT"], 0):
                self.__url_parts["index"] = (
                    self.es_settings["ENVIRONMENT"] + "_" + self.__url_parts["index"]
                )
            index = self.__url_parts["index"]
        

        try:
            r = {}
            es = Elasticsearch(hosts=self.__url_parts["hosts"], timeout=45)

            if not es.ping():
                raise ValueError("Connection failed")

            if not self.__url_parts.get("is_scroll") and not es.indices.exists(
                index=self.__url_parts["index"]
            ):
                return {}

            if method.upper() == "GET":
                if self.__url_parts["method"] == "_count":
                    r = es.count(
                        index=self.__url_parts["index"],
                        doc_type=self.__url_parts["doc_type"],
                        body=serial_q,
                    )

                elif self.__url_parts["method"] == "_mapping":
                    r = es.indices.get_mapping(
                        self.__url_parts["index"], self.__url_parts["doc_type"]
                    )

                else:
                    r = es.get(
                        self.__url_parts["index"],
                        self.__url_parts["_id"],
                        doc_type=self.__url_parts["doc_type"],
                    )

            elif method.upper() == "POST":

                if self.__url_parts["method"] == "_search":

                    if self.__q.get("scroll_id"):
                        r = es.scroll(
                            scroll_id=self.__q["scroll_id"], scroll=self.__q["scroll"]
                        )

                    elif self.__url_parts.get("is_scroll"):
                        r = es.search(
                            index=self.__url_parts["index"],
                            doc_type=self.__url_parts["doc_type"],
                            body=serial_q,
                            scroll=self.__url_parts["scroll"],
                        )
                    else:
                        r = es.search(
                            index=self.__url_parts["index"],
                            doc_type=self.__url_parts["doc_type"],
                            body=serial_q,
                        )

                elif self.__url_parts["method"] == "_count":
                    r = es.count(
                        index=self.__url_parts["index"],
                        doc_type=self.__url_parts["doc_type"],
                        body=serial_q,
                    )

                elif self.__url_parts["method"] == "_bulk":
                    r = es.bulk(
                        self.__url_parts["body"],
                        index=self.__url_parts["index"],
                        doc_type=self.__url_parts["doc_type"],
                    )

                elif self.__url_parts["method"] == "_update":
                    r = es.update(
                        index=self.__url_parts["index"],
                        doc_type=self.__url_parts["doc_type"],
                        body=serial_q,
                    )

                elif self.__url_parts["method"] == "_delete_by_query":
                    r = es.delete_by_query(
                        self.__url_parts["index"],
                        serial_q,
                        doc_type=self.__url_parts["doc_type"],
                    )

                elif self.__url_parts["method"] == "_update_by_query":
                    r = es.update_by_query(
                        index=self.__url_parts["index"],
                        doc_type=self.__url_parts["doc_type"],
                        body=serial_q,
                    )

                elif self.__url_parts["method"] == "_insert":
                    r = es.index(
                        index=self.__url_parts["index"],
                        doc_type=self.__url_parts["doc_type"],
                        body=serial_q,
                        id=self.__url_parts["_id"],
                    )

            
            elif method.upper() == "PUT":
                if self.__url_parts["method"] == "_mapping":
                    r = es.indices.put_mapping(
                        self.__url_parts["doc_type"],
                        serial_q,
                        index=self.__url_parts["index"],
                    )
                else:
                    r = es.create(
                        index=self.__url_parts["index"],
                        doc_type=self.__url_parts["doc_type"],
                        id=self.__url_parts["_id"],
                        body=self.__url_parts["body"],
                    )
            elif method.upper() == "DELETE":
                r = es.delete(
                    index=self.__url_parts["index"],
                    doc_type=self.__url_parts["doc_type"],
                    id=self.__url_parts["_id"],
                )

            return r
        except Exception as e:
            self.logger.error(str(e))
            raise



def fetch_data():
    print(f"###### initailze ######")
    es_query = ESQuery(
        {
        "index": "test",
        "doc_type": None,
        "method": "_search"
        }
    )
    query = {}
    data = es_query.execute("GET")
