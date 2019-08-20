import secret_config

WSP = r'[ \t]'  # see 2.2.2. Structured Header Field Bodies
CRLF = r'(?:\r\n)'  # see 2.2.3. Long Header Fields
NO_WS_CTL = r'\x01-\x08\x0b\x0c\x0f-\x1f\x7f'  # see 3.2.1. Primitive Tokens
QUOTED_PAIR = r'(?:\\.)'  # see 3.2.2. Quoted characters
FWS = r'(?:(?:' + WSP + r'*' + CRLF + r')?' + WSP + r'+)'  # see 3.2.3. Folding white space and comments
CTEXT = r'[' + NO_WS_CTL + r'\x21-\x27\x2a-\x5b\x5d-\x7e]'  # see 3.2.3
CCONTENT = r'(?:' + CTEXT + r'|' + QUOTED_PAIR + r')'  # see 3.2.3 (NB: The RFC includes COMMENT here
# as well, but that would be circular.)
COMMENT = r'\((?:' + FWS + r'?' + CCONTENT + r')*' + FWS + r'?\)'  # see 3.2.3
CFWS = r'(?:' + FWS + r'?' + COMMENT + ')*(?:' + FWS + '?' + COMMENT + '|' + FWS + ')'  # see 3.2.3
ATEXT = r'[\w!#$%&\'\*\+\-/=\?\^`\{\|\}~]'  # see 3.2.4. Atom
ATOM = CFWS + r'?' + ATEXT + r'+' + CFWS + r'?'  # see 3.2.4
DOT_ATOM_TEXT = ATEXT + r'+(?:\.' + ATEXT + r'+)*'  # see 3.2.4
DOT_ATOM = CFWS + r'?' + DOT_ATOM_TEXT + CFWS + r'?'  # see 3.2.4
QTEXT = r'[' + NO_WS_CTL + r'\x21\x23-\x5b\x5d-\x7e]'  # see 3.2.5. Quoted strings
QCONTENT = r'(?:' + QTEXT + r'|' + QUOTED_PAIR + r')'  # see 3.2.5
QUOTED_STRING = CFWS + r'?' + r'"(?:' + FWS + r'?' + QCONTENT + r')*' + FWS + r'?' + r'"' + CFWS + r'?'
LOCAL_PART = r'(?:' + DOT_ATOM + r'|' + QUOTED_STRING + r')'  # see 3.4.1. Addr-spec specification
DTEXT = r'[' + NO_WS_CTL + r'\x21-\x5a\x5e-\x7e]'  # see 3.4.1
DCONTENT = r'(?:' + DTEXT + r'|' + QUOTED_PAIR + r')'  # see 3.4.1
DOMAIN_LITERAL = CFWS + r'?' + r'\[' + r'(?:' + FWS + r'?' + DCONTENT + r')*' + FWS + r'?\]' + CFWS + r'?'  # see 3.4.1
DOMAIN = r'(?:' + DOT_ATOM + r'|' + DOMAIN_LITERAL + r')'  # see 3.4.1
ADDR_SPEC = LOCAL_PART + r'@' + DOMAIN  # see 3.4.1

# A valid address will match exactly the 3.4.1 addr-spec.
VALID_ADDRESS_REGEXP = '^' + ADDR_SPEC + '$'


def is_valid_email(mail):
    """
    Return whether the email address has a valid format

    :param mail: the mail to check
    :type mail: str

    :return: True if it is valid
    :rtype: bool
    """
    import re
    pattern = re.compile(VALID_ADDRESS_REGEXP)
    return pattern.match(mail)


def send_html_mail(name, email, subject, body:str):
    import smtplib
    import ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    with open("utils/mail.html", encoding="utf-8") as file:
        html = file.read()

        html = html.replace("{{ name }}", name)
        html = html.replace("{{ body }}", body.replace("\n", "<br>").replace("\n", "&nbsp;&nbsp;&nbsp;&nbsp;"))

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = secret_config.mail_user
        message["To"] = email

        message.attach(MIMEText(html, "html"))

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(secret_config.mail_user, secret_config.mail_password)
            server.sendmail(
                secret_config.mail_user, email, message.as_string()
            )

        print("Sent mail to %s (%s)" % (name, email))
