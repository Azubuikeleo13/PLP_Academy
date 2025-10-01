# VibeCoding — Mini E-Learning Platform 🎓

A tiny, polished e-learning prototype built with **HTML, CSS, and vanilla JavaScript**. Learners can browse courses, view details, and mark courses as completed. Includes a lightweight login/signup demo (local only) and an optional Node/Express backend.

> Built for the **VibeCoding Week 1** assignment.

---

## ✨ Features

- **Course catalog** (3+ example courses)
- **Course details view** with lessons + estimated time
- **Mark as completed** (and reset progress)
- **Search** across titles, subtitles, levels, and tags
- **Demo auth** (email + display name) — stored locally
- **Per-user progress** via `localStorage`
- **Responsive UI** with light/dark/auto theme
- **Accessible** semantics, focus management, and ARIA touches
- **Hash-based routing** (`#/courses`, `#/course/:id`, `#/profile`)

---

## 🧱 Project Structure

vibecoding-elearn/
├─ index.html
├─ styles.css
├─ app.js
└─ optional-server/
├─ server.js
└─ db.json

yaml

- **Frontend** is fully static — open `index.html` and go.
- **optional-server/** provides a tiny Express API for courses (read-only).

---

## 🚀 Quick Start (No Backend)

1. **Download/clone** this folder.
2. Open `index.html` directly in your browser.

> Tip: Use a static server for cleaner routing & CORS:
>
> - Python: `python -m http.server 3000`
> - Node: `npx serve .`
>   Visit `http://localhost:3000`

---

## 🧪 Optional: Run the Mini Backend

This is not required for the assignment, but handy if you want a real `/api`:

```bash
cd optional-server
npm init -y
npm i express
node server.js
# Server: http://localhost:5173
Serves the static frontend from the parent folder.

Exposes:

GET /api/courses → list courses

GET /api/courses/:id → course by id

If you want the frontend to fetch from the API instead of the in-file array:

Replace COURSES usage in app.js with:



const COURSES = await fetch('/api/courses').then(r => r.json());
Wrap initial render in an async init:



document.addEventListener("DOMContentLoaded", async () => {
  // ... loadState();
  window.COURSES = await fetch('/api/courses').then(r => r.json());
  render();
  // ...rest of wiring
});
👩‍💻 Usage Guide
Browse courses: Home route #/courses

View details: Click View

Mark completed: Click Mark as Completed on a card or in detail view

Search: Use the search icon in the header

Login/Signup: Click Login → provide email + name (local only)

Profile: Shows your courses; you can Log out

Keyboard Tips

Tab / Shift+Tab to navigate controls

Enter to activate focused button

Focus jumps to main content on route change for screen readers

🛠 Tech Choices
No build tools (fast to run/evaluate)

Vanilla JS SPA with a micro-router (hash routes)

LocalStorage for user + progress state

Progressive enhancement and semantic HTML

🔐 Data & Persistence
User { email, name } saved as vc:user

Progress saved per email under vc:progress

Theme preference saved as vc:theme

Clear data by removing those keys in DevTools or using Log out (removes user only).

🧩 Assignment Checklist
 View a list of courses (≥ 3)

 See course details when clicked

 Mark course as completed

 (Optional) Login/Signup

 Clean, responsive UI with accessible semantics

 Progress persists per user

🧰 Customization
Add more courses: edit COURSES in app.js (or optional-server/db.json)

Tweak theme: update CSS variables in styles.css

Change routes: see routes map in app.js

Swap storage: replace LocalStorage calls with API requests

🐞 Troubleshooting
Nothing loads after editing JS
Check the browser console for syntax errors (missing commas/braces).

Routing looks broken when opening index.html directly
Use a local static server (see Quick Start tip).

Progress doesn’t save
Ensure you’re logged in (demo auth). Progress is saved per email.

📦 Deployment
Any static host works:

GitHub Pages, Netlify, Vercel (static), Render (static)

For the optional server, deploy Node on Render/railway/Heroku-like platforms and serve the static files.

📝 Scripts & Commands
None required. Suggested dev helpers:

bash

# Static server (Node)
npx serve .

# Static server (Python)
python -m http.server 3000
🧭 Accessibility Notes
Landmarks: <header>, <main>, <footer>

Focus management: main region receives focus on navigation

Form inputs have labels; buttons have titles or visible text

Color scheme honors prefers-color-scheme and user toggle

🤝 Contributing
PRs welcome for:

More course seeds

i18n, service worker (offline), or tests

Real user auth + database

📄 License
MIT — do whatever, just keep the notice.

🙌 Credits
Crafted for VibeCoding Week 1 with ❤️
UI & code by you + a little AI pair-programming boost.
```
