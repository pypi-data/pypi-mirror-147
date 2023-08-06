import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__)))

import EventHub.SendEvents as SendEvents

def run(env_name, client_code, account_name, events_json):
    return SendEvents.send_events('order.create', env_name, client_code, account_name, events_json)


if len(sys.argv) > 0:
    print(SendEvents.run('order.create'))
    print('order.create events were sent.')




