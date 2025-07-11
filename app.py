
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

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    company = data.get('company')
    phone = data.get('phone')

    pdf_path = create_pass_pdf(name, company)

    try:
        send_email_with_pass(email, pdf_path, name, company, phone)
        return jsonify({'message': 'Registration successful! Pass sent via email.'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'message': f'Failed to send email: {str(e)}'}), 500
def send_email_with_pass(recipient_email, pdf_path, name, company, phone):
    msg = EmailMessage()
    msg['Subject'] = 'Registration Confirmation – Grain Revolution Global Launch Event'
    msg['From'] = EMAIL_USER
    msg['To'] = recipient_email

    # Updated formal content
    msg.set_content(f"""\
Dear {name},

Greetings from APIT!

We are delighted to confirm your successful registration as a delegated participant for the upcoming Global Launch Event – “Grain Revolution”, scheduled to be held on August 23, 2025, at Hyderabad, India.

It is a great honor to welcome you to this historic occasion, where the world’s most advanced rice processing technologies will be unveiled. Your participation is highly valued, and we are confident that this event will be insightful and impactful for all industry stakeholders.

Should you require any assistance with travel, accommodation, or event-specific details, our coordination team is readily available to support you. Please feel free to reach out to us at 9845015791, and we’ll be glad to help.

We look forward to hosting you at Grain Revolution – a landmark moment in the future of rice processing.

Warm regards,  
Shashikumar Thimmaiah  
Managing Director & CEO  
APIT Machinery Pvt. Ltd.
""")

    # Attach the generated PDF pass
    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename='APIT-Digital-Pass.pdf')

    # Send using SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        print("Connecting to SMTP...")
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
        print(f"✅ Email successfully sent to {recipient_email}")





@app.route('/send-travel-plan', methods=['POST'])
def send_travel_plan():
    data = request.get_json()
    name = data.get("name")
    contact = data.get("contact")
    arrival_date = data.get('arrival_date')
    arrival_time = data.get('arrival_time') or "Not specified"
    departure_date = data.get('departure_date')
    departure_time = data.get('departure_time') or "Not specified"
    from_place = data.get('from_place')
    accompanying = data.get('accompanying')
    mode = data.get('mode')
    meal = data.get('meal')

    message = (
        "New Travel Plan Submission:\n\n"
        f"Name: {name}\n"
        f"Contact: {contact}\n"
        f"Date of Arrival: {arrival_date} at {arrival_time}\n"
        f"Date of Departure: {departure_date} at {departure_time}\n"
        f"Coming From: {from_place}\n"
        f"Persons Accompanying: {accompanying}\n"
        f"Mode of Travel: {mode}\n"
        f"Meal Preference: {meal}"
    )

    try:
        send_simple_email(EMAIL_USER, "New Travel Plan Submitted", message)
        return jsonify({'success': True})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

def send_simple_email(to_email, subject, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
        print(f"Email successfully sent to {to_email}")


if __name__ == '__main__':
    app.run(debug=False)
