# WhatsApp PDF Generator 📱📄

A serverless, storage-less PDF generator for WhatsApp messages built using **Python, Flask, and Twilio**. 

## ✨ Features

- Receive messages (text/images) via WhatsApp.
- Automatically generate a PDF from user messages.
- Send the generated PDF back to the user's WhatsApp chat.
- No backend storage — all data is transient, ensuring **better user data privacy**.
- Lightweight SaaS design.

## 🚀 Technologies Used

- Python 3.x
- Flask
- Twilio WhatsApp API
- FPDF (PDF Generation)
- Ngrok (for local testing)

## 📦 Project Structure

/whatsapppdfgen
│
├── app.py # Main Flask server
├── pdf_generator.py # PDF generation logic
├── requirements.txt # Python dependencies
├── static/ # Folder for temporary PDF generation (auto-generated)
└── README.md # This file



## ⚙️ Installation & Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/whatsapp-pdf-generator.git
    cd whatsapp-pdf-generator
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables (if any)** or hardcode for local testing:
    - TWILIO_ACCOUNT_SID
    - TWILIO_AUTH_TOKEN

4. **Run the app**:
    ```bash
    python app.py
    ```

5. **Expose localhost via Ngrok**:
    ```bash
    ngrok http 8080
    ```

6. **Configure Twilio WhatsApp Sandbox**:
    - Set Webhook URL to your Ngrok URL `/incoming`.

## ✅ Usage

- Send messages to your Twilio WhatsApp number.
- Type `"end"` to generate and receive the PDF in your chat.
- **No storage involved** — secure, temporary, user-side PDF delivery.

## 🔒 Security & Privacy

- **No storage backend** — all messages are processed in-memory.
- Generated PDF is delivered directly to user — nothing is permanently stored.
- Suitable for secure use cases.

## 📝 Future Enhancements

- Add image embedding in PDF.
- Multi-user session handling with expiration.
- Host on Render/Heroku for production.

## 🙏 Credits

- [Twilio](https://www.twilio.com/)
- [FPDF](https://pyfpdf.readthedocs.io/en/latest/)
- [Flask](https://flask.palletsprojects.com/)
