import re
URL = "https://www.compass.com/agents/locations/district-of-columbia-dc/30522/"

RAW_HTML_FILE = "raw.html"
CLEANED_DATA_FILE = "cleaned_data.txt"


def extract_details(cleaned_text):
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        phone_pattern = r"\+?\d{1,3}?[-.\s]?\(?\d{2,3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"

        email = re.search(email_pattern, cleaned_text)
        phone = re.search(phone_pattern, cleaned_text)

        email = email.group() if email else ""
        phone = phone.group() if phone else ""

        name = cleaned_text.replace(email, "").replace(phone, "")
        name = re.sub(r"M[:\-]?", "", name).strip()

        return {
            "name": name,
            "email": email,
            "phone": phone
            }
