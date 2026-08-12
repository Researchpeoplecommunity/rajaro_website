"""Send admin notification emails for form submissions."""

import logging
import smtplib
from email.message import EmailMessage

from flask import current_app

logger = logging.getLogger(__name__)


def _mail_settings():
    return {
        "server": current_app.config.get("MAIL_SERVER", ""),
        "port": current_app.config.get("MAIL_PORT", 587),
        "username": current_app.config.get("MAIL_USERNAME", ""),
        "password": current_app.config.get("MAIL_PASSWORD", ""),
        "use_tls": current_app.config.get("MAIL_USE_TLS", True),
        "from_addr": current_app.config.get("MAIL_FROM", ""),
        "notify_to": current_app.config.get("NOTIFY_EMAIL", "contact@rajaro.com"),
    }


def send_form_notification(subject, lines):
    """Email form submission details to the admin inbox.

    `lines` is a list of (label, value) tuples. Submission still succeeds if mail is not configured.
    """
    cfg = _mail_settings()
    if not cfg["server"]:
        logger.info("MAIL_SERVER not set — skipping notification: %s", subject)
        return False

    body_parts = [f"{label}: {value or '—'}" for label, value in lines if label]
    body = "\n".join(body_parts)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = cfg["from_addr"] or cfg["username"] or "noreply@rajaro.com"
    msg["To"] = cfg["notify_to"]
    msg.set_content(body)

    try:
        with smtplib.SMTP(cfg["server"], cfg["port"], timeout=30) as smtp:
            if cfg["use_tls"]:
                smtp.starttls()
            if cfg["username"] and cfg["password"]:
                smtp.login(cfg["username"], cfg["password"])
            smtp.send_message(msg)
        logger.info("Notification sent: %s", subject)
        return True
    except Exception:
        logger.exception("Failed to send notification: %s", subject)
        return False
