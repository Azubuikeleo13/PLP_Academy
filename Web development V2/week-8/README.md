# Nova Studio — Multipage Website (Final Assignment)

A production-ready, responsive, accessible multipage website built with semantic HTML5, modern CSS, and vanilla JavaScript.

## 🔎 Purpose

Demonstrates best practices for structure, styling, interactivity, and deployment. The site represents a fictional design/dev studio, **Nova Studio**.

## 🧭 Information Architecture

- **Home** (`/index.html`): value proposition, key stats, primary CTAs
- **About** (`/about.html`): background, values, highlights
- **Services** (`/services.html`): offerings, pricing hints, FAQs
- **Work** (`/work.html`): portfolio grid
- **Contact** (`/contact.html`): Netlify-ready contact form, validation

Shared header/footer power consistent navigation and layout across all pages.

## 🗂 Project Structure

/ (root)
├─ index.html
├─ about.html
├─ services.html
├─ work.html
├─ contact.html
├─ css/
│ └─ style.css
├─ js/
│ └─ main.js
├─ images/
│ ├─ logo.svg
│ ├─ hero-bg.svg
│ └─ work-\*.svg
└─ README.md

markdown
Always show details

Copy code

## 🧰 Tech & Features

- **Semantic HTML5** with landmarks and accessible navigation (`aria-current`, skip link, focus states)
- **Responsive CSS** (mobile-first grid/utility patterns), CSS variables, light/dark support via prefers-color-scheme + toggle
- **Interactivity (JS)**: hamburger menu with proper ARIA, scroll-reveal animations (`IntersectionObserver`), client-side form validation
- **Performance**: system font stack, lazy images, minimal JS
- **Accessibility**: high-contrast focus, labels, helpful error messages

## ✅ Pre-deploy Checklist

- Validate HTML/CSS:
  - HTML: <https://validator.w3.org/>
  - CSS: <https://jigsaw.w3.org/css-validator/>
- Test responsive behavior at 360px, 768px, 1024px, 1280px
- Run Lighthouse (Chrome DevTools) for Performance, A11y, Best Practices, SEO

## 🚀 Deployment

You can deploy with any static host. Three options:

### 1) GitHub Pages

1. Create a new repo (e.g., `nova-studio-site`) and push all files.
2. In **Settings → Pages**, choose `Deploy from a branch` and select `main / root`.
3. The site will be live at: `https://<your-username>.github.io/nova-studio-site/`

> Tip: Because this site uses root-relative URLs (`/css/style.css`), GitHub Pages under a subpath will need either:
>
> - Use a _project_ site and switch paths to **relative** (`css/style.css`) _or_
> - Convert to a **user/org** site (repo named `<username>.github.io`) so root `/` works.

### 2) Netlify

1. Drag & drop the project folder into the Netlify dashboard _or_ connect your GitHub repo.
2. Build command: **none** (static). Publish directory: **/**.
3. The contact form already includes `netlify` attribute—Netlify will capture submissions.

### 3) Vercel

1. Import the repo in Vercel and deploy.
2. Framework preset: **Other** (no build). Output directory: `/`.

### Fixing pathing for subfolder deployments

If your host serves the site under a subpath (e.g., `/nova/`), change absolute asset links to relative:

- In HTML, switch `/css/style.css` → `css/style.css`
- Same for images and scripts (`/images/...` → `images/...`, `/js/main.js` → `js/main.js`)

## 🧪 Local testing

Just open `index.html` in a browser, or use a simple server:

📄 License
MIT — use it as a starter for your own portfolio or client work.
