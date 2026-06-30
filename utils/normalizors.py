import pandas as pd
import re
from typing import Optional, List

from .main_vars import (
    EMAIL_REGEX,
    NULL_VALUES,
    TITLE_MAP,
    E164_REGEX
)

def safe_normalize(func, value, default):
    try:
        return func(value)
    except Exception:
        return default

def collapse_spaces(text):

    if text is None:
        return None

    return re.sub(r"\s+", " ", str(text)).strip()

def normalize_null(value: Optional[str]) -> Optional[str]:
    if pd.isna(value):
        return None
    
    if value is None:
        return None

    value = str(value).strip()

    if value.lower() in NULL_VALUES:
        return None

    return value

def normalize_name(name: Optional[str]) -> Optional[str]:
    name = normalize_null(name)

    if name is None:
        return None

    name = collapse_spaces(name)

    return name.title()

def normalize_email(email: Optional[str]) -> List[str]:
    email = normalize_null(email)

    if email is None:
        return []

    email = email.strip().lower()

    if EMAIL_REGEX.fullmatch(email):
        return [email]

    return []

def normalize_phone(phone: Optional[str]) -> List[str]:
    phone = normalize_null(phone)

    if phone is None:
        return []

    digits = re.sub(r"\D", "", phone)

    normalized_phone = None

    if len(digits) == 12 and digits.startswith("91"):
        normalized_phone = "+" + digits

    elif len(digits) == 10:
        normalized_phone = "+91" + digits

    elif phone.startswith("+"):
        normalized_phone = "+" + digits

    if normalized_phone and E164_REGEX.fullmatch(normalized_phone):
        return [normalized_phone]

    return []

def normalize_company(company: Optional[str]) -> Optional[str]:
    company = normalize_null(company)

    if company is None:
        return None

    company = collapse_spaces(company)

    if company.isupper() or company.istitle():
        return company

    return company.title()


def normalize_title(title: Optional[str]) -> Optional[str]:

    title = normalize_null(title)

    if title is None:
        return None

    title = collapse_spaces(title)

    cleaned_title = []
    for word in str(title).split():
        if word.lower() in TITLE_MAP:
            cleaned_title.append(TITLE_MAP[word.lower()])
        else:
            if set(word) == 'i': cleaned_title.append(word.upper())
            else: cleaned_title.append(word.title())

    return ' '.join(cleaned_title)