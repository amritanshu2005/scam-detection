"""
Intelligence Extraction Module
Extracts bank accounts, UPI IDs, phishing URLs, and other intelligence from conversations
"""

import re
from typing import List, Dict, Any


class IntelligenceExtractor:
    """Extracts actionable intelligence from conversation messages"""
    
    def __init__(self):
        # Patterns for different types of intelligence
        self.patterns = {
            "bank_account": [
                r'\b\d{9,18}\b',  # 9-18 digit account numbers
                r'account\s*(?:no|number|#)?\s*:?\s*(\d{9,18})',
                r'ac\s*(?:no|number|#)?\s*:?\s*(\d{9,18})',
            ],
            "upi_id": [
                r'upi://pay\?[^\s]+',
                r'[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.(?:paytm|ybl|okaxis|okicici|oksbi|phonepe|gpay|amazonpay)',
                r'[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # Generic UPI format
                r'\b\d{10}@[a-zA-Z]+\b',  # Phone number @ bank format
            ],
            "phishing_url": [
                r'https?://[^\s<>"{}|\\^`\[\]]+',
                r'www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}[^\s<>"{}|\\^`\[\]]*',
                r'[a-zA-Z0-9.-]+\.(?:com|net|org|in|co\.in|io|xyz|online)[^\s<>"{}|\\^`\[\]]*',
            ],
            "ifsc": [
                r'\b[A-Z]{4}0\d{6}\b',  # IFSC code format
            ],
            "phone": [
                r'\b(?:\+91|91|0)?[6-9]\d{9}\b',  # Indian phone numbers
            ],
            "email": [
                r'\b[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
            ],
        }
        
        # Compile patterns
        self.compiled_patterns = {
            key: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
            for key, patterns in self.patterns.items()
        }
        
        # Suspicious domain indicators
        self.suspicious_domains = [
            'bit.ly', 'tinyurl', 'short.link', 't.co',
            'free', 'prize', 'winner', 'claim', 'verify',
            'bank-verify', 'account-update', 'secure-login'
        ]
    
    def extract(self, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract intelligence from conversation
        
        Args:
            conversation_history: List of conversation messages
            
        Returns:
            Dictionary with extracted intelligence
        """
        intelligence = {
            "bank_accounts": [],
            "upi_ids": [],
            "phishing_urls": [],
            "other": {}
        }
        
        # Combine all messages
        full_text = " ".join([
            msg.get("content", "") for msg in conversation_history
            if msg.get("role") == "scammer"
        ])
        
        # Extract bank accounts
        intelligence["bank_accounts"] = self._extract_bank_accounts(full_text)
        
        # Extract UPI IDs
        intelligence["upi_ids"] = self._extract_upi_ids(full_text)
        
        # Extract phishing URLs
        intelligence["phishing_urls"] = self._extract_phishing_urls(full_text)
        
        # Extract other intelligence
        intelligence["other"] = {
            "ifsc_codes": self._extract_ifsc(full_text),
            "phone_numbers": self._extract_phone_numbers(full_text),
            "emails": self._extract_emails(full_text),
        }
        
        return intelligence
    
    def _extract_bank_accounts(self, text: str) -> List[str]:
        """Extract bank account numbers"""
        accounts = set()
        
        # Try all bank account patterns
        for pattern in self.compiled_patterns["bank_account"]:
            matches = pattern.findall(text)
            for match in matches:
                # Extract number from match (could be tuple or string)
                account = match if isinstance(match, str) else match[0] if match else ""
                if account:
                    # Validate: 9-18 digits, not a phone number
                    if account.isdigit() and 9 <= len(account) <= 18:
                        # Exclude if it looks like a phone number
                        if not (len(account) == 10 and account[0] in '6789'):
                            accounts.add(account)
        
        return list(accounts)
    
    def _extract_upi_ids(self, text: str) -> List[str]:
        """Extract UPI IDs"""
        upi_ids = set()
        
        # Extract UPI payment links
        for pattern in self.compiled_patterns["upi_id"]:
            matches = pattern.findall(text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else ""
                
                if match:
                    # Clean and validate UPI ID
                    cleaned = match.strip()
                    # UPI IDs typically have @ symbol
                    if '@' in cleaned or 'upi://' in cleaned.lower():
                        upi_ids.add(cleaned)
        
        return list(upi_ids)
    
    def _extract_phishing_urls(self, text: str) -> List[str]:
        """Extract phishing URLs"""
        urls = set()
        
        for pattern in self.compiled_patterns["phishing_url"]:
            matches = pattern.findall(text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else ""
                
                if match:
                    url = match.strip()
                    # Filter out common legitimate domains (optional - can be customized)
                    if not self._is_legitimate_domain(url):
                        urls.add(url)
        
        return list(urls)
    
    def _extract_ifsc(self, text: str) -> List[str]:
        """Extract IFSC codes"""
        ifsc_codes = set()
        
        for pattern in self.compiled_patterns["ifsc"]:
            matches = pattern.findall(text)
            for match in matches:
                if match:
                    ifsc_codes.add(match.upper())
        
        return list(ifsc_codes)
    
    def _extract_phone_numbers(self, text: str) -> List[str]:
        """Extract phone numbers"""
        phones = set()
        
        for pattern in self.compiled_patterns["phone"]:
            matches = pattern.findall(text)
            for match in matches:
                if match:
                    # Clean phone number
                    phone = re.sub(r'[^\d]', '', match)
                    if len(phone) == 10:
                        phones.add(phone)
        
        return list(phones)
    
    def _extract_emails(self, text: str) -> List[str]:
        """Extract email addresses"""
        emails = set()
        
        for pattern in self.compiled_patterns["email"]:
            matches = pattern.findall(text)
            for match in matches:
                if match:
                    # Exclude UPI IDs (they look like emails but aren't)
                    if not any(domain in match.lower() for domain in ['paytm', 'ybl', 'okaxis', 'okicici', 'oksbi']):
                        emails.add(match.lower())
        
        return list(emails)
    
    def _is_legitimate_domain(self, url: str) -> bool:
        """Check if URL is from a legitimate domain"""
        legitimate_domains = [
            'google.com', 'facebook.com', 'twitter.com', 'linkedin.com',
            'github.com', 'stackoverflow.com', 'wikipedia.org',
            'amazon.in', 'flipkart.com', 'paytm.com', 'phonepe.com',
            'gpay', 'bank', 'gov.in', 'nic.in'
        ]
        
        url_lower = url.lower()
        return any(domain in url_lower for domain in legitimate_domains)

