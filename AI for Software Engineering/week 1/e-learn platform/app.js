/* VibeCoding Mini E-Learning — Frontend SPA (no build tools) */

const $ = (sel, el = document) => el.querySelector(sel);
const $$ = (sel, el = document) => Array.from(el.querySelectorAll(sel));

/** ------------------ Data (could be replaced by API) ------------------ **/
const COURSES = [
  {
    id: "html-foundations",
    title: "HTML Foundations",
    subtitle: "Semantics, structure, and accessible markup.",
    tags: ["Beginner", "Web"],
    level: "Beginner",
    estMins: 60,
    lessons: [
      { id: "h1", title: "Intro to the Web", mins: 8 },
      { id: "h2", title: "Semantic HTML", mins: 15 },
      { id: "h3", title: "Forms & Inputs", mins: 18 },
      { id: "h4", title: "Media & Accessibility", mins: 19 },
    ],
    description:
      "Master the building blocks of the web with clean, semantic HTML that screen readers and search engines love.",
  },
  {
    id: "css-layouts",
    title: "Modern CSS Layouts",
    subtitle: "Flexbox, Grid, and responsive strategies.",
    tags: ["Intermediate", "CSS"],
    level: "Intermediate",
    estMins: 75,
    lessons: [
      { id: "c1", title: "The Box Model", mins: 10 },
      { id: "c2", title: "Flexbox Essentials", mins: 20 },
      { id: "c3", title: "CSS Grid in Practice", mins: 25 },
      { id: "c4", title: "Responsive Design Patterns", mins: 20 },
    ],
    description:
      "Lay out complex interfaces with confidence using Flexbox and Grid, with mobile-first techniques baked in.",
  },
  {
    id: "js-fundamentals",
    title: "JavaScript Fundamentals",
    subtitle: "Data types, DOM, events, and state.",
    tags: ["Beginner", "JavaScript"],
    level: "Beginner",
    estMins: 90,
    lessons: [
      { id: "j1", title: "Language Basics", mins: 20 },
      { id: "j2", title: "DOM & Events", mins: 25 },
      { id: "j3", title: "Asynchronous JS", mins: 22 },
      { id: "j4", title: "State & LocalStorage", mins: 23 },
    ],
    description:
      "Go from zero to shipping interactive features — the essentials you actually use as a web dev.",
  },
  {
    id: "ai-assist",
    title: "AI-Assisted Coding",
    subtitle: "Prompting, pair programming, and guardrails.",
    tags: ["Productivity", "AI"],
    level: "All levels",
    estMins: 45,
    lessons: [
      { id: "a1", title: "Prompt Basics", mins: 10 },
      { id: "a2", title: "Debugging with AI", mins: 12 },
      { id: "a3", title: "Refactor & Docs", mins: 11 },
      { id: "a4", title: "Ethics & Safety", mins: 12 },
    ],
    description:
      "Use AI effectively as your coding copilot — speed up without sacrificing code quality.",
  },
];

/** ------------------ State & Persistence ------------------ **/
const LS_KEYS = {
  USER: "vc:user",
  PROGRESS: "vc:progress", // { [email]: { [courseId]: 0..100 } }
};

const state = {
  user: null, // { email, name }
  progress: {}, // user-specific map
  route: location.hash || "#/courses",
  theme: sessionStorage.getItem("vc:theme") || "auto",
};

/** ------------------ Auth (demo) ------------------ **/
function openAuth() {
  const dlg = $("#authModal");
  $("#authTitle").textContent = "Welcome to VibeCoding";
  $("#authEmail").value = "";
  $("#authName").value = "";
  dlg.showModal();
}
function updateAuthButton() {
  const btn = $("#authBtn");
  if (state.user) {
    btn.textContent = "Profile";
    btn.onclick = () => navigate("#/profile");
  } else {
    btn.textContent = "Login";
    btn.onclick = openAuth;
  }
}

function loadState() {
  const u = sessionStorage.getItem(LS_KEYS.USER);
  if (u) state.user = JSON.parse(u);

  const p = sessionStorage.getItem(LS_KEYS.PROGRESS);
  if (p) state.progress = JSON.parse(p);

  applyTheme(state.theme);
}

function saveUser(user) {
  state.user = user;
  sessionStorage.setItem(LS_KEYS.USER, JSON.stringify(user));
  // create progress bucket if missing
  if (!state.progress[user.email]) {
    state.progress[user.email] = {};
    saveProgress();
  }
  updateAuthButton();
}

function saveProgress() {
  sessionStorage.setItem(LS_KEYS.PROGRESS, JSON.stringify(state.progress));
}

function userProgressFor(courseId) {
  const email = state.user?.email;
  if (!email) return 0;
  return state.progress[email]?.[courseId] ?? 0;
}

function setUserProgress(courseId, percent) {
  const email = state.user?.email;
  if (!email) return;
  state.progress[email] = state.progress[email] || {};
  state.progress[email][courseId] = Math.max(0, Math.min(100, percent));
  saveProgress();
}

/** ------------------ Rendering Helpers ------------------ **/
function h(tag, attrs = {}, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") el.className = v;
    else if (k.startsWith("on") && typeof v === "function")
      el.addEventListener(k.slice(2).toLowerCase(), v);
    else if (v !== false && v != null) el.setAttribute(k, v === true ? "" : v);
  }
  for (const c of children.flat()) {
    if (c == null) continue;
    el.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return el;
}

function notFound() {
  return h(
    "div",
    { class: "empty" },
    h("p", {}, "That page doesn’t exist. "),
    h("a", { href: "#/courses" }, "Back to courses")
  );
}

/** ------------------ Views ------------------ **/
function CoursesView() {
  const wrapper = h("section", {});
  const grid = h("div", { class: "grid", id: "courseGrid" });

  // filter by search
  const q = ($("#searchInput")?.value || "").trim().toLowerCase();
  const data = COURSES.filter((c) =>
    [c.title, c.subtitle, c.level, ...(c.tags || [])].join(" ").toLowerCase().includes(q)
  );

  if (data.length === 0) {
    wrapper.appendChild(
      h("div", { class: "empty" }, "No matching courses. Try a different search.")
    );
    return wrapper;
  }

  for (const course of data) {
    const card = renderCourseCard(course);
    grid.appendChild(card);
  }

  wrapper.appendChild(grid);
  return wrapper;
}

function requireAuth(fn) {
  if (state.user) return fn();
  openAuth();
}

function renderCourseCard(course) {
  const tpl = $("#courseCardTpl");
  const node = tpl.content.firstElementChild.cloneNode(true);

  $(".title", node).textContent = course.title;
  $(".subtitle", node).textContent = course.subtitle;

  const badges = $(".badge-list", node);
  (course.tags || []).forEach((t) => badges.appendChild(h("span", { class: "badge" }, t)));

  $(".lessons", node).textContent = `${course.lessons.length} lessons`;
  $(".level", node).textContent = course.level;
  $(".est", node).textContent = `${course.estMins} min est.`;

  const pct = userProgressFor(course.id);
  $("progress", node).value = pct;
  $(".progress-label", node).textContent = `${pct}% complete`;

  $(".view-btn", node).addEventListener("click", () => {
    navigate(`#/course/${course.id}`);
  });

  $(".complete-btn", node).addEventListener("click", () => {
    requireAuth(() => {
      setUserProgress(course.id, 100);
      flash(`Marked “${course.title}” as completed ✅`);
      render();
    });
  });

  return node;
}

function CourseDetailView(id) {
  const course = COURSES.find((c) => c.id === id);
  if (!course) return notFound();

  const pct = userProgressFor(course.id);
  const hero = h(
    "section",
    { class: "detail-hero" },
    h(
      "div",
      { class: "left" },
      h("h2", {}, course.title),
      h("p", {}, course.description),
      h(
        "div",
        { class: "meta" },
        h("span", { class: "chip" }, `${course.lessons.length} lessons`),
        h("span", { class: "chip" }, course.level),
        h("span", { class: "chip" }, `${course.estMins} min est.`)
      )
    ),
    h(
      "div",
      { class: "actions" },
      h("button", { class: "btn ghost", onClick: () => navigate("#/courses") }, "← Back"),
      h(
        "button",
        {
          class: "btn",
          onClick: () => {
            requireAuth(() => {
              setUserProgress(course.id, 0);
              flash("Progress reset.");
              render();
            });
          },
        },
        "Reset"
      ),
      h(
        "button",
        {
          class: "btn primary",
          onClick: () => {
            requireAuth(() => {
              setUserProgress(course.id, 100);
              flash("Marked as completed ✅");
              render();
            });
          },
        },
        "Mark Completed"
      )
    )
  );

  const lessons = h(
    "section",
    {},
    h("h3", {}, "Lessons"),
    h(
      "div",
      { class: "lesson-list" },
      course.lessons.map((ls, i) =>
        h(
          "div",
          { class: "lesson" },
          h("span", { class: "dot", "aria-hidden": "true" }),
          h(
            "div",
            {},
            h("div", { class: "title" }, `${i + 1}. ${ls.title}`),
            h("div", { class: "muted" }, `ID: ${ls.id}`)
          ),
          h("span", { class: "time" }, `${ls.mins} min`)
        )
      )
    )
  );

  const progress = h(
    "div",
    { class: "progress" },
    h("progress", { value: pct, max: 100 }),
    h("span", { class: "progress-label" }, `${pct}% complete`)
  );

  const main = h("section", { class: "course-detail" }, hero, progress, lessons);
  return main;
}

function ProfileView() {
  if (!state.user) {
    return h(
      "div",
      { class: "empty" },
      h("p", {}, "You’re not logged in."),
      h("div", {}, h("button", { class: "btn primary", onClick: openAuth }, "Login / Sign up"))
    );
  }

  const email = state.user.email;
  const prog = state.progress[email] || {};
  const items = COURSES.map((c) => ({
    course: c,
    pct: prog[c.id] ?? 0,
  }));

  const grid = h(
    "div",
    { class: "grid" },
    items.map(({ course, pct }) => renderCourseCard(course))
  );

  return h(
    "section",
    {},
    h(
      "div",
      { class: "detail-hero" },
      h("div", {}, h("h2", {}, `Hi, ${state.user.name}`), h("p", { class: "muted" }, email)),
      h(
        "div",
        { class: "actions" },
        h(
          "button",
          {
            class: "btn",
            onClick: () => {
              sessionStorage.removeItem(LS_KEYS.USER);
              state.user = null;
              updateAuthButton();
              flash("Logged out.");
              render();
            },
          },
          "Log out"
        )
      )
    ),
    h("h3", {}, "Your Courses"),
    grid
  );
}

/** ------------------ Router ------------------ **/
const routes = {
  "#/courses": () => CoursesView(),
  "#/profile": () => ProfileView(),
  "#/course/:id": (params) => CourseDetailView(params.id),
};

function matchRoute(hash) {
  for (const pattern of Object.keys(routes)) {
    if (!pattern.includes(":")) {
      if (hash === pattern) return { handler: routes[pattern], params: {} };
    } else {
      const re = new RegExp("^" + pattern.replace(/:[^/]+/g, "([^/]+)") + "$");
      const m = hash.match(re);
      if (m) {
        const keys = (pattern.match(/:([^/]+)/g) || []).map((s) => s.slice(1));
        const params = Object.fromEntries(keys.map((k, i) => [k, m[i + 1]]));
        return { handler: routes[pattern], params };
      }
    }
  }
  return null;
}

function updateHeaderForRoute() {
  const isCourses = state.route.startsWith("#/courses");
  const isProfile = state.route.startsWith("#/profile");
  const isCourseDetail = state.route.startsWith("#/course/");

  // Search visibility (only on Courses)
  const searchToggle = document.getElementById("searchToggle");
  const searchBar = document.getElementById("searchBar");
  const searchInput = document.getElementById("searchInput");

  if (isCourses) {
    searchToggle?.classList.remove("hidden");
  } else {
    // hide + clear search when leaving the catalog
    searchToggle?.classList.add("hidden");
    searchBar?.classList.add("hidden");
    if (searchInput && searchInput.value) {
      searchInput.value = "";
    }
  }

  // Update page title for context
  if (isCourses) document.title = "VibeCoding — Courses";
  else if (isProfile) document.title = "VibeCoding — Your Profile";
  else if (isCourseDetail) document.title = "VibeCoding — Course Details";
  else document.title = "VibeCoding";

  // Ensure auth button reflects state
  updateAuthButton?.();
}

function render() {
  const mount = $("#app");
  mount.innerHTML = "";
  const match = matchRoute(state.route);
  const view = match ? match.handler(match.params) : notFound();
  mount.appendChild(view);
  mount.focus();
  updateHeaderForRoute();
}

/** ------------------ Utilities ------------------ **/
function navigate(hash) {
  if (hash === state.route) return;
  state.route = hash;
  history.pushState({}, "", hash);
  render();
}

function flash(msg, ms = 1800) {
  const el = h(
    "div",
    {
      style: `
    position:fixed; left:50%; top:12px; transform:translateX(-50%);
    background:var(--panel); color:var(--text); border:1px solid var(--border);
    padding:.6rem .9rem; border-radius:.6rem; box-shadow:var(--shadow); z-index:9999;
  `,
    },
    msg
  );
  document.body.appendChild(el);
  setTimeout(() => el.remove(), ms);
}

function applyTheme(choice) {
  // choice: "auto" | "light" | "dark"
  const mql = window.matchMedia("(prefers-color-scheme: dark)");
  const dark = choice === "dark" || (choice === "auto" && mql.matches);
  document.documentElement.style.colorScheme = dark ? "dark" : "light";
  sessionStorage.setItem("vc:theme", choice);
}

/** ------------------ Event Wiring ------------------ **/
window.addEventListener("hashchange", () => {
  state.route = location.hash || "#/courses";
  render();
});

document.addEventListener("DOMContentLoaded", () => {
  $("#year").textContent = new Date().getFullYear();
  loadState();
  state.route = location.hash || "#/courses";
  render();

  // header controls
  $("#themeToggle").addEventListener("click", () => {
    const current = sessionStorage.getItem("vc:theme") || "auto";
    const next = current === "auto" ? "dark" : current === "dark" ? "light" : "auto";
    applyTheme(next);
    flash(`Theme: ${next}`);
  });

  $("#searchToggle").addEventListener("click", () => {
    const bar = $("#searchBar");
    const expanded = bar.classList.toggle("hidden");
    $("#searchToggle").setAttribute("aria-expanded", (!expanded).toString());
    if (!expanded) $("#searchInput").focus();
  });

  $("#searchInput").addEventListener("input", () => render());

  updateAuthButton();

  // auth modal handling
  const dlg = $("#authModal");
  $("#authForm").addEventListener("close", (e) => {
    // dialog close event does not carry value; use submit listener below
  });
  $("#authForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const email = $("#authEmail").value.trim().toLowerCase();
    const name = $("#authName").value.trim();
    if (!email || !name) return;
    saveUser({ email, name });
    $("#authModal").close();
    flash(`Welcome, ${name}!`);
    render();
  });
});
