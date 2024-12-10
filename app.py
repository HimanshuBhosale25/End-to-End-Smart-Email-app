from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
import base64
import openai

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow CORS from the frontend running on localhost:5500
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Allow only the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth 2.0 credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Google OAuth 2.0 Endpoints
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
GMAIL_API_BASE = "https://www.googleapis.com/gmail/v1/users/me"

# Scopes for Gmail API access
SCOPES = "https://mail.google.com/"

# Temporary storage for tokens (replace with a secure database in production)
tokens = {}

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def home():
    """Redirects the user to Google's OAuth 2.0 consent screen."""
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = f"{AUTH_URL}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    return RedirectResponse(auth_url)

@app.get("/oauth2callback")
def oauth2callback(request: Request):
    """Handles the OAuth 2.0 callback and exchanges authorization code for tokens."""
    code = request.query_params.get("code")
    if not code:
        return {"error": "Authorization code not provided"}

    # Exchange the authorization code for tokens
    token_payload = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(TOKEN_URL, data=token_payload)
    if token_response.status_code != 200:
        return {"error": "Failed to retrieve tokens", "details": token_response.json()}

    global tokens
    tokens = token_response.json()

    # Redirect to the frontend running on localhost:5500
    return RedirectResponse(url="http://127.0.0.1:5500/index.html")

@app.get("/emails")
def fetch_emails():
    """Fetches the first 10 user's emails."""
    access_token = tokens.get("access_token")
    if not access_token:
        return {"error": "Access token not found. Please login first."}

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{GMAIL_API_BASE}/messages", headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to fetch emails", "details": response.json()}

    # Get the first 10 emails only
    messages = response.json().get("messages", [])[:10]
    emails = []

    # Loop through the message IDs and fetch the details for each one
    for message in messages:
        message_id = message["id"]
        message_details = fetch_email_details(message_id, headers)

        # Add the email details to the list
        emails.append(message_details)

    return {"emails": emails}

@app.get("/generate_response/{message_id}")
def generate_response(message_id: str):
    """Generate a response to the email."""
    access_token = tokens.get("access_token")
    if not access_token:
        return {"error": "Access token not found. Please login first."}

    headers = {"Authorization": f"Bearer {access_token}"}
    message_details = fetch_email_details(message_id, headers)

    generated_response = generate_response_from_openai(message_details["body"])
    return {"generated_response": generated_response}

@app.get("/summarize_email/{message_id}")
def summarize_email(message_id: str):
    """Summarize the email body."""
    access_token = tokens.get("access_token")
    if not access_token:
        return {"error": "Access token not found. Please login first."}

    headers = {"Authorization": f"Bearer {access_token}"}
    message_details = fetch_email_details(message_id, headers)

    summarized_email = summarize_email_body(message_details["body"])
    return {"summarized_email": summarized_email}

def fetch_email_details(message_id, headers):
    """Fetch detailed information for each email including sender, subject, and body."""
    url = f"{GMAIL_API_BASE}/messages/{message_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        email_data = response.json()
        email_details = {
            "id": message_id,
            "sender": extract_header_value(email_data, "From"),
            "subject": extract_header_value(email_data, "Subject"),
            "body": extract_email_body(email_data)
        }
        return email_details
    else:
        return {"error": "Failed to fetch email details", "status_code": response.status_code}

def extract_header_value(email_data, header_name):
    """Extract the value of a specific header from the email data."""
    headers = email_data.get("payload", {}).get("headers", [])
    for header in headers:
        if header["name"] == header_name:
            return header["value"]
    return "No " + header_name

def extract_email_body(email_data):
    """Extracts the body content of the email (text/plain or text/html)."""
    payload = email_data.get("payload", {})
    parts = payload.get("parts", [])
    
    # Check for body in 'text/plain' or 'text/html' format
    for part in parts:
        mime_type = part.get("mimeType")
        if mime_type == "text/plain" or mime_type == "text/html":
            body = part.get("body", {}).get("data", "")
            return decode_base64(body)
    return "No body content"

def decode_base64(encoded_str):
    """Decodes a base64 encoded string."""
    return base64.urlsafe_b64decode(encoded_str).decode("utf-8")

def generate_response_from_openai(email_body):
    """Generate a response to the email using OpenAI GPT."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # or gpt-3.5-turbo for a smaller model
            messages=[{"role": "system", "content": "You are an assistant."},
                      {"role": "user", "content": f"Respond to this email: {email_body}"}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating response: {str(e)}"

def summarize_email_body(email_body):
    """Summarize the email body using OpenAI GPT."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # or gpt-3.5-turbo for a smaller model
            messages=[{"role": "system", "content": "You are an assistant."},
                      {"role": "user", "content": f"Summarize this email: {email_body}"}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error summarizing email: {str(e)}"
