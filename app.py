import os
from flask import Flask, request, jsonify, send_file
from pdf_generator import generate_pdf
from datetime import datetime
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
grokurl = os.getenv('grokurl')

msglist = []  # will store text and image paths as they come (to preserve order)

@app.route("/", methods=['GET','POST'])
def home():
    return "WhatsApp PDF Generator Running!"

@app.route("/incoming", methods=['POST', 'GET'])
def incoming_message():
    sender = request.form.get('From')
    msg_body = request.form.get('Body')
    num_media = int(request.form.get('NumMedia', 0))
    print("Twilio sent NumMedia:", num_media)
    print(f"Incoming message from: {sender}")
    print(f"Message body: {msg_body}")
    print(f"Number of media files: {num_media}")


    # If user sends "pdf", generate the PDF
    if msg_body.strip().lower() == "pdf":
        
        pdf_path = generate_pdf(msglist)

        response = MessagingResponse()
        response.message("Here is your PDF").media(f"{grokurl}static/output.pdf")
        msglist.clear()
        return str(response)

    # Append text if text message received
    
    if msg_body and msg_body.strip().lower() != "pdf":
        msglist.append({'type': 'text', 'content': msg_body})


    # Handle multiple media (image) files
    for i in range(num_media):
        media_url = request.form.get(f'MediaUrl{i}')
        content_type = request.form.get(f'MediaContentType{i}')
        print(f"Media {i}: URL = {media_url}")
        print(f"Media {i}: Content-Type = {content_type}")

        if content_type.startswith('image'):
            try:
                resp = requests.get(media_url, timeout=10)
                resp.raise_for_status()
                img_data = resp.content
            except Exception as e:
                print(f"Error downloading image: {e}")
                continue  # skip bad image

            img_path = f"static/image_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.jpg"
            with open(img_path, 'wb') as f:
                f.write(img_data)
            msglist.append({'type': 'image', 'path': img_path})
    for item in msglist:
        if item.get('type') == 'image':
            os.remove(item['path'])

    return "Done", 200

@app.route("/static/<path:filename>", methods=['GET'])
def serve_static(filename):
    return send_file(os.path.join("static", filename))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
