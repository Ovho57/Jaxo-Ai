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
            self.parts.append("\\n")
    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript", "svg"} and self.skip:
            self.skip -= 1
        elif tag in {"p", "div", "li", "h1", "h2", "h3", "tr"} and not self.skip:
            self.parts.append("\\n")
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
                response = client.get(current)
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
                raw = response.content[:MAX_BYTES].decode(response.encoding or "utf-8", errors="replace")
                if "html" in content_type or "<html" in raw[:1000].lower():
                    parser = TextExtractor()
                    parser.feed(raw)
                    extracted = "\\n".join(parser.parts)
                else:
                    extracted = raw
                page_text = "\\n".join(line.strip() for line in extracted.splitlines() if line.strip())
                return f"URL: {current}\\nHTTP: {response.status_code}\\n\\n{(page_text or '(No readable text; this site may require JavaScript.)')[:30000]}"
            return "Too many redirects (limit: 5)."
    except (httpx.HTTPError, OSError, ValueError) as exc:
        return f"Website inspection failed: {exc}"
