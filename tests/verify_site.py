import os
import sys
import re
from html.parser import HTMLParser

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

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

        # Title & Meta
        if "<title>Pedro Planel - Software Engineer</title>" not in html:
            errors.append("Missing or incorrect <title>")

        # Umami script
        if 'src="https://cloud.umami.is/script.js"' not in html or '9bd8d51f-c7bb-430c-b253-4fbb78315826' not in html:
            errors.append("Missing Umami analytics script or incorrect data-website-id")

        # Color stripe (20 color blocks)
        stripe_matches = re.findall(r'style="background-color:\s*#[0-9a-fA-F]{6}"', html)
        if len(stripe_matches) < 20:
            errors.append(f"Expected at least 20 color stripe segments, found {len(stripe_matches)}")

        # Sections
        for section_id in ["about", "projects", "blog", "contact"]:
            if f'id="{section_id}"' not in html:
                errors.append(f"Missing section with id='{section_id}'")

        # Game of Life link
        if 'href="/game-of-life/"' not in html and 'href="game-of-life/"' not in html:
            errors.append("Missing link to /game-of-life/")

        # Contact info
        if "pplanel@gmail.com" not in html:
            errors.append("Missing email contact: pplanel@gmail.com")
        if "github.com/pplanel" not in html and "https://github.com/pplanel" not in html:
            errors.append("Missing GitHub link for pplanel")

        # Footer badges
        if "PROD" not in html:
            errors.append("Missing PROD badge in footer")
        if "V1.0.0" not in html:
            errors.append("Missing V1.0.0 badge in footer")

    if errors:
        print("VERIFICATION FAILED:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("VERIFICATION PASSED: All requirements verified successfully.")

if __name__ == "__main__":
    test_site()
