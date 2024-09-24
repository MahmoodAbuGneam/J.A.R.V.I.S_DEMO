# jarvis_gmail_commands.py

import gmail_integration

def check_new_emails(creds, num_emails=5):
    emails = gmail_integration.get_recent_emails(creds, max_results=num_emails)
    if isinstance(emails, str):
        return emails  # This will be an error message
    
    response = f"You have {len(emails)} recent emails. Here's a summary:\n"
    for i, email in enumerate(emails, 1):
        response += f"{i}. From: {email.get('sender', 'Unknown')}\n"
        response += f"   Subject: {email.get('subject', 'No subject')}\n"
    
    return response

def read_email_content(creds, email_index):
    emails = gmail_integration.get_recent_emails(creds, max_results=email_index)
    if isinstance(emails, str):
        return emails  # This will be an error message
    
    if email_index > len(emails):
        return f"Sorry, I could only find {len(emails)} recent emails."
    
    email = emails[email_index - 1]
    response = f"Reading email from {email.get('sender', 'Unknown')}.\n"
    response += f"Subject: {email.get('subject', 'No subject')}\n"
    response += f"Content: {email.get('snippet', 'No content available')}"
    
    return response

def process_email_command(command, creds):
    if command == "check":
        return check_new_emails(creds)
    elif command.startswith("read"):
        try:
            email_index = int(command.split()[-1])
            return read_email_content(creds, email_index)
        except ValueError:
            return "Please specify which email you want me to read by number. For example, 'read 2'."
    else:
        return "I'm not sure what you want me to do with your emails. You can ask me to check your emails or read a specific email."