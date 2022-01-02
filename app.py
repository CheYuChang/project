import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,StickerSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "acne", "shopping","menu","cheek","chin","forehead","nose","solve","through","sure"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "acne",
            "conditions": "is_going_to_acne",
        },
        {
            "trigger": "advance",
            "source": "acne",
            "dest": "cheek",                        
            "conditions": "is_going_to_cheek",
        },
        {
            "trigger": "advance",
            "source": "acne",
            "dest": "chin",                        
            "conditions": "is_going_to_chin",
        },
        {
            "trigger": "advance",
            "source": "acne",
            "dest": "forehead",                        
            "conditions": "is_going_to_forehead",
        },
        {
            "trigger": "advance",
            "source": "acne",
            "dest": "nose",                        
            "conditions": "is_going_to_nose",
        },
        {
            "trigger": "advance",
            "source": "through",
            "dest": "solve",                        
            "conditions": "is_going_to_solve",
        },
        {
            "trigger": "advance",
            "source": "through",
            "dest": "menu",                        
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "sure",
            "dest": "shopping",
            "conditions": "is_going_to_shopping",
        },
        {
            "trigger": "advance",
            "source": "sure",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "go_back",
            "source": ["solve","shopping"],
            "dest": "user",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "sure",
            "conditions": "is_going_to_sure",
        },
        
        {"trigger": "advance", "source": ["acne", "shopping","menu","cheek","chin","forehead","nose","solve","through","sure"], "dest": "menu","conditions":"is_going_to_back"},
        {"trigger": "advance", "source": ["cheek","chin","forehead","nose"], "dest": "through","conditions":"is_going_to_through"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        #
        
        if response == False:
            sticker=StickerSendMessage(
                package_id='11537',
                sticker_id='52002744'
            )
            line_bot_api.reply_message(event.reply_token, sticker)

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)