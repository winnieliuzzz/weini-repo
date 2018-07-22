import uuid
from src.common.database import Database
import src.models.stores.constants as StoreConstants
import src.models.stores.errors as StoreErrors


class Store:
    def __init__(self, name, url_prefix, price_tag, price_query, img_query, img_src_tag, _id=None):
        self.name = name
        self.url_prefix = url_prefix
        self.price_tag = price_tag
        self.price_query = price_query
        self.img_query = img_query
        self.img_src_tag = img_src_tag
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Store {}>".format(self.name)

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "price_tag": self.price_tag,
            "price_query": self.price_query,
            "img_query": self.img_query,
            "img_src_tag": self.img_src_tag
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"_id":id}))

    def save_to_mongo(self):
        Database.update(StoreConstants.COLLECTION, {'_id': self._id}, self.json())

    @classmethod
    def get_by_name(cls, store_name):
        return cls(**Database.find_one(StoreConstants.COLLECTION, {"name": store_name}))

    @classmethod
    def get_by_url_prefix(cls, url_prefix):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {"url_prefix": {"$regex": '^{}'.format(url_prefix)}})]

    @classmethod
    def find_by_url(cls, url):
        store = None
        for i in range(len(url)+1):
            stores = cls.get_by_url_prefix(url[:i])
            if len(stores)==0:
                raise StoreErrors.StoreNotFoundException("The URL Prefix used to find the store didn't give us any results!")
            else:
                store = stores[0]
                if len(stores)==1:
                    return store
        return store


    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(StoreConstants.COLLECTION, {})]


    def delete(self):
        Database.remove(StoreConstants.COLLECTION, {'_id': self._id})
