import streamlit as st
import smtplib
import random
import os
import time
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

# UI Configuration
st.set_page_config(page_title="Email OTP Verification 🔒", layout="centered")

# Custom CSS for UI Styling
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1350&q=80");
        background-size: cover;
        background-position: center;
    }

    /* Heading white and bold */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        font-weight: bold !important;
        text-align: center;
    }

    /* Form labels and input text - black */
    label, .stTextInput input, .stTextArea textarea,
    .stSelectbox div, .stForm span {
        color: black !important;
        font-weight: bold !important;
    }

    /* Inputs */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px;
        color: black !important;
    }

    /* Buttons */
    .stButton>button {
        background-color: #00b894;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
    }

    /* Alert messages */
    .stAlert {
        background-color: rgba(0, 0, 0, 0.6) !important;
        border-left: 5px solid white !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px;
    }

    .stAlert>div {
        padding: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Page Heading
st.markdown("<h1>🔐 OTP Email Verification</h1>", unsafe_allow_html=True)

# Session states
if "otp" not in st.session_state:
    st.session_state.otp = None
if "otp_sent_time" not in st.session_state:
    st.session_state.otp_sent_time = None
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False
if "email" not in st.session_state:
    st.session_state.email = ""

# Function to send OTP
def send_otp(user_email):
    otp = random.randint(1000, 9999)
    body = f"Your OTP is: {otp}\nThis OTP will expire in 3 minutes."

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = user_email
    msg["Subject"] = "OTP Verification"
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        st.session_state.otp = otp
        st.session_state.otp_sent_time = time.time()
        st.session_state.email_sent = True
        st.session_state.email = user_email
        st.success(f"✅ OTP sent to {user_email}")
    except Exception as e:
        st.error(f"❌ Failed to send OTP: {e}")

# OTP Form
with st.form("otp_form"):
    user_email = st.text_input("Enter your email address", placeholder="example@gmail.com")
    send_clicked = st.form_submit_button("Send OTP")

    if send_clicked:
        if EMAIL is None or PASSWORD is None:
            st.error("EMAIL or PASSWORD missing in .env file")
        elif not user_email:
            st.warning("Please enter a valid email")
        else:
            send_otp(user_email)

# Resend OTP
if st.session_state.email_sent:
    if st.button("🔁 Resend OTP"):
        send_otp(st.session_state.email)

# OTP Expiry Check
def is_otp_expired():
    if st.session_state.otp_sent_time:
        return time.time() - st.session_state.otp_sent_time > 180  # 3 minutes
    return True

# OTP Verification
if st.session_state.email_sent and st.session_state.otp:
    if is_otp_expired():
        st.error("⏰ OTP expired! Please resend OTP.")
    else:
        remaining = int(180 - (time.time() - st.session_state.otp_sent_time))
        st.info(f"⏳ OTP will expire in: {remaining} seconds")

        entered_otp = st.text_input("Enter the OTP received on email", max_chars=4)
        if st.button("✅ Verify OTP"):
            try:
                if int(entered_otp) == st.session_state.otp:
                    st.success("🎉 OTP Verified Successfully!")
                    st.balloons()
                    st.session_state.otp = None
                    st.session_state.email_sent = False
                else:
                    st.error("❌ Incorrect OTP. Please try again.")
            except ValueError:
                st.warning("⚠️ Please enter numeric OTP only.")
