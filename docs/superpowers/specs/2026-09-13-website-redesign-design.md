# Personal Website Redesign Design Specification

- **Date**: 2026-09-13
- **Author**: Antigravity & Pedro Planel
- **Status**: Approved by User

## 1. Overview & Objective

Redesign the personal website at `pplanel.dev` (`pplanel.github.io`) to replicate the neo-brutalist aesthetic and layout of [aprilnea.me/en](https://aprilnea.me/en). The result is a clean, responsive single-page developer portfolio showcasing Pedro Planel's engineering focus, philosophy, featured projects (notably the existing WebAssembly Game of Life), blog preview, and contact details.

## 2. Architecture & Technology Stack

- **Approach**: Pure Static HTML5 with Tailwind CSS (Approach 1).
- **Hosting**: GitHub Pages via root `index.html` (zero build step required).
- **Preserved Assets**:
  - `CNAME`: Configured for `pplanel.dev`.
  - `/game-of-life/`: Retained intact and linked as a featured project.
  - Analytics: Umami tracking script (`data-website-id="9bd8d51f-c7bb-430c-b253-4fbb78315826"`).
- **Dependencies**: Tailwind CSS via CDN with customized utility styles for neo-brutalist shadows and tactile animations.

## 3. Design System & Visual Language

- **Background**: Soft retro concrete grey (`#e8e8e8`).
- **Main Container**: White (`#ffffff`) card with a 1px solid black border and hard 4px offset shadow: `border border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,0.2)]`.
- **Typography**: Monospace font stack (`font-mono`, `ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace`) across all headers, body copy, tables, and buttons.
- **Section Dividers**: Gray dotted lines (`border-t border-dotted border-gray-400`).
- **Tactile Button & Card Interactions**:
  - Resting: `border border-black shadow-[2px_2px_0px_0px_rgba(0,0,0,0.2)] transition-all duration-100`
  - Hover: `hover:shadow-[1px_1px_0px_0px_rgba(0,0,0,0.2)] hover:translate-x-[1px] hover:translate-y-[1px]`
  - Active: `active:shadow-none active:translate-x-[2px] active:translate-y-[2px]`
- **Signature Color Calibration Bar**:
  - 20-segment color stripe bar in the header: `#c41e3a`, `#e85d04`, `#1e4d8c`, `#2563eb`, `#06b6d4`, `#d4a72c`, `#a855f7`, `#1e1e1e`, `#e5e5e5`, `#d4d4d4`, `#c4c4c4`, `#b4b4b4`, `#a4a4a4`, `#949494`, `#1e1e1e`, `#177a45`, `#2563eb`, `#7c3aed`, `#c41e3a`, `#e85d04`.

## 4. Components & Content Breakdown

### 4.1 Header & Navigation
- **Top Row**:
  - Brand: `Pedro Planel` / `pplanel` in bold monospace.
  - Color Stripe Bar: 20-segment colored bar spanning flex-1.
  - Top Badge: Neo-brutalist `GH ↗` button linking to `https://github.com/pplanel`.
- **Navigation Row**:
  - 5 segmented tactile tabs: `Home` (with `#177a45` green status dot), `About`, `Projects`, `Blog`, `Contact`.
  - Smooth-scrolling anchors linking to respective section IDs on the page (`#about`, `#projects`, `#blog`, `#contact`).

### 4.2 Hello / Intro Section (`#about`)
- **Header**: `Hello` with dotted divider.
- **Left Column (2fr)**:
  - Role subtitle: `Software Engineer / Open Source Enthusiast / Builder`.
  - Blockquote callout with thick left border (`border-l-4 border-black bg-gray-50`):
    > *"Pedro Planel — Building reliable systems, pragmatic tools, and clean digital experiences."*
  - Bio description focusing on software fundamentals, systems, and developer tooling.
  - Yellow CTA button: `Contact →` (`bg-[#d4a72c]`) scrolling to the contact section, flanked by `(Open for collaboration)` label.
- **Right Column (1fr) - Philosophy Card**:
  - Bordered box with 3px hard drop shadow:
    - Card header: `Philosophy`
    - Tenet 1: `Simplicity over complexity.` (accent left border)
    - Tenet 2: `Build for durability.` (accent left border)
    - Tenet 3: `Ship, measure, and iterate.` (accent left border)

### 4.3 Projects Section (`#projects`)
- **Header**: `Projects` with dotted divider.
- **Left Column (2fr)**:
  - Summary of engineering exploration, systems programming, and web tools.
  - Orange CTA button: `View All Projects →` / `View GitHub →` (`bg-[#f2572b] text-white`).
- **Right Column (1fr) - Featured Project**:
  - Interactive project card for **Conway's Game of Life**:
    - Direct link to `/game-of-life/`.
    - Title: `Game of Life`.
    - Description: WebAssembly and WebGL implementation of Conway's cellular automaton.
    - Card hover with tactile drop shadow.

### 4.4 Blog Section (`#blog`)
- **Header**: `Blog` with dotted divider.
- **Content**:
  - Description: Notes on software engineering, architecture, and technology.
  - Green CTA button: `View Posts →` (`bg-[#177a45] text-white`).

### 4.5 Contact Section (`#contact`)
- **Header**: `Contact` with dotted divider.
- **Table**: Monospace data table with blue left-accent border (`border-l-4 border-[#3498db]`):
  - Row 1: **Email** → `pplanel@gmail.com`
  - Row 2: **GitHub** → `github.com/pplanel`
  - Row 3: **Website** → `pplanel.dev`
  - Row 4: **Status** → `Available for select engineering projects`

### 4.6 Footer
- **Divider**: Solid black top border.
- **Copyright**: `© COPYRIGHT 2026, PEDRO PLANEL. ALL RIGHTS RESERVED.`
- **Links**: Monospace uppercase links to GitHub and Email.
- **Badges**:
  - Green `PROD` badge (`bg-[#177a45] text-white px-1.5 py-0.5`).
  - Bordered `V1.0.0` badge (`border border-black px-1.5 py-0.5`).

## 5. Responsive Design

- **Mobile View (< 640px)**:
  - Nav tabs use compact padding (`px-1.5 py-1.5`) and smaller text (`text-xs`).
  - Two-column grid layouts collapse into single-column vertical stacks.
  - Table cells wrap cleanly without overflow.
- **Desktop View (≥ 640px / 768px)**:
  - 2-column proportional grids (`2fr_1fr`).
  - Generous padding and crisp neo-brutalist shadows.

## 6. Verification Plan

1. **Local Server Verification**:
   - Serve site locally via `python3 -m http.server 8000`.
   - Inspect layout fidelity against `aprilnea.me/en` design tokens.
2. **Interactive Testing**:
   - Verify smooth-scrolling for all navigation tabs.
   - Verify tactile button press effects (hover and active translation + shadow collapse).
   - Test external links (GitHub, email `mailto:`, `/game-of-life/`).
3. **Integrity Checks**:
   - Confirm `CNAME` remains unmodified.
   - Confirm `/game-of-life/` loads and functions.
   - Confirm Umami analytics script is present.
