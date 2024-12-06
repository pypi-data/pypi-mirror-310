from . import SingletonFactory

try:
    from pymongo import MongoClient

    __exists = True

except:
    __exists = False


class MongoSF(SingletonFactory["MongoClient"]):
    def _instantiate(self):
        if not __exists:
            raise ImportError("You don't have `pymongo` installed!")

        mongo = MongoClient(
            *self.args,
            **self.kwargs,
        )

        print("Instantiated MongoDB.", mongo)

        return mongo

    def _destroy(self):
        mongo = self.instance

        mongo.close()

        print("MongoDB destroyed.", mongo)

        return True
