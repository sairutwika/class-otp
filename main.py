import streamlit as st
import smtplib
import random
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

# Title
st.title("🔒 Email OTP Verification")

# Initialize session state
if "otp" not in st.session_state:
    st.session_state.otp = None

# Email form
with st.form("otp_form"):
    user_email = st.text_input("ENTER THE EMAIL ADDRESS")
    send_clicked = st.form_submit_button("Send OTP")

    if send_clicked:
        if EMAIL is None or PASSWORD is None:
            st.error("EMAIL OR PASSWORD MISSING. Please check your .env file.")
        elif user_email == "":
            st.warning("PLEASE ENTER A VALID EMAIL ID")
        else:
            st.session_state.otp = random.randint(1111, 9999)
            body = f"OTP sent: {st.session_state.otp}"
            
            msg = MIMEMultipart()
            msg["From"] = EMAIL
            msg["To"] = user_email
            msg["Subject"] = "OTP for Verification"
            msg.attach(MIMEText(body, "plain"))

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(EMAIL, PASSWORD)
                server.send_message(msg)
                server.quit()

                st.success(f"OTP sent successfully to {user_email}")
            except Exception as e:
                st.error(f"Authentication failed: {e}")

# OTP verification
if st.session_state.otp:
    entered_otp = st.text_input("ENTER THE RECEIVED OTP")
    if st.button("Verify OTP"):
        try:
            if int(entered_otp) == st.session_state.otp:
                st.success("✅ Hurray! OTP matched successfully.")
                st.session_state.otp = None
            else:
                st.error("❌ Invalid OTP. Please try again.")
        except ValueError:
            st.warning("⚠️ Please enter a 4-digit number.")
