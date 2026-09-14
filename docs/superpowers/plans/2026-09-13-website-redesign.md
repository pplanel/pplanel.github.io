# Website Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `pplanel.dev` into a responsive neo-brutalist developer portfolio matching the design and layout of `aprilnea.me/en`.

**Architecture:** Single-page static HTML5 application using Tailwind CSS and custom neo-brutalist utility classes for borders, hard drop shadows, and tactile button animations. Runs directly on GitHub Pages with zero build step.

**Tech Stack:** HTML5, Tailwind CSS (via CDN), CSS3 variables & animations, Node.js/Python for automated testing.

**Spec:** [docs/superpowers/specs/2026-09-13-website-redesign-design.md](file:///Users/pplanel/src/pplanel.github.io/docs/superpowers/specs/2026-09-13-website-redesign-design.md)

## Global Constraints

- Preserve `CNAME` with content `pplanel.dev` intact.
- Preserve `game-of-life/` directory intact and link to `/game-of-life/` in the projects section.
- Preserve Umami tracking script (`<script defer src="https://cloud.umami.is/script.js" data-website-id="9bd8d51f-c7bb-430c-b253-4fbb78315826"></script>`).
- Retain zero-build deployment: website must be fully viewable directly from root `index.html`.
- All styling must match the neo-brutalist token rules: `#e8e8e8` background, 1px solid black borders, hard offset shadows (`shadow-[2px_2px_0px_0px_rgba(0,0,0,0.2)]`, `shadow-[4px_4px_0px_0px_rgba(0,0,0,0.2)]`), monospace font stack, and 20-segment color calibration bar.

---

### Task 1: Automated Verification Test Suite

**Files:**
- Create: `tests/verify_site.py`

**Interfaces:**
- Consumes: `index.html`, `CNAME`, `game-of-life/index.html`
- Produces: CLI exit code `0` on test success, non-zero on failure. Validates HTML DOM structure, required anchors, color stripe count, meta tags, and analytics script.

- [ ] **Step 1: Write the automated test script**

Create `tests/verify_site.py` to validate:
1. File existence (`index.html`, `CNAME`, `game-of-life/index.html`).
2. CNAME contains `pplanel.dev`.
3. Umami analytics script with `data-website-id="9bd8d51f-c7bb-430c-b253-4fbb78315826"` is present in `<head>`.
4. Page title is `Pedro Planel - Software Engineer`.
5. Top bar has the 20-segment color bar (`div` containing 20 colored children).
6. Navigation contains 5 links (`#about`, `#projects`, `#blog`, `#contact` or direct links) and green status indicator dot.
7. Sections with IDs `about`, `projects`, `blog`, `contact` exist.
8. Featured project link to `/game-of-life/` exists.
9. Contact table contains `pplanel@gmail.com` and `github.com/pplanel`.
10. Footer contains copyright `PEDRO PLANEL`, `PROD` badge, and `V1.0.0` badge.

```python
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
```

- [ ] **Step 2: Run test to verify it fails on current codebase**

Run: `python3 tests/verify_site.py`
Expected: FAIL with missing title, sections, color stripes, etc.

- [ ] **Step 3: Commit verification test suite**

```bash
git add tests/verify_site.py
git commit -m "test: add verification test suite for website redesign"
```

---

### Task 2: Implement Neo-Brutalist `index.html`

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: Design spec tokens (`#e8e8e8` background, 1px solid black borders, hard offset drop shadows, 20-segment color bar, tactile buttons).
- Produces: Complete responsive single-page layout passing `tests/verify_site.py`.

- [ ] **Step 1: Write the updated `index.html`**

Update `index.html` with:
1. Clean HTML5 header with viewport meta, Tailwind CSS via CDN, custom styles for neo-brutalist tactile micro-interactions (`.btn-tactile`, `.card-tactile`), monospace font stack, and the Umami script.
2. Neo-brutalist header:
   - Name: `Pedro Planel`
   - 20-segment color bar with exact colors: `#c41e3a`, `#e85d04`, `#1e4d8c`, `#2563eb`, `#06b6d4`, `#d4a72c`, `#a855f7`, `#1e1e1e`, `#e5e5e5`, `#d4d4d4`, `#c4c4c4`, `#b4b4b4`, `#a4a4a4`, `#949494`, `#1e1e1e`, `#177a45`, `#2563eb`, `#7c3aed`, `#c41e3a`, `#e85d04`.
   - GitHub badge button: `GH ↗` linking to `https://github.com/pplanel`.
3. Navigation bar:
   - Buttons for `Home`, `About`, `Projects`, `Blog`, `Contact`.
   - `Home` tab has green status indicator dot (`bg-[#177a45]`).
   - Smooth scroll anchor links.
4. Main card container (`bg-white border border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,0.2)] p-4 md:p-6`):
   - **Hello / About Section (`id="about"`)**:
     - Monospace section header `Hello` with dotted divider.
     - 2-column grid (`grid-cols-1 md:grid-cols-[2fr_1fr] gap-6`):
       - Left: Role `Software Engineer / Open Source Enthusiast / Builder`, blockquote callout, bio text, yellow `Contact →` button (`bg-[#d4a72c]`), `(Open for collaboration)` status.
       - Right: Philosophy card with bordered tenets and accent stripes.
   - Dotted section divider.
   - **Projects Section (`id="projects"`)**:
     - Header `Projects` with dotted divider.
     - 2-column grid:
       - Left: Work overview, orange button `View GitHub →` (`bg-[#f2572b] text-white`).
       - Right: Featured project card for **Conway's Game of Life** linking to `/game-of-life/`, highlighting WebAssembly & WebGL.
   - Dotted section divider.
   - **Blog Section (`id="blog"`)**:
     - Header `Blog` with dotted divider.
     - Writing overview, green button `View Posts →` (`bg-[#177a45] text-white`).
   - Dotted section divider.
   - **Contact Section (`id="contact"`)**:
     - Header `Contact` with dotted divider.
     - Monospace table with blue left-accent border (`border-l-4 border-[#3498db]`) containing Email, GitHub, Website, Availability.
5. Footer:
   - Top border, copyright notice `© COPYRIGHT 2026, PEDRO PLANEL. ALL RIGHTS RESERVED.`
   - GitHub and Email links.
   - Status badges: Green `PROD` pill + bordered `V1.0.0` badge.

- [ ] **Step 2: Run verification test suite**

Run: `python3 tests/verify_site.py`
Expected: `VERIFICATION PASSED: All requirements verified successfully.`

- [ ] **Step 3: Commit updated `index.html`**

```bash
git add index.html
git commit -m "feat: implement neo-brutalist personal website redesign"
```

---

### Task 3: Local Verification & Visual Polish

**Files:**
- Test against: `index.html`, `game-of-life/index.html`

**Interfaces:**
- Consumes: Static files served locally via HTTP.
- Produces: Confirmed rendering, navigation smooth-scrolling, tactile button depression, and responsive layout.

- [ ] **Step 1: Test static serving via local HTTP server**

Run: `python3 -m http.server 8000 &` (or run background task) and test HTTP response codes for `/`, `/game-of-life/`, and assets.

- [ ] **Step 2: Verify responsive viewport and micro-interactions**

Check CSS classes to ensure:
- Viewport `<meta name="viewport" content="width=device-width, initial-scale=1.0">` is present.
- Buttons include tactile classes:
  - `shadow-[2px_2px_0px_0px_rgba(0,0,0,0.2)]`
  - `hover:shadow-[1px_1px_0px_0px_rgba(0,0,0,0.2)] hover:translate-x-[1px] hover:translate-y-[1px]`
  - `active:shadow-none active:translate-x-[2px] active:translate-y-[2px]`
- Nav items wrap neatly on mobile screen widths (`text-xs md:text-sm`).

- [ ] **Step 3: Commit any final polish adjustments**

```bash
git add index.html
git commit -m "chore: finalize website styling and responsive layout"
```
