import re
import math
from urllib.parse import urlparse
from difflib import SequenceMatcher

# Suspicious keywords often seen in phishing
SUSPICIOUS_WORDS = [
    "login", "verify", "secure", "account",
    "update", "bank", "paypal", "confirm",
    "signin", "reset", "alert"
]

# Popular legitimate domains for typosquatting detection
POPULAR_DOMAINS = [
    "google.com", "facebook.com", "paypal.com",
    "amazon.com", "instagram.com", "microsoft.com",
    "apple.com", "linkedin.com"
]


# -------------------------------
# 1️⃣ Shannon Entropy (Novel Feature)
# -------------------------------
def shannon_entropy(text):
    if len(text) == 0:
        return 0

    prob = [float(text.count(c)) / len(text) for c in set(text)]
    entropy = -sum([p * math.log2(p) for p in prob])
    return entropy


# -------------------------------
# 2️⃣ Detect IP Address in URL
# -------------------------------
def has_ip(url):
    pattern = r'http[s]?://(\d{1,3}\.){3}\d{1,3}'
    return 1 if re.search(pattern, url) else 0


# -------------------------------
# 3️⃣ Digit Ratio
# -------------------------------
def digit_ratio(url):
    digits = sum(c.isdigit() for c in url)
    return digits / len(url)


# -------------------------------
# 4️⃣ Suspicious Word Count
# -------------------------------
def suspicious_word_count(url):
    count = 0
    for word in SUSPICIOUS_WORDS:
        if word in url.lower():
            count += 1
    return count


# -------------------------------
# 5️⃣ Typosquatting Similarity (Novel Feature)
# -------------------------------
def typosquat_similarity(domain):
    max_similarity = 0
    for legit in POPULAR_DOMAINS:
        similarity = SequenceMatcher(None, domain, legit).ratio()
        max_similarity = max(max_similarity, similarity)
    return max_similarity


# -------------------------------
# MAIN FEATURE EXTRACTOR
# -------------------------------
def extract_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc

    features = [
        len(url),                      # URL length
        domain.count("."),             # Dot count
        url.count("-"),                # Hyphen count
        sum(c.isdigit() for c in url), # Digit count
        digit_ratio(url),              # Digit ratio
        1 if parsed.scheme == "https" else 0,  # HTTPS flag
        has_ip(url),                   # IP usage
        shannon_entropy(url),          # Entropy (Novel)
        suspicious_word_count(url),    # Suspicious keywords
        typosquat_similarity(domain)   # Typosquatting similarity (Novel)
    ]

    return features