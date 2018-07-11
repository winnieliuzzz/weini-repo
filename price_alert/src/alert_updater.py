from src.common.database import Database
from src.models.alerts.alert import Alert
from src.app import app

Database.initialize()
alerts_needing_update = Alert.find_needing_update()
gmail = app.config['GMAIL']
password = app.config['PASSWORD']

for alert in alerts_needing_update:
    alert.load_item_price()
    alert.send_email_if_price_reached(gmail, password)