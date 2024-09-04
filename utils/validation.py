"""
Validation utility module.

This module provides functions for validating email addresses and passwords. It supports basic format validation
using a regular expression, advanced validation with the `email-validator` library, and optional
MX record validation to check if the domain can receive emails.

Functions:
    - is_valid_format(email): Validates the format of an email address using a regular expression.
    - get_mx_records(domain): Retrieves the MX records for a given domain.
    - validate_email_address(email, check_mx=True, debug=False): Validates an email address, with
      options for MX record checking and debug logging.
"""

import logging
import re

import dns.resolver
from dns.exception import DNSException
from email_validator import EmailNotValidError
from email_validator import validate_email as email_validator

# Constants
MX_DNS_CACHE = {}

# Regular expression for email format validation
EMAIL_REGEX = (
    r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)"
    r"*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
    r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
)

# Set up logging
logger = logging.getLogger("email_validation")
logger.setLevel(logging.DEBUG)


def is_valid_format(email):
    """
    Check if the email format is valid using a regular expression.

    Args:
    ----
        email (str): The email address to validate.

    Returns:
    -------
        bool: True if the email format is valid, False otherwise.

    """
    return re.match(EMAIL_REGEX, email) is not None


def get_mx_records(domain):
    """
    Fetch the MX records for the given domain.

    This function retrieves the Mail Exchange (MX) records for the specified domain using DNS queries.
    The results are cached to reduce the number of DNS lookups for the same domain.

    Args:
    ----
        domain (str): The domain part of an email address.

    Returns:
    -------
        list: A list of tuples containing MX records (exchange, preference) if found, otherwise None.

    """
    if domain in MX_DNS_CACHE:
        return MX_DNS_CACHE[domain]

    try:
        answers = dns.resolver.resolve(domain, "MX")
        mx_records = [(r.exchange.to_text(), r.preference) for r in answers]
        MX_DNS_CACHE[domain] = mx_records
        return mx_records
    except DNSException as e:
        logger.debug("DNSException: %s", e)
        MX_DNS_CACHE[domain] = None
        return None


def validate_email_address(email, check_mx=True, debug=False):
    """
    Validate the email address with options for MX validation and debug logging.

    This function validates an email address by checking its format and optionally verifying that
    the domain has valid MX records. It also performs advanced validation using the `email-validator`
    library, which checks for issues like invalid characters and incorrect structure.

    Args:
    ----
        email (str): The email address to validate.
        check_mx (bool): If True, perform MX record validation to ensure the domain can receive emails (default is True).
        debug (bool): If True, enables debug logging (default is False).

    Returns:
    -------
        bool: True if the email address is valid and, if `check_mx` is True, has valid MX records.
              False if the email format is invalid or if MX records are required and not found.

    """
    if debug:
        logging.basicConfig()

    try:
        # Valid format check
        if not is_valid_format(email):
            return False

        # Advanced validation with the email-validator library
        email_validator(email)

        # Check MX records if required
        if check_mx:
            domain = email.split("@")[1]
            if not get_mx_records(domain):
                return False

        return True

    except EmailNotValidError as e:
        logger.debug("EmailNotValidError: %s", e)
        return False


def validate_password(password):
    """
    Validate a password to ensure it meets specific security criteria.

    The password must:
        - Be at least 8 characters long.
        - Not be more than 20 characters long.
        - Contain at least one digit.
        - Contain at least one uppercase letter.
        - Contain at least one lowercase letter.
        - Contain at least one special symbol from the following: !, @, #, $, %, ^, &, *, -

    Args:
    ----
        password (str): The password string to validate.

    Returns:
    -------
        bool: True if the password meets all the requirements, False otherwise.
        list: A list of error messages indicating which requirements were not met.

    """
    errors = []
    special_sym = ["!", "@", "#", "$", "%", "^", "&", "*", "-"]
    val = True

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
        val = False
    if len(password) > 20:
        errors.append("Password should not be more than 20 characters long")
        val = False

    # Check if password contains at least one digit, uppercase letter, lowercase letter, and special symbol
    has_digit = False
    has_upper = False
    has_lower = False
    has_symbol = False

    # Check the characters in the password using ASCII
    for char in password:
        if 48 <= ord(char) <= 57:
            has_digit = True
        elif 65 <= ord(char) <= 90:
            has_upper = True
        elif 97 <= ord(char) <= 122:
            has_lower = True
        elif char in special_sym:
            has_symbol = True

    if not has_digit:
        errors.append("Password must contain at least one digit")
        val = False
    if not has_upper:
        errors.append("Password must contain at least one uppercase letter")
        val = False
    if not has_lower:
        errors.append("Password must contain at least one lowercase letter")
        val = False
    if not has_symbol:
        errors.append("Password must contain at least one special symbol")
        val = False

    return val, errors
