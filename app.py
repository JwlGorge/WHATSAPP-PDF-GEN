import os
from flask import Flask, request, jsonify, send_file
from pdf_generator import generate_pdf_with_images
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


    # If user sends "pdf", generate the PDF
    if msg_body.strip().lower() == "pdf":
        texts = [item for item in msglist if isinstance(item, str)]
        images = [item for item in msglist if isinstance(item, dict) and item['type'] == 'image']

        image_paths = [img['path'] for img in images]
        pdf_path = generate_pdf_with_images(texts, image_paths)

        response = MessagingResponse()
        response.message("Here is your PDF").media(f"{grokurl}static/output.pdf")
        msglist.clear()
        return str(response)

    # Append text if text message received
    if msg_body and msg_body.strip().lower() != "pdf":
        msglist.append(msg_body)

    # Handle multiple media (image) files
    for i in range(num_media):
        media_url = request.form.get(f'MediaUrl{i}')
        content_type = request.form.get(f'MediaContentType{i}')

        if content_type.startswith('image'):
            img_data = requests.get(media_url).content
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
