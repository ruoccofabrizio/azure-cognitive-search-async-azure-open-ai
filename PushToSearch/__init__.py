import logging, json, datetime
import azure.functions as func
from sharedcode import helper

def main(msg: func.ServiceBusMessage):
    # helper.initialize()
    logging.info('Python ServiceBus queue trigger processed message: %s',
                 msg.get_body().decode('utf-8'))
    data = json.loads(msg.get_body().decode('utf-8'))

    # Push to Azure Cognitive Search
    result_code = helper.push_to_ACS(data)

    if result_code == 200:
        logging.info('Push to Azure Cognitive Search succeeded.')
    elif result_code in (404, 207):
        helper.send_to_queue(data, scheduled_enqueue_time_utc= datetime.datetime.utcnow() + datetime.timedelta(seconds=10))


