from bs4 import BeautifulSoup
import re
import tldextract
from urllib.parse import urlparse


def extract_url_features(url: str) -> dict:
    parsed = urlparse(url)
    extracted = tldextract.extract(url)

    registered_domain = f"{extracted.domain}.{extracted.suffix}"
    subdomains = extracted.subdomain.split(".") if extracted.subdomain else []

    return {
        "url": url,
        "domain": registered_domain,
        "subdomain": extracted.subdomain,
        "subdomain_depth": len(subdomains),
        "path": parsed.path,
        "url_length": len(url),
        "num_digits_in_url": sum(c.isdigit() for c in url),
        "is_punycode": "xn--" in url,
    }


def compact_html(url: str, raw_html: str) -> dict:
    url_info = extract_url_features(url)

    if not raw_html:
        return {"url_info": url_info, "summary": "Empty HTML content"}

    soup = BeautifulSoup(raw_html, "html.parser")

    # 1. Page Title & Meta Description
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": re.compile(r"description", re.I)})
    if meta_tag and meta_tag.get("content"):
        meta_desc = meta_tag["content"].strip()

    # 2. Form Analysis (Critical for Phishing)
    forms = []
    for form in soup.find_all("form")[:3]:  # Top 3 forms are enough
        action = form.get("action", "").strip()
        inputs = []
        for inp in form.find_all(["input", "textarea"]):
            inp_type = inp.get("type", "text")
            inp_name = inp.get("name") or inp.get("id") or ""
            inputs.append(f"{inp_type}:{inp_name}")
        forms.append({"action": action, "inputs": inputs[:6]})

    # 3. Security Red Flags
    raw_lower = raw_html.lower()
    flags = {
        "has_password_field": bool(soup.find("input", {"type": "password"})),
        "has_hidden_iframe": bool(
            soup.find("iframe", style=re.compile(r"display:\s*none|visibility:\s*hidden", re.I))
        ),
        "has_eval_or_unescape": bool(re.search(r"\b(eval|unescape)\s*\(", raw_lower)),
        "has_base64_strings": bool(re.search(r"data:text/html;base64,", raw_lower)),
        "right_click_disabled": "contextmenu" in raw_lower,
    }

    # 4. Visible Text (first 600 characters)
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    visible_text = soup.get_text(separator=" ", strip=True)
    visible_text_snippet = " ".join(visible_text.split()[:100])

    return {
        "url_info": url_info,
        "title": title[:100],
        "meta_description": meta_desc[:200],
        "forms": forms,
        "flags": flags,
        "visible_snippet": visible_text_snippet,
    }