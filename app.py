
from dotenv import load_dotenv
load_dotenv()
import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
from generate_pass import create_pass_pdf
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

print(f"Loaded EMAIL_USER: {EMAIL_USER}")
print("EMAIL_PASS is loaded:", bool(EMAIL_PASS))
@app.route('/')
def home():
    return "✅ Launch Event Backend is Running"
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    company = data.get('company')
    phone = data.get('phone')

    pdf_path = create_pass_pdf(name, company)

    try:
        send_email_with_pass(email, pdf_path, name)
        return jsonify({'message': 'Registration successful! Invitation has been emailed.'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'message': f'Failed to send email: {str(e)}'}), 500

def send_email_with_pass(recipient_email, pdf_path, name):
    msg = EmailMessage()
    msg['Subject'] = 'Registration Confirmation – Grain Revolution Global Launch Event'
    msg['From'] = EMAIL_USER
    msg['To'] = recipient_email

    msg.set_content(f"""Dear {name},

Greetings from APIT!

We are delighted to confirm your successful registration as a delegated participant for the upcoming Global Launch Event – “Grain Revolution”, scheduled to be held on August 23, 2025, at Hyderabad, India.

It is a great honor to welcome you to this historic occasion, where the world’s most advanced rice processing technologies will be unveiled. Your participation is highly valued, and we are confident that this event will be insightful and impactful for all industry stakeholders.

Should you require any assistance with travel, accommodation, or event-specific details, our coordination team is readily available to support you. Please feel free to reach out to us at 9606922348, and we’ll be glad to help.

We look forward to hosting you at Grain Revolution – a landmark moment in the future of rice processing.

Warm regards,  
Shashikumar Thimmaiah  
Managing Director & CEO  
APIT Machinery Pvt. Ltd.
""")

    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename='APIT-Digital-Pass.pdf')

    with smtplib.SMTP('smtp.office365.com', 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
        print(f"✅ Email sent to {recipient_email}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides this in env
    app.run(host="0.0.0.0", port=port)
