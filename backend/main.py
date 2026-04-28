import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# ── CORS
# This tells the backend to accept requests from your frontend.
# During development we allow all origins (*).
# When you deploy, we'll lock this to your actual domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# ── EMAIL CONFIG
# We read credentials from environment variables — never hardcode passwords.
SMTP_USER = os.environ.get("SMTP_USER")  # your Gmail address
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")  # your Gmail app password
TO_EMAIL = "mashaephantus2000@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465  # SSL port


def send_email(name: str, email: str, message: str) -> bool:
    """
    Builds and sends an email to your inbox.
    Returns True if successful, False if anything goes wrong.
    """
    subject = f"Portfolio enquiry from {name}"

    # The email body — plain and readable in any client
    body = f"""
New message from your portfolio contact form.

──────────────────────────────
Name    : {name}
Email   : {email}
──────────────────────────────

{message}

──────────────────────────────
Sent via ephantus.dev contact form
    """.strip()

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg["Reply-To"] = email  # hitting Reply in Gmail goes straight to the client
    msg.attach(MIMEText(body, "plain"))

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, TO_EMAIL, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


@app.post("/contact")
async def contact(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(default=""),
):
    """
    Receives the contact form submission and fires the email.
    """
    if not name or not email:
        return JSONResponse(
            status_code=400,
            content={"ok": False, "error": "Name and email are required."},
        )

    success = send_email(name, email, message)

    if success:
        return JSONResponse(content={"ok": True})
    else:
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": "Could not send email. Try again later."},
        )


@app.get("/health")
def health():
    """
    Simple check — visit /health in the browser to confirm the server is running.
    """
    return {"status": "online"}
