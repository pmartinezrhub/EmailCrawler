from termcolor import colored
import re
from email_validator import validate_email, EmailNotValidError

class EmailFinder():
    
    def __init__(self, raw_html):
        self.raw_html = raw_html

    def is_valid_email(self, email):
        if len(email) < 321:
            email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
            return re.match(email_regex, email) is not None
        return False

    def check_email_is_valid(self, mail_candidate):
        try:
            if not self.is_valid_email(mail_candidate):
                return False
            
            emailinfo = validate_email(mail_candidate, check_deliverability=False)
            email = emailinfo["email"]
            
            splited_email = email.split("@")
            last_part_email = splited_email[1].split(".")[-1]
            len_domain = len(last_part_email)
            
            if 1 < len_domain < 4:
                return True
            else:
                return False
        except EmailNotValidError as e:
            print(colored("[-] Invalid email: " + str(e) + " " + mail_candidate, "blue"))
            return False


    def search_emails(self):
        if self.raw_html is not None:
            emails = re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', self.raw_html)
            valid_emails = []
            
            for email in emails:
                if self.check_email_is_valid(email):
                    valid_emails.append(email)
                else:
                    print(colored("[-] Removing invalid email => " + email, "blue"))
            
            return valid_emails if valid_emails else None
        return None