import os
from flask import Flask, request, jsonify
from pdf_generator import generate_pdf
from datetime import datetime
import requests
from twilio.twiml.messaging_response import MessagingResponse


load_dotenv()
app = Flask(__name__)



# Twilio Auth - Needed to download media
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
grokurl=os.getenv('grokurl')

@app.route("/", methods=['GET'])
def home():
    return "WhatsApp PDF Generator Running!"

msglist=[]
@app.route("/incoming", methods=['POST','GET'])
def incoming_message():
    sender = request.form.get('From')
    msg_body = request.form.get('Body')
    media_url = request.form.get('MediaUrl0')
    print(msg_body)
    if msg_body=="pdf":
        pdf_path = generate_pdf(msglist)  # PDF saved to static folder
        pdf_url = f"{grokurl}{pdf_path}"  # Update ngrok URL here each time runnig grok

        response = MessagingResponse()
        response.message("Here is your PDF").media(f"{grokurl}static/output.pdf")
        msglist.clear()  # Reset for next session
        return str(response)

    msglist.append(msg_body)


    
    return "Done", 200

    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)