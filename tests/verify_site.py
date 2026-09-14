import os
import sys
import re
import http.server
import socketserver
import threading
import urllib.request

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def test_http_serving():
    errors = []
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=REPO_ROOT, **kwargs)
        def log_message(self, format, *args):
            pass

    httpd = socketserver.TCPServer(("127.0.0.1", 0), QuietHandler)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    try:
        endpoints = [
            ("/", 200),
            ("/game-of-life/", 200),
            ("/game-of-life/index.html", 200),
            ("/game-of-life/bootstrap.js", 200),
            ("/game-of-life/728d384596d1385ab19c.module.wasm", 200),
            ("/CNAME", 200),
        ]
        for path, expected_status in endpoints:
            url = f"http://127.0.0.1:{port}{path}"
            req = urllib.request.Request(url)
            try:
                with urllib.request.urlopen(req) as resp:
                    if resp.status != expected_status:
                        errors.append(f"HTTP {path} returned status {resp.status}, expected {expected_status}")
            except Exception as e:
                errors.append(f"HTTP request to {url} failed: {e}")
    finally:
        httpd.shutdown()
        httpd.server_close()

    return errors

def test_site():
    errors = []

    # 1. Check required files
    for rel_path in ["index.html", "CNAME", "game-of-life/index.html"]:
        full_path = os.path.join(REPO_ROOT, rel_path)
        if not os.path.exists(full_path):
            errors.append(f"Missing required file: {rel_path}")

    # 2. Check CNAME
    cname_path = os.path.join(REPO_ROOT, "CNAME")
    if os.path.exists(cname_path):
        with open(cname_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content != "pplanel.dev":
                errors.append(f"CNAME expected 'pplanel.dev', got '{content}'")

    # 3. Check index.html contents
    index_path = os.path.join(REPO_ROOT, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Viewport & Title
        if '<meta name="viewport" content="width=device-width, initial-scale=1.0">' not in html:
            errors.append("Missing responsive viewport meta tag")
        if "<title>Pedro Planel - Software Engineer</title>" not in html:
            errors.append("Missing or incorrect <title>")

        # Umami script
        if 'src="https://cloud.umami.is/script.js"' not in html or '9bd8d51f-c7bb-430c-b253-4fbb78315826' not in html:
            errors.append("Missing Umami analytics script or incorrect data-website-id")

        # Color stripe (20 color blocks)
        stripe_matches = re.findall(r'style="background-color:\s*#[0-9a-fA-F]{6}"', html)
        if len(stripe_matches) < 20:
            errors.append(f"Expected at least 20 color stripe segments, found {len(stripe_matches)}")

        # Tactile micro-interactions (consolidated in <style> block and applied on elements)
        tactile_rules = [
            ".btn-tactile",
            ".btn-tactile:hover",
            ".btn-tactile:active",
            ".card-tactile",
            ".card-tactile:hover",
            ".card-tactile:active",
            "box-shadow: 2px 2px 0px 0px rgba(0, 0, 0, 0.2);",
            "box-shadow: 3px 3px 0px 0px rgba(0, 0, 0, 0.2);",
            "transform: translate(1px, 1px);",
            "transform: translate(2px, 2px);",
        ]
        for tr in tactile_rules:
            if tr not in html:
                errors.append(f"Missing tactile CSS rule in style block: '{tr}'")

        for cls in ["btn-tactile", "card-tactile"]:
            if cls not in html:
                errors.append(f"Missing tactile class '{cls}' in markup")

        # Responsive navigation
        if "grid-cols-5" not in html or "text-xs md:text-sm" not in html:
            errors.append("Navigation missing responsive grid or text classes")

        # Sections
        for section_id in ["about", "projects", "blog", "contact"]:
            if f'id="{section_id}"' not in html:
                errors.append(f"Missing section with id='{section_id}'")

        # Game of Life link
        if 'href="/game-of-life/"' not in html and 'href="game-of-life/"' not in html:
            errors.append("Missing link to /game-of-life/")

        # Contact info & footer links
        if "pplanel@gmail.com" not in html:
            errors.append("Missing email contact: pplanel@gmail.com")
        if "github.com/pplanel" not in html and "https://github.com/pplanel" not in html:
            errors.append("Missing GitHub link for pplanel")
        if "@PPLANEL" in html:
            errors.append("Found redundant '@PPLANEL' link in footer; expected clean 'GITHUB · EMAIL'")

        # Footer badges
        if "PROD" not in html:
            errors.append("Missing PROD badge in footer")
        if "V1.0.0" not in html:
            errors.append("Missing V1.0.0 badge in footer")

    # 4. Check HTTP serving
    http_errors = test_http_serving()
    errors.extend(http_errors)

    if errors:
        print("VERIFICATION FAILED:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("VERIFICATION PASSED: All requirements verified successfully.")

if __name__ == "__main__":
    test_site()
