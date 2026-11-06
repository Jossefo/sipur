(function () {
  const skipLink = document.querySelector(".skip-link");
  if (skipLink) skipLink.addEventListener("click", event => {
    event.preventDefault();
    const main = document.querySelector("main");
    main.tabIndex = -1; main.focus(); main.scrollIntoView();
  });
  function initSipur() {
  "use strict";
  const IS_STATIC = document.documentElement.dataset.static === "true";
  const STATIC_BASE = new URL("./", location.href);
  const LIB_KEY = "sipur.library.v1";
  function loadLib() {
    try {
      const items = JSON.parse(localStorage.getItem(LIB_KEY) || "[]");
      return Array.isArray(items) ? items.filter(b => b && typeof b.token === "string" && b.token.length <= 12000) : [];
    } catch (_) { return []; }
  }
  function saveLib(items) {
    try { localStorage.setItem(LIB_KEY, JSON.stringify(items)); return true; }
    catch (_) { return false; }
  }
  function announce(el, message) {
    if (el) { el.hidden = false; el.textContent = message; }
  }
  const form = document.querySelector("[data-validate]");
  if (form) {
    form.addEventListener("submit", function (e) {
      const fields = form.elements;
      const problems = [];
      if (fields.namedItem("name").value.trim().length < 2) problems.push("צריך שם, לפחות שתי אותיות.");
      const age = Number(fields.namedItem("age").value);
      if (!(age >= 3 && age <= 9)) problems.push("הגיל הוא בין 3 ל־9.");
      [1, 2, 3].forEach(n => {
        if (fields.namedItem("event" + n).value.trim().length < 2) problems.push("צריך לפחות שתי אותיות ברגע " + n + ".");
      });
      const old = form.parentNode.querySelector(".errors");
      if (old) old.remove();
      if (problems.length) {
        e.preventDefault();
        const ul = document.createElement("ul");
        ul.className = "errors"; ul.setAttribute("role", "alert"); ul.tabIndex = -1;
        problems.forEach(p => { const li = document.createElement("li"); li.textContent = p; ul.appendChild(li); });
        form.before(ul); ul.focus();
      } else {
        const submit = form.querySelector('button[type="submit"]');
        submit.disabled = true;
        announce(form.querySelector("[data-form-status]"), "עוד רגע, והסיפור שלהם מוכן…");
      }
    });
    window.addEventListener("pageshow", () => { form.querySelector('button[type="submit"]').disabled = false; });
  }
  const reader = document.querySelector("[data-reader]");
  if (reader) {
    if (reader.dataset.demo !== "true") {
      const items = loadLib();
      if (!items.some(b => b.token === reader.dataset.token)) {
        items.unshift({token:reader.dataset.token,title:reader.dataset.title,name:reader.dataset.name,
          age:reader.dataset.age,moral:reader.dataset.moral,cover:reader.dataset.cover,template:reader.dataset.template,fingerprint:reader.dataset.fingerprint});
        if (!saveLib(items.slice(0, 80))) announce(reader.querySelector("[data-share-status]"), "לא ניתן לשמור בספרייה בדפדפן הזה. אפשר להעתיק קישור כדי לשמור את הסיפור.");
      }
    }
    const pages = Array.from(reader.querySelectorAll("[data-page]"));
    const dots = Array.from(reader.querySelectorAll("[data-goto]"));
    const prev = reader.querySelector("[data-prev]");
    const next = reader.querySelector("[data-next]");
    const bar = reader.querySelector("[data-progress]");
    let index = 0;
    function show(n) {
      index = Math.max(0, Math.min(pages.length - 1, n));
      pages.forEach((p, i) => { p.hidden = i !== index; p.classList.toggle("is-on", i === index); });
      dots.forEach((d, i) => { d.classList.toggle("is-on", i === index); d.setAttribute("aria-current", i === index ? "step" : "false"); });
      prev.disabled = index === 0; next.disabled = index === pages.length - 1;
      if (bar) bar.style.width = ((index + 1) / pages.length * 100) + "%";
      announce(reader.querySelector("[data-page-status]"), "עמוד " + (index + 1) + " מתוך " + pages.length);
    }
    prev.addEventListener("click", () => show(index - 1));
    next.addEventListener("click", () => show(index + 1));
    dots.forEach(d => d.addEventListener("click", () => show(Number(d.dataset.goto))));
    document.addEventListener("keydown", function (e) {
      if (e.target.closest("input, textarea, select, button, a, [contenteditable]")) return;
      if (e.key === "ArrowLeft") { e.preventDefault(); show(index + 1); }
      if (e.key === "ArrowRight") { e.preventDefault(); show(index - 1); }
    });
    let start = null;
    const surface = reader.querySelector(".book-page").parentNode;
    surface.addEventListener("touchstart", e => {
      start = e.target.closest(".page-art") ? {x:e.changedTouches[0].clientX,y:e.changedTouches[0].clientY} : null;
    }, {passive:true});
    surface.addEventListener("touchend", e => {
      if (!start) return;
      const dx = e.changedTouches[0].clientX - start.x, dy = e.changedTouches[0].clientY - start.y;
      if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.5) show(index + (dx > 0 ? 1 : -1));
      start = null;
    }, {passive:true});
    show(0);
    reader.querySelectorAll("[data-fade-art]").forEach(img => {
      const reveal = () => img.classList.add("is-on");
      if (img.complete && img.naturalWidth) reveal();
      img.addEventListener("load", reveal); img.addEventListener("error", () => img.remove());
    });
    reader.querySelector("[data-print]").addEventListener("click", () => window.print());
    const night = reader.querySelector("[data-reading-mode]");
    night.addEventListener("click", () => {
      const on = document.body.classList.toggle("night-mode");
      night.setAttribute("aria-pressed", String(on)); night.textContent = on ? "מצב יום ☀" : "מצב לילה ☾";
    });
    const fb = reader.querySelector("[data-feedback]");
    fb.addEventListener("submit", async e => {
      e.preventDefault();
      const button = fb.querySelector('button[type="submit"]'), status = fb.querySelector("[data-feedback-status]");
      const rating = new FormData(fb).get("rating");
      if (!rating) return;
      button.disabled = true;
      try {
        if (IS_STATIC) {
          const entries = JSON.parse(localStorage.getItem("sipur.feedback.v1") || "[]");
          const items = Array.isArray(entries) ? entries : [];
          items.push({rating:rating,template_id:reader.dataset.template});
          localStorage.setItem("sipur.feedback.v1",JSON.stringify(items.slice(-100)));
          announce(status, "תודה! המשוב נשמר רק במכשיר הזה.");
          return;
        }
        const response = await fetch("/api/feedback", {method:"POST",headers:{"Content-Type":"application/json"},
          body:JSON.stringify({rating:rating,template_id:reader.dataset.template})});
        if (!response.ok) throw new Error("feedback failed");
        announce(status, "תודה! המשוב שלכם עוזר לנו להשתפר.");
      } catch (_) { announce(status, "לא הצלחנו לשלוח עכשיו. אפשר לנסות שוב."); button.disabled = false; }
    });
    reader.querySelector("[data-share]").addEventListener("click", async () => {
      const status = reader.querySelector("[data-share-status]");
      const url = location.href;
      try {
        if (navigator.share) await navigator.share({title:document.title,url:url});
        else if (navigator.clipboard) { await navigator.clipboard.writeText(url); announce(status, "הקישור הועתק. כל מי שמקבל אותו יכול לקרוא את הסיפור."); }
        else announce(status, "אפשר להעתיק את הקישור משורת הכתובת.");
      } catch (error) {
        if (error.name !== "AbortError") announce(status, "אפשר להעתיק את הקישור משורת הכתובת.");
      }
    });
  }
  const grid = document.querySelector("[data-library]");
  if (grid) {
    const empty = document.querySelector("[data-library-empty]");
    function renderLibrary() {
      const items = loadLib(); grid.replaceChildren(); empty.hidden = items.length > 0;
      items.forEach(book => {
        const wrap = document.createElement("div"); wrap.className = "book-card-wrap";
        const a = document.createElement("a"); a.className = "book-card"; a.href = IS_STATIC ? new URL("reader.html", STATIC_BASE).href + "#" + book.token : "/s/" + encodeURIComponent(book.token);
        const img = document.createElement("img"); img.alt = ""; img.loading = "lazy";
        // Old libraries may contain external image URLs; never request those again.
        let cover = IS_STATIC ? new URL("static/images/bedtime-world.webp", STATIC_BASE).href : "/static/images/bedtime-world.webp";
        if (typeof book.cover === "string") {
          try {
            const candidate = new URL(book.cover, location.href);
            if (candidate.origin === location.origin && /\/static\/images\/[a-z-]+\.webp$/.test(candidate.pathname)) cover = candidate.href;
          } catch (_) { /* Keep bundled fallback. */ }
        }
        img.src = cover;
        img.addEventListener("error", () => { const ph = document.createElement("div"); ph.className = "cover-ph"; img.replaceWith(ph); });
        const body = document.createElement("div"); body.className = "book-card-body";
        const title = document.createElement("h3"); title.textContent = book.title || "סיפור";
        const name = document.createElement("p"); name.textContent = book.name || "";
        const moral = document.createElement("p"); moral.textContent = book.moral || "";
        body.append(title, name, moral); a.append(img, body);
        const remove = document.createElement("button"); remove.type = "button"; remove.className = "remove-book"; remove.textContent = "הסרה";
        remove.setAttribute("aria-label", "להסיר מהספרייה: " + (book.title || "סיפור"));
        remove.addEventListener("click", () => {
          if (saveLib(loadLib().filter(b => b.token !== book.token))) { renderLibrary(); announce(document.querySelector("[data-library-status]"), "הספר הוסר מהספרייה במכשיר הזה."); }
          else announce(document.querySelector("[data-library-status]"), "לא הצלחנו לעדכן את הספרייה בדפדפן הזה.");
        });
        wrap.append(a, remove); grid.appendChild(wrap);
      });
    }
    renderLibrary();
  }
  }
  if (document.documentElement.dataset.static === "true") {
    if (window.sipurReady) initSipur();
    else document.addEventListener("sipur:ready", initSipur, {once:true});
  } else initSipur();
})();
