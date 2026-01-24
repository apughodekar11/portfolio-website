import json
import boto3
import os
import re
import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize SES client
ses = boto3.client('ses', region_name=os.environ.get('AWS_REGION', 'eu-west-1'))

# Configuration from environment variables
RECIPIENT_EMAIL = os.environ.get('RECIPIENT_EMAIL', 'your.email@example.com')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'noreply@yourdomain.com')
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', 'https://yourdomain.com').split(',')

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_input(body):
    """Validate form input"""
    errors = []
    
    # Required fields
    if not body.get('name') or len(body['name'].strip()) < 2:
        errors.append('Name is required (minimum 2 characters)')
    
    if not body.get('email') or not validate_email(body['email']):
        errors.append('Valid email is required')
    
    if not body.get('message') or len(body['message'].strip()) < 10:
        errors.append('Message is required (minimum 10 characters)')
    
    # Length limits (prevent abuse)
    if body.get('name') and len(body['name']) > 100:
        errors.append('Name is too long (max 100 characters)')
    
    if body.get('email') and len(body['email']) > 254:
        errors.append('Email is too long')
    
    if body.get('subject') and len(body['subject']) > 200:
        errors.append('Subject is too long (max 200 characters)')
    
    if body.get('message') and len(body['message']) > 5000:
        errors.append('Message is too long (max 5000 characters)')
    
    return errors

def sanitize_input(text):
    """Basic sanitization to prevent injection"""
    if not text:
        return ''
    # Remove any HTML tags
    clean = re.sub(r'<[^>]*>', '', str(text))
    return clean.strip()

def create_email_body(name, email, subject, message):
    """Create formatted email body"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #3b82f6, #22d3ee); color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f8f9fa; padding: 20px; border: 1px solid #e9ecef; }}
            .field {{ margin-bottom: 15px; }}
            .label {{ font-weight: bold; color: #555; }}
            .value {{ margin-top: 5px; padding: 10px; background: white; border-radius: 4px; border: 1px solid #ddd; }}
            .message-box {{ white-space: pre-wrap; }}
            .footer {{ font-size: 12px; color: #666; margin-top: 20px; padding-top: 15px; border-top: 1px solid #ddd; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2 style="margin: 0;">📬 New Contact Form Submission</h2>
            </div>
            <div class="content">
                <div class="field">
                    <div class="label">From:</div>
                    <div class="value">{sanitize_input(name)} &lt;{sanitize_input(email)}&gt;</div>
                </div>
                <div class="field">
                    <div class="label">Subject:</div>
                    <div class="value">{sanitize_input(subject) or '(No subject)'}</div>
                </div>
                <div class="field">
                    <div class="label">Message:</div>
                    <div class="value message-box">{sanitize_input(message)}</div>
                </div>
                <div class="footer">
                    <p>Received at: {timestamp}</p>
                    <p>Reply directly to this email to respond to {sanitize_input(name)}.</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
New Contact Form Submission
===========================

From: {sanitize_input(name)} <{sanitize_input(email)}>
Subject: {sanitize_input(subject) or '(No subject)'}

Message:
--------
{sanitize_input(message)}

---
Received at: {timestamp}
Reply directly to this email to respond.
    """
    
    return html_body, text_body

def send_email(name, email, subject, message):
    """Send email via SES"""
    html_body, text_body = create_email_body(name, email, subject, message)
    
    email_subject = f"Portfolio Contact: {sanitize_input(subject) or 'New Message'}"
    
    response = ses.send_email(
        Source=SENDER_EMAIL,
        Destination={
            'ToAddresses': [RECIPIENT_EMAIL]
        },
        Message={
            'Subject': {
                'Data': email_subject,
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': text_body,
                    'Charset': 'UTF-8'
                },
                'Html': {
                    'Data': html_body,
                    'Charset': 'UTF-8'
                }
            }
        },
        ReplyToAddresses=[sanitize_input(email)]
    )
    
    return response

def get_cors_headers(origin):
    """Get CORS headers based on origin"""
    # Check if origin is allowed
    if origin in ALLOWED_ORIGINS or '*' in ALLOWED_ORIGINS:
        allowed_origin = origin
    else:
        allowed_origin = ALLOWED_ORIGINS[0]  # Default to first allowed origin
    
    return {
        'Access-Control-Allow-Origin': allowed_origin,
        'Access-Control-Allow-Headers': 'Content-Type,X-Requested-With',
        'Access-Control-Allow-Methods': 'POST,OPTIONS',
        'Content-Type': 'application/json'
    }

def lambda_handler(event, context):
    """Main Lambda handler"""
    
    # Get origin for CORS
    headers = event.get('headers', {}) or {}
    origin = headers.get('origin') or headers.get('Origin', '')
    cors_headers = get_cors_headers(origin)
    
    # Handle preflight OPTIONS request
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': ''
        }
    
    try:
        # Parse request body
        body = event.get('body', '{}')
        if isinstance(body, str):
            body = json.loads(body)
        
        # Log incoming request (sanitized)
        logger.info(f"Contact form submission from: {body.get('email', 'unknown')}")
        
        # Validate input
        validation_errors = validate_input(body)
        if validation_errors:
            logger.warning(f"Validation failed: {validation_errors}")
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps({
                    'success': False,
                    'message': 'Validation failed',
                    'errors': validation_errors
                })
            }
        
        # Extract fields
        name = body['name']
        email = body['email']
        subject = body.get('subject', '')
        message = body['message']
        
        # Send email
        ses_response = send_email(name, email, subject, message)
        
        logger.info(f"Email sent successfully. MessageId: {ses_response['MessageId']}")
        
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({
                'success': True,
                'message': 'Thank you! Your message has been sent successfully.'
            })
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {str(e)}")
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'body': json.dumps({
                'success': False,
                'message': 'Invalid request format'
            })
        }
        
    except ses.exceptions.MessageRejected as e:
        logger.error(f"SES rejected message: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({
                'success': False,
                'message': 'Failed to send email. Please try again later.'
            })
        }
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({
                'success': False,
                'message': 'An unexpected error occurred. Please try again later.'
            })
        }
