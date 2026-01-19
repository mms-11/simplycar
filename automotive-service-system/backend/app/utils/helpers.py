def calculate_total_cost(labor_cost, parts_cost):
    return labor_cost + parts_cost

def format_phone_number(phone_number):
    if len(phone_number) == 10:
        return f"({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}"
    return phone_number

def validate_email(email):
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def generate_appointment_id():
    import uuid
    return str(uuid.uuid4())