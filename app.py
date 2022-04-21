"""Example bot which execute python expression and returns a local execution environment which is enough to teach the concept"""

from flask import Flask, request, json

app = Flask(__name__)


@app.route('/', methods=['POST'])
def on_event():
    """Handles an event from Google Chat."""
    event = request.get_json()
    if event['type'] == 'ADDED_TO_SPACE':
        text = f"Thanks for adding me to {event['space']['displayName']}!"
    
    elif event['type'] == 'REMOVED_FROM_SPACE':
        text = f"Bye Bye,nice tille stay at {event['space']['displayName']}!"
    
    elif event['type'] == 'MESSAGE':
        if event['message']['text'].startswith('@python exec'):
            message = event['message']['text'].split('@python exec')
            cls = {}
            expr = message[1][1:]
            #exec(object, globals, locals)
            exec(str(expr),globals(),cls)
            text = f"```{cls}```"

    return json.jsonify({'text': text})
