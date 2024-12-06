from . import SingletonFactory

try:
    from elasticsearch import Elasticsearch

    __exists = True

except:
    __exists = False


class ElasticsearchSF(SingletonFactory["Elasticsearch"]):
    def _instantiate(self):
        if not __exists:
            raise ImportError("You don't have `elasticsearch` installed!")

        es = Elasticsearch(
            *self.args,
            **self.kwargs,
        )

        print("Instantiated Elasticsearch.", es)

        return es

    def _destroy(self):
        es = self.instance

        es.close()

        print("Elasticsearch destroyed.", es)

        return True
