import logging
import re

from bs4 import BeautifulSoup
from ..const import EMAIL_ATTR_BODY, EMAIL_ATTR_SUBJECT

_LOGGER = logging.getLogger(__name__)
ATTR_GLS_IT = 'gls_it'
EMAIL_DOMAIN_GLS_IT = 'gls.com'


def parse_gls_it(email):
    """Parse GLS IT tracking numbers."""
    tracking_numbers = []

    soup = BeautifulSoup(email[EMAIL_ATTR_BODY], 'html.parser')

    matches = re.findall(r'https?://www\.gls-italy\.com/tracktraceuser/[A-Z]{2}/\d+', email[EMAIL_ATTR_BODY])
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

    return tracking_numbers
