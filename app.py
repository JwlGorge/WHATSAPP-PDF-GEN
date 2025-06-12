import os
from flask import Flask, request, jsonify, send_file
from pdf_generator import generate_pdf
from datetime import datetime
import requests
from twilio.twiml.messaging_response import MessagingResponse
from requests.auth import HTTPBasicAuth
import gc


# Load environment variables from .env file


app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
grokurl = os.getenv('grokurl')

msglist = []  # will store text and image paths as they come (to preserve order)

@app.route("/", methods=['GET','POST'])
def home():
    return "WhatsApp PDF Generator Running!"
msglist = []  # Global message list
session_started = False  # Global session flag

@app.route("/incoming", methods=['POST', 'GET'])
def incoming_message():
    global msglist, session_started  # Explicit globals
    
    sender = request.form.get('From')
    msg_body = request.form.get('Body')
    num_media = int(request.form.get('NumMedia', 0))

    # Reset session if this is the first message of new session (not "pdf")
    if not session_started and msg_body.strip().lower() != "pdf":
        # Clean up any old images
        for item in msglist:
            if isinstance(item, dict) and item.get('type') == 'image':
                try:
                    os.remove(item['path'])
                except Exception as e:
                    print(f"Error deleting {item['path']}: {e}")
        msglist.clear()
        session_started = True  # Mark session as started

    # If user sends "pdf", generate the PDF
    if msg_body.strip().lower() == "pdf":
        pdf_path = generate_pdf(msglist)

        response = MessagingResponse()
        response.message("Here is your PDF").media(f"{grokurl}static/output.pdf")

        # After sending PDF, cleanup
        for item in msglist:
            if item.get('type') == 'image':
                try:
                    os.remove(item['path'])
                except Exception as e:
                    print(f"Error deleting {item['path']}: {e}")
        msglist.clear()
        session_started = False  # Reset for next session
        gc.collect()
        return str(response)

    # Append text if text message received
    if msg_body and msg_body.strip().lower() != "pdf":
        msglist.append({'type': 'text', 'content': msg_body})

    # Handle multiple media (image) files
    for i in range(num_media):
        media_url = request.form.get(f'MediaUrl{i}')
        content_type = request.form.get(f'MediaContentType{i}')

        if content_type.startswith('image'):
            try:
                resp = requests.get(
                    media_url,
                    auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
                    timeout=10
                )
                resp.raise_for_status()
                img_data = resp.content
            except Exception as e:
                print(f"Error downloading image: {e}")
                continue  # skip this image if error occurs

            img_path = f"static/image_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.jpg"
            with open(img_path, 'wb') as f:
                f.write(img_data)
            msglist.append({'type': 'image', 'path': img_path})

    return "Done", 200


@app.route("/static/<path:filename>", methods=['GET'])
def serve_static(filename):
    return send_file(os.path.join("static", filename))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
