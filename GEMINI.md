# AidBio Website Project

This repository contains the source code for the [AidBio](https://aidbio-ai.github.io/) official website, a specialized consultancy providing AI and Data Science solutions for Life Sciences and Agritech.

## Project Overview

The project is a high-performance, single-page static website designed to be hosted on GitHub Pages. It focuses on a clean, professional aesthetic with support for modern web features like dark mode and scroll-driven animations.

- **Purpose:** Professional landing page for AidBio.
- **Main Technologies:** 
  - **HTML5:** Semantic structure for SEO and accessibility.
  - **CSS3:** Custom styling using modern features like CSS Variables, Flexbox, Grid, and standard Transitions.
  - **Vanilla JavaScript:** Light-weight interactions, theme management, and scroll effects without external dependencies.
  - **Typography:** Inter and Playfair Display (via Google Fonts).

## Project Structure

```text
/
├── index.html        # Main entry point (HTML, CSS, and JS)
├── README.md         # Basic project identification
├── assets/           # Static assets
│   ├── aidbio_logo.svg
│   └── favicon.png
└── GEMINI.md         # Context for AI-assisted development
```

## Key Components

- **Theme Management:** A robust script in the `<head>` handles light/dark mode based on user preference or system settings.
- **Responsive Navigation:** A sticky navigation bar that adapts its appearance on scroll.
- **Reveal Animations:** Uses the `IntersectionObserver` API to animate elements as they enter the viewport.
- **Hero Effects:** Dynamic scaling and opacity adjustments for the hero logo based on scroll position.

## Development and Deployment

### Running Locally

Since this is a static project with no build step, you can run it using any simple HTTP server:

```bash
# Using Python (built-in)
python3 -m http.server 8000

# Using Node.js (npx)
npx serve .

# Or simply open index.html in your preferred browser.
```

### Building

There is no build process (Transpilation, Minification, or Bundling) currently configured for this project. The source code in `index.html` is served directly.

### Deployment

Deployment is handled automatically via GitHub Actions or GitHub Pages settings when changes are pushed to the main branch.

## Development Conventions

- **Surgical Edits:** When modifying `index.html`, ensure that CSS and JS changes are kept within their respective `<style>` and `<script>` blocks unless refactoring into external files is requested.
- **Theming:** Use CSS variables (e.g., `--bg-primary`, `--text-main`) for all colors to maintain theme compatibility.
- **Performance:** Keep external dependencies to a minimum to ensure fast load times.
- **Accessibility:** Ensure semantic HTML and proper `aria` attributes are maintained.
