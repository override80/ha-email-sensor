import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY, EMAIL_ATTR_SUBJECT, USPS_TRACKING_NUMBER_REGEX, UPS_TRACKING_NUMBER_REGEX, FEDEX_TRACKING_NUMBER_REGEX

_LOGGER = logging.getLogger(__name__)
ATTR_GENERIC = 'generic'
EMAIL_DOMAIN_GENERIC = ''

def parse_generic(email):
    """Tries to parse tracking numbers for any type of email."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')

    matches = re.findall(UPS_TRACKING_NUMBER_REGEX, email[EMAIL_ATTR_BODY])
    for tracking_number in matches:
        if tracking_number not in tracking_numbers:
            tracking_numbers.append(tracking_number)

    matches = re.findall(USPS_TRACKING_NUMBER_REGEX, email[EMAIL_ATTR_BODY])
    for tracking_number in matches:
        if tracking_number not in tracking_numbers:
            tracking_numbers.append(tracking_number)

    pattern = r"^GLS Italy - Notifica spedizione ([A-Z]{2}) (\d{9})$"
    match = re.match(pattern, email[EMAIL_ATTR_SUBJECT])
    if match:
        caps, number = match.groups()
        tracking_numbers.append({
          'link': f"https://www.gls-italy.com/tracktraceuser/{caps}/{number}",
          'tracking_number': f"{caps} {number}"
        })

    # matches = re.findall(FEDEX_TRACKING_NUMBER_REGEX, email[EMAIL_ATTR_BODY])
    # for tracking_number in matches:
    #     if tracking_number not in tracking_numbers:
    #         tracking_numbers.append(tracking_number)

    return tracking_numbers
