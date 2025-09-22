/**
 * Nova Studio — Main JS
 * - Mobile menu toggle with ARIA
 * - Theme toggle (persisted)
 * - Scroll reveal (IntersectionObserver)
 * - Client-side form validation
 */
(function () {
  const nav = document.querySelector(".nav-links");
  const menuBtn = document.querySelector(".menu-toggle");
  const themeBtn = document.querySelector(".theme-toggle");

  // Mobile menu
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", () => {
      const isOpen = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", String(isOpen));
      if (isOpen) nav.querySelector("a")?.focus();
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open");
        menuBtn.setAttribute("aria-expanded", "false");
        menuBtn.focus();
      }
    });
  }

  // Theme toggle (prefers-color-scheme aware)
  const saved = localStorage.getItem("theme");
  if (saved === "light") document.documentElement.classList.add("theme-light");
  if (saved === "dark") document.documentElement.classList.add("theme-dark");

  function applyTheme(mode) {
    document.documentElement.classList.remove("theme-light", "theme-dark");
    if (mode) document.documentElement.classList.add(`theme-${mode}`);
    localStorage.setItem("theme", mode || "");
  }

  themeBtn?.addEventListener("click", () => {
    const isDark = document.documentElement.classList.contains("theme-dark");
    const isLight = document.documentElement.classList.contains("theme-light");
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const current = isDark ? "dark" : isLight ? "light" : prefersDark ? "dark" : "light";
    const next = current === "dark" ? "light" : "dark";
    applyTheme(next);
  });

  // Scroll reveal
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  // Contact form validation
  const form = document.querySelector('form[data-validate="contact"]');
  if (form) {
    form.addEventListener("submit", (e) => {
      let valid = true;
      const name = form.querySelector("#name");
      const email = form.querySelector("#email");
      const message = form.querySelector("#message");

      form.querySelectorAll(".error").forEach((el) => (el.textContent = ""));

      if (!name.value.trim()) {
        valid = false;
        form.querySelector('[data-error-for="name"]').textContent = "Please enter your name.";
      }
      const emailValue = email.value.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailValue)) {
        valid = false;
        form.querySelector('[data-error-for="email"]').textContent = "Enter a valid email address.";
      }
      if (!message.value.trim() || message.value.trim().length < 12) {
        valid = false;
        form.querySelector('[data-error-for="message"]').textContent =
          "Message should be at least 12 characters.";
      }
      if (!valid) e.preventDefault();
    });
  }
})();
