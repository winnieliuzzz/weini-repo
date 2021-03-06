import datetime
import uuid
import requests
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item
import smtplib
from email.message import EmailMessage


class Alert:
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id = uuid.uuid4().hex if _id is None else _id
        self.active = active

    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item.name, self.price_limit)

    def send(self, gmail, password):
        email = EmailMessage()
        email['Subject'] = "Price for {0} is now ${1}".format(self.item.name, self.item.price)
        email['From'] = "WhaleofDeal"
        email['To'] = self.user_email
        content = "It's A Deal!\n {0}\n {1} \n To navigate to the alert, visit {2}".format(self.item.name, self.item.url, "https://whaleofdeal.herokuapp.com/alerts/{}".format(self._id))
        email.set_content(content)

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(gmail, password)

        s.send_message(email)
        s.quit()
        # return requests.post(
        #     AlertConstants.URL,
        #     auth=("api", AlertConstants.API_KEY),
        #     data={
        #         "from": AlertConstants.FROM,
        #         "to": self.user_email,
        #         "subject": "Price for {0} is now ${1}".format(self.item.name, self.item.price),
        #         "text": "It's A Deal!\n {0}\n {1} \n To navigate to the alert, visit {2}".format(
        #             self.item.name, self.item.url, "http://"+app.config['DOMAIN']+"/alerts/{}".format(self._id))
        #     }
        # )

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes = minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"last_checked":
                                                           {"$lte": last_updated_limit},
                                                       "active" : True
                                                       })]

    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.now()
        self.item.save_to_mongo()
        self.save_to_mongo()
        return self.item.price

    def send_email_if_price_reached(self, gmail, password):
        if self.item.price < self.price_limit:
            self.send(gmail, password)

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {'user_email': user_email})]

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {'_id': alert_id}))

    def deactivate(self):
        self.active = False
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.save_to_mongo()

    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {'_id': self._id})