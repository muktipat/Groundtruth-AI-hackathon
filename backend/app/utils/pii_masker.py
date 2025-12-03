"""PII masking utility for privacy protection."""
import re
from typing import Tuple


class PIIMasker:
    """Handles PII detection and masking."""
    
    # Patterns for different PII types
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    PHONE_PATTERN = r'\b(?:\+?1[-.\s]?)?\(?(?:\d{3})\)?[-.\s]?(?:\d{3})[-.\s]?(?:\d{4})\b'
    SSN_PATTERN = r'\b(?:\d{3}[-]?\d{2}[-]?\d{4})\b'
    CREDIT_CARD_PATTERN = r'\b(?:\d{4}[-\s]?){3}\d{4}\b'
    
    @staticmethod
    def mask_email(email: str) -> str:
        """Mask email address."""
        if '@' in email:
            name, domain = email.split('@')
            masked_name = name[0] + '*' * (len(name) - 2) + name[-1] if len(name) > 2 else '*'
            return f"{masked_name}@{domain}"
        return "[EMAIL]"
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """Mask phone number."""
        # Keep last 4 digits
        digits_only = re.sub(r'\D', '', phone)
        if len(digits_only) >= 4:
            return "***-***-" + digits_only[-4:]
        return "[PHONE]"
    
    @staticmethod
    def mask_ssn(ssn: str) -> str:
        """Mask SSN."""
        return "***-**-" + ssn[-4:]
    
    @staticmethod
    def mask_credit_card(cc: str) -> str:
        """Mask credit card number."""
        digits_only = re.sub(r'\D', '', cc)
        if len(digits_only) >= 4:
            return "**** **** **** " + digits_only[-4:]
        return "[CARD]"
    
    @classmethod
    def mask_text(cls, text: str) -> Tuple[str, dict]:
        """
        Mask all PII in text.
        
        Returns:
            Tuple of (masked_text, pii_locations)
        """
        masked_text = text
        pii_found = {}
        
        # Mask emails
        emails = re.findall(cls.EMAIL_PATTERN, text)
        for email in emails:
            masked_email = cls.mask_email(email)
            masked_text = masked_text.replace(email, masked_email)
            pii_found.setdefault('emails', []).append({'original': email, 'masked': masked_email})
        
        # Mask phone numbers
        phones = re.findall(cls.PHONE_PATTERN, text)
        for phone in phones:
            masked_phone = cls.mask_phone(phone)
            masked_text = masked_text.replace(phone, masked_phone)
            pii_found.setdefault('phones', []).append({'original': phone, 'masked': masked_phone})
        
        # Mask SSNs
        ssns = re.findall(cls.SSN_PATTERN, text)
        for ssn in ssns:
            masked_ssn = cls.mask_ssn(ssn)
            masked_text = masked_text.replace(ssn, masked_ssn)
            pii_found.setdefault('ssns', []).append({'original': ssn, 'masked': masked_ssn})
        
        # Mask credit cards
        ccs = re.findall(cls.CREDIT_CARD_PATTERN, text)
        for cc in ccs:
            masked_cc = cls.mask_credit_card(cc)
            masked_text = masked_text.replace(cc, masked_cc)
            pii_found.setdefault('credit_cards', []).append({'original': cc, 'masked': masked_cc})
        
        return masked_text, pii_found


# Singleton instance
pii_masker = PIIMasker()
