import ipaddress
import socket
from urllib.parse import urljoin, urlparse
import httpx
from html.parser import HTMLParser

MAX_BYTES = 1_000_000

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip = [], 0
    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip += 1
        elif tag in {"p", "div", "br", "li", "h1", "h2", "h3", "tr"} and not self.skip:
            self.parts.append("\n")
    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript", "svg"} and self.skip:
            self.skip -= 1
        elif tag in {"p", "div", "li", "h1", "h2", "h3", "tr"} and not self.skip:
            self.parts.append("\n")
    def handle_data(self, data):
        if not self.skip:
            value = " ".join(data.split())
            if value:
                self.parts.append(value)

def validate_public_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Provide a complete public http:// or https:// URL.")
    if parsed.username or parsed.password:
        raise ValueError("URLs containing embedded credentials are blocked.")
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(parsed.hostname, None)}
    except OSError as exc:
        raise ValueError(f"Could not resolve website host: {exc}") from exc
    if not addresses or any(not ipaddress.ip_address(addr).is_global for addr in addresses):
        raise ValueError("Private, local, and reserved network addresses are blocked.")
    return parsed

def inspect_website(url):
    """Fetch readable text from a public website; no login or JavaScript execution."""
    current = url.strip()
    headers = {"User-Agent": "JAXO-Website-Inspector/1.0", "Accept": "text/html,text/plain,application/xhtml+xml"}
    try:
        with httpx.Client(timeout=15.0, follow_redirects=False, headers=headers) as client:
            for _ in range(6):
                validate_public_url(current)
                with client.stream("GET", current) as response:
                    if response.status_code in {301, 302, 303, 307, 308}:
                        location = response.headers.get("location")
                        if not location:
                            return "Redirect without a Location header."
                        current = urljoin(current, location)
                        continue
                    response.raise_for_status()
                    content_type = response.headers.get("content-type", "").lower()
                    if not any(kind in content_type for kind in ("text/html", "text/plain", "application/xhtml+xml")):
                        return f"Unsupported page type ({content_type or 'unknown'}). HTML/plain text only."
                    chunks, total = [], 0
                    for chunk in response.iter_bytes():
                        remaining = MAX_BYTES - total
                        if remaining <= 0:
                            break
                        piece = chunk[:remaining]
                        chunks.append(piece)
                        total += len(piece)
                        if total >= MAX_BYTES:
                            break
                    raw = b"".join(chunks).decode(response.encoding or "utf-8", errors="replace")
                if "html" in content_type or "<html" in raw[:1000].lower():
                    parser = TextExtractor()
                    parser.feed(raw)
                    extracted = "\n".join(parser.parts)
                else:
                    extracted = raw
                page_text = "\n".join(line.strip() for line in extracted.splitlines() if line.strip())
                return f"URL: {current}\nHTTP: {response.status_code}\n\n{(page_text or '(No readable text; this site may require JavaScript.)')[:30000]}"
            return "Too many redirects (limit: 5)."
    except (httpx.HTTPError, OSError, ValueError) as exc:
        return f"Website inspection failed: {exc}"


def check_phishing_site(url):
    """Heuristic phishing triage; not a definitive reputation verdict."""
    import ipaddress
    from urllib.parse import urlparse, urljoin
    parsed = urlparse(url.strip())
    host = (parsed.hostname or "").lower()
    reasons = []
    if parsed.scheme != "https":
        reasons.append("The URL does not use HTTPS.")
    if "@" in parsed.netloc:
        reasons.append("The URL contains an @ symbol that can disguise its true destination.")
    try:
        ipaddress.ip_address(host)
        reasons.append("The site uses a raw IP address rather than a normal domain.")
    except ValueError:
        pass
    if host.startswith("xn--") or ".xn--" in host:
        reasons.append("The domain uses punycode, which can be used to imitate another domain.")
    if host in {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "cutt.ly"}:
        reasons.append("The link uses a URL shortener, hiding its final destination.")
    if host.count(".") >= 4:
        reasons.append("The domain has an unusually deep subdomain structure.")
    if any(host.endswith(tld) for tld in {".zip", ".click", ".top", ".work", ".support", ".gq", ".tk", ".ml", ".cf"}):
        reasons.append("The domain uses a top-level domain frequently seen in suspicious campaigns.")
    keywords = [word for word in ("login", "verify", "secure", "account", "password", "wallet", "payment", "bank") if word in (host + parsed.path + parsed.query).lower()]
    if len(keywords) >= 2:
        reasons.append("The URL contains multiple sensitive-account keywords: " + ", ".join(keywords))
    if len(url) > 180:
        reasons.append("The URL is unusually long.")
    final_url = url
    try:
        with httpx.Client(timeout=15.0, follow_redirects=False, headers={"User-Agent":"JAXO-Phishing-Check/1.0"}) as client:
            for _ in range(6):
                validate_public_url(final_url)
                with client.stream("GET", final_url) as response:
                    if response.status_code in {301,302,303,307,308}:
                        target = response.headers.get("location")
                        if not target:
                            reasons.append("Redirect has no destination.")
                            break
                        final_url = urljoin(final_url, target)
                        continue
                    response.raise_for_status()
                    if "html" in response.headers.get("content-type", "").lower():
                        data, size = [], 0
                        for chunk in response.iter_bytes():
                            part = chunk[:MAX_BYTES-size]
                            data.append(part)
                            size += len(part)
                            if size >= MAX_BYTES:
                                break
                        parser = PageParser()
                        parser.feed(b"".join(data).decode(response.encoding or "utf-8", errors="replace"))
                        final_host = (urlparse(final_url).hostname or "").lower()
                        if parser.password_fields:
                            reasons.append(f"The page contains {parser.password_fields} password field(s); verify the domain before entering credentials.")
                        for action in parser.form_actions:
                            if action:
                                action_host = (urlparse(urljoin(final_url, action)).hostname or "").lower()
                                if action_host and action_host != final_host:
                                    reasons.append(f"A form submits data to a different domain: {action_host}.")
                    break
    except (httpx.HTTPError, OSError, ValueError) as exc:
        reasons.append(f"Live inspection could not complete: {exc}")
    reasons = list(dict.fromkeys(reasons))
    if len(reasons) >= 3:
        verdict = "HIGH RISK — do not enter passwords or payment details."
    elif reasons:
        verdict = "CAUTION — suspicious indicators found; verify independently."
    else:
        verdict = "NO OBVIOUS WARNING SIGNS — this does NOT prove the site is safe."
    findings = "\n".join("- " + item for item in reasons) if reasons else "- No obvious heuristic warning signs detected."
    return f"JAXO PHISHING CHECK\nURL: {url}\nFinal URL: {final_url}\nAssessment: {verdict}\n\n{findings}\n\nThis is heuristic analysis, not a live antivirus or threat-intelligence verdict. A clean result cannot guarantee safety."
