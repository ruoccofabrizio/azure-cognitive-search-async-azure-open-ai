import logging, json
import azure.functions as func
from sharedcode import helper
import traceback

# Get logging options:
logger = logging.getLogger(__name__)

def main(msg: func.ServiceBusMessage):
    # helper.initialize()

    # Get the message body
    body = json.loads(msg.get_body().decode('utf-8'))

    data = {
        'metadata_storage_path': body['metadata_storage_path'],
        'output' : []
    }
    
    result = helper.get_openai_response(text = body['text'])
    logging.info(result)

    try:
        data['output'] = json.loads(result)
        if data['output'].get('results', None) is not None:
            data['output'] = data['output']['results']
    except Exception as e:
        logging.error(traceback.format_exc())
    
    helper.send_to_queue(data)
    logging.info(data['output'])
