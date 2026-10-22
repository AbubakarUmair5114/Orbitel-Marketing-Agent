"""
Orbitel Customer Sentiment & Churn Risk Intelligence Engine
Production Webhook Test Harness & Security / Validation Suite

Tests:
1. Valid high-risk corporate network outage payload.
2. Valid billing dispute payload.
3. Schema Validation Failures (Missing fields, text < 10 chars) -> HTTP 400.
4. PII Redaction Engine (Pakistani phone numbers and email addresses).
5. Heuristic Urgency Override (Regex patterns for legal, outage, switch, roman urdu).
6. Business Signal Time-Window Deduplication Logic.
"""

import re
import json
import uuid
import datetime

# --- Validation Constants from n8n Workflow Node 2 ---
MIN_TEXT = 10
MAX_TEXT = 2000
MAX_ID = 100
CUSTOMER_TYPES = ['individual', 'household', 'sme', 'corporate', 'enterprise']
SERVICE_TYPES = ['postpaid', 'prepaid', 'data', 'voice', 'sms', 'roaming', 'broadband', 'international_calling', 'business_plan', 'add_on_package']

EMAIL_REGEX = re.compile(r'[^\s@<>()[\]",;]+@[^\s@<>()[\]",;]+\.[^\s@<>()[\]",;]+')
PAK_PHONE_REGEX = re.compile(r'(?<!\d)(?:(?:\+|00)?92[\s\-.]?|0)\(?3\d{2}\)?[\s\-.]?\d{3}[\s\-.]?\d{4}(?!\d)')

URGENCY_PATTERNS = [
    (re.compile(r'\bcancel\w*', re.IGNORECASE), 'cancel'),
    (re.compile(r'\bswitch\w*', re.IGNORECASE), 'switch'),
    (re.compile(r'\boutage\w*', re.IGNORECASE), 'outage'),
    (re.compile(r'\bfraud\w*', re.IGNORECASE), 'fraud'),
    (re.compile(r'\b(legal\w*|lawsuit|court\s?case|sue\b|suing\b)', re.IGNORECASE), 'legal'),
    (re.compile(r'\brefund\w*', re.IGNORECASE), 'refund'),
    (re.compile(r'\bterminat\w*', re.IGNORECASE), 'terminate'),
    (re.compile(r'\bdisconnect\w*', re.IGNORECASE), 'disconnect'),
    (re.compile(r'\b(complain\w*|escalat\w*|PTA\b|PEMRA\b|regulator\w*)', re.IGNORECASE), 'complaint_escalation'),
    (re.compile(r'\b(band\s?karo|chorr?\w*|chorna|chod\w*|nikal\w*|wapas\w*|dobara\s?nahi|nahi\s?chahiye|problem\s?hai|bahut\s?bura)\b', re.IGNORECASE), 'roman_urdu_urgency'),
    (re.compile(r'\b(jazz|telenor|zong|ufone|going\s?to\s?(switch|leave|move))\b', re.IGNORECASE), 'competitor_switch'),
    (re.compile(r'\b(leaving|leaving\s?orbitel|port\s?out|number\s?portability|MNP)\b', re.IGNORECASE), 'leaving')
]

WINDOWS = {
    'coverage_expansion': 7 * 24,
    'billing_issue': 30 * 24,
    'service_recovery': 48,
    'hr_escalation': 7 * 24,
    'upsell_opportunity': 30 * 24,
    'product_feedback': 90 * 24,
    'none': 24
}

def validate_and_clean_payload(body, headers={'content-type': 'application/json'}):
    """Simulates Node 2 (Validate & Clean Input) in the n8n workflow."""
    if not isinstance(body, dict):
        return {"valid": False, "http_status": 400, "error": "Request body must be a JSON object.", "field": "body"}

    # Text validation
    raw_text = body.get("text")
    if raw_text is None or not isinstance(raw_text, str):
        return {"valid": False, "http_status": 400, "error": "text is required and must be a string.", "field": "text"}
    
    cleaned_text = " ".join(raw_text.split())
    if len(cleaned_text) < MIN_TEXT:
        return {"valid": False, "http_status": 400, "error": f"text must be at least {MIN_TEXT} characters after trimming.", "field": "text"}

    # Customer ID validation
    cid = body.get("customer_id")
    if not cid:
        return {"valid": False, "http_status": 400, "error": "customer_id is required.", "field": "customer_id"}
    cid_str = str(cid).strip()
    if len(cid_str) > MAX_ID:
        return {"valid": False, "http_status": 400, "error": f"customer_id exceeds max length {MAX_ID}.", "field": "customer_id"}

    # PII Redaction
    redacted_text = EMAIL_REGEX.sub("[EMAIL_REMOVED]", cleaned_text)
    redacted_text = PAK_PHONE_REGEX.sub("[PHONE_REMOVED]", redacted_text)

    # Urgency override heuristics
    urgency_override = False
    matched_labels = []
    for pattern, label in URGENCY_PATTERNS:
        if pattern.search(redacted_text):
            urgency_override = True
            matched_labels.append(label)

    return {
        "valid": True,
        "http_status": 200,
        "customer_id": cid_str,
        "customer_type": body.get("customer_type", "unknown").lower() if body.get("customer_type", "").lower() in CUSTOMER_TYPES else "unknown",
        "service_type": body.get("service_type", "unknown").lower() if body.get("service_type", "").lower() in SERVICE_TYPES else "unknown",
        "source": str(body.get("source", "unknown"))[:100],
        "cleanedText": redacted_text[:MAX_TEXT],
        "urgency_override": urgency_override,
        "matched_urgency_labels": matched_labels,
        "record_id": f"rec-{uuid.uuid4().hex[:12]}"
    }

def check_dedup(current_record, historical_records):
    """Simulates Node 9 (Dedup Check) across business signal time windows."""
    signal = current_record.get("business_signal", "none")
    window_hours = WINDOWS.get(signal, 24)
    now = datetime.datetime.now(datetime.timezone.utc)
    window_start = now - datetime.timedelta(hours=window_hours)

    duplicate = None
    for row in historical_records:
        if row.get("customer_id") != current_record.get("customer_id"):
            continue
        if row.get("business_signal") != signal:
            continue
        
        row_time = datetime.datetime.fromisoformat(row.get("timestamp").replace("Z", "+00:00"))
        if row_time >= window_start:
            duplicate = row
            break

    return {
        "is_duplicate": duplicate is not None,
        "duplicate_of": duplicate.get("record_id") if duplicate else "",
        "dedup_window_hours": window_hours
    }

def run_test_suite():
    print("======================================================================")
    print("ORBITEL INTELLIGENCE ENGINE - WEBHOOK VALIDATION & SECURITY TEST SUITE")
    print("======================================================================\n")

    # TEST 1: Valid Corporate Network Blackout Payload
    payload_1 = {
        "customer_id": "ORB-CORP-992",
        "customer_type": "enterprise",
        "service_type": "fiber",
        "source": "WhatsApp Support",
        "text": "Severe fiber outage in Sundar Industrial Estate. Our cloud ERP is disconnected and we are planning to switch to competitor Jazz immediately."
    }
    res1 = validate_and_clean_payload(payload_1)
    print("[TEST 1] Valid Corporate Blackout Payload:")
    assert res1["valid"] is True and res1["http_status"] == 200
    assert res1["urgency_override"] is True
    assert "outage" in res1["matched_urgency_labels"] and "switch" in res1["matched_urgency_labels"]
    print("  -> Status: PASSED (HTTP 200, Urgency Override = TRUE, Labels: outage, switch)\n")

    # TEST 2: Schema Validation Failure - Text Length < 10 characters
    payload_2 = {
        "customer_id": "ORB-102",
        "customer_type": "individual",
        "service_type": "prepaid",
        "source": "Web Portal",
        "text": "No signal"  # 9 characters
    }
    res2 = validate_and_clean_payload(payload_2)
    print("[TEST 2] Malformed Payload (Text < 10 characters):")
    assert res2["valid"] is False and res2["http_status"] == 400
    assert "at least 10 characters" in res2["error"]
    print(f"  -> Status: PASSED (HTTP 400 Rejection: {res2['error']})\n")

    # TEST 3: Schema Validation Failure - Missing Customer ID
    payload_3 = {
        "customer_type": "individual",
        "service_type": "postpaid",
        "source": "Email",
        "text": "My 4G speeds in F-10 Islamabad are extremely fast and reliable!"
    }
    res3 = validate_and_clean_payload(payload_3)
    print("[TEST 3] Missing Required Field (customer_id):")
    assert res3["valid"] is False and res3["http_status"] == 400
    assert res3["field"] == "customer_id"
    print(f"  -> Status: PASSED (HTTP 400 Rejection on field: '{res3['field']}')\n")

    # TEST 4: PII Redaction of Pakistani Mobile Numbers and Emails
    payload_4 = {
        "customer_id": "ORB-5541",
        "customer_type": "household",
        "service_type": "broadband",
        "source": "Web Form",
        "text": "Call me on 0300-1234567 or email direct to ceo@enterprise-pk.com regarding my illegal billing charges."
    }
    res4 = validate_and_clean_payload(payload_4)
    print("[TEST 4] PII Redaction Engine (Masking Mobile & Email):")
    assert "[PHONE_REMOVED]" in res4["cleanedText"]
    assert "[EMAIL_REMOVED]" in res4["cleanedText"]
    assert "0300-1234567" not in res4["cleanedText"]
    assert "ceo@enterprise-pk.com" not in res4["cleanedText"]
    print(f"  -> Redacted Text: \"{res4['cleanedText']}\"")
    print("  -> Status: PASSED (PII successfully masked before LLM ingestion)\n")

    # TEST 5: Roman Urdu Urgency Heuristic Trigger
    payload_5 = {
        "customer_id": "ORB-7721",
        "customer_type": "individual",
        "service_type": "postpaid",
        "source": "Phone Helpline",
        "text": "Roz roz network band karo ge to hum SIM tod ke doosri le lenge. Bohot bura service hai!"
    }
    res5 = validate_and_clean_payload(payload_5)
    print("[TEST 5] Roman Urdu Colloquial Churn Detection:")
    assert res5["urgency_override"] is True
    assert "roman_urdu_urgency" in res5["matched_urgency_labels"]
    print(f"  -> Matched Labels: {res5['matched_urgency_labels']}")
    print("  -> Status: PASSED (Colloquial Pakistani churn expressions captured)\n")

    # TEST 6: Business Signal Deduplication Window
    print("[TEST 6] Business Signal Deduplication Window Logic:")
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    recent_timestamp = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=4)).isoformat()
    old_timestamp = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=180)).isoformat()

    current_signal_record = {
        "customer_id": "ORB-CORP-992",
        "business_signal": "coverage_expansion",
        "record_id": "rec-new-001"
    }

    history_with_recent_duplicate = [
        {
            "customer_id": "ORB-CORP-992",
            "business_signal": "coverage_expansion",
            "record_id": "rec-hist-001",
            "timestamp": recent_timestamp
        }
    ]

    dedup_res_1 = check_dedup(current_signal_record, history_with_recent_duplicate)
    assert dedup_res_1["is_duplicate"] is True
    print(f"  -> Recent submission within 7-day window: Suppressed (is_duplicate = TRUE, duplicate_of = {dedup_res_1['duplicate_of']})")

    history_with_expired_window = [
        {
            "customer_id": "ORB-CORP-992",
            "business_signal": "coverage_expansion",
            "record_id": "rec-hist-002",
            "timestamp": old_timestamp
        }
    ]
    dedup_res_2 = check_dedup(current_signal_record, history_with_expired_window)
    assert dedup_res_2["is_duplicate"] is False
    print("  -> Past submission outside 7-day window: Allowed (is_duplicate = FALSE)")
    print("  -> Status: PASSED (Department alert flood prevention confirmed)\n")

    print("======================================================================")
    print("ALL 6 PRODUCTION TEST SUITES COMPLETED WITH 100% SUCCESS!")
    print("======================================================================")

if __name__ == "__main__":
    run_test_suite()

