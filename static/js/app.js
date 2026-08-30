(function () {
  const LIB_KEY = "sipur.library.v1";

  function loadLib() {
    try {
      const raw = localStorage.getItem(LIB_KEY);
      const items = raw ? JSON.parse(raw) : [];
      return Array.isArray(items) ? items : [];
    } catch (_) {
      return [];
    }
  }

  function saveLib(items) {
    localStorage.setItem(LIB_KEY, JSON.stringify(items));
  }

  function upsertBook(meta) {
    if (!meta || !meta.token) return;
    const items = loadLib();
    if (items.some(function (x) { return x.token === meta.token; })) return;
    items.unshift(meta);
    saveLib(items.slice(0, 80));
  }

  const form = document.querySelector("[data-validate]");
  if (form) {
    form.addEventListener("submit", function (e) {
      const name = form.name.value.trim();
      const age = Number(form.age.value);
      const events = [form.event1.value, form.event2.value, form.event3.value].map(function (v) {
        return v.trim();
      });
      const problems = [];
      if (name.length < 2) problems.push("צריך שם, לפחות שתי אותיות.");
      if (!(age >= 3 && age <= 9)) problems.push("הגיל הוא בין 3 ל־9.");
      events.forEach(function (ev, i) {
        if (ev.length < 2) problems.push("צריך דבר " + (i + 1) + " מהשבוע.");
      });
      const old = form.parentNode.querySelector(".errors");
      if (old) old.remove();
      if (problems.length) {
        e.preventDefault();
        const ul = document.createElement("ul");
        ul.className = "errors";
        ul.setAttribute("role", "alert");
        problems.forEach(function (p) {
          const li = document.createElement("li");
          li.textContent = p;
          ul.appendChild(li);
        });
        form.parentNode.insertBefore(ul, form);
      }
    });
  }

  const reader = document.querySelector("[data-reader]");
  if (reader) {
    upsertBook({
      token: reader.dataset.token,
      title: reader.dataset.title,
      name: reader.dataset.name,
      age: reader.dataset.age,
      moral: reader.dataset.moral,
      cover: reader.dataset.cover,
    });

    const pages = Array.from(reader.querySelectorAll("[data-page]"));
    const dots = Array.from(reader.querySelectorAll("[data-goto]"));
    const prev = reader.querySelector("[data-prev]");
    const next = reader.querySelector("[data-next]");
    const bar = reader.querySelector("[data-progress]");
    let i = 0;

    function show(n) {
      i = Math.max(0, Math.min(pages.length - 1, n));
      pages.forEach(function (p, idx) {
        const on = idx === i;
        p.hidden = !on;
        p.classList.toggle("is-on", on);
      });
      dots.forEach(function (d, idx) {
        d.classList.toggle("is-on", idx === i);
      });
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === pages.length - 1;
      if (bar) bar.style.width = ((i + 1) / pages.length * 100) + "%";
    }

    if (prev) prev.addEventListener("click", function () { show(i - 1); });
    if (next) next.addEventListener("click", function () { show(i + 1); });
    dots.forEach(function (d) {
      d.addEventListener("click", function () { show(Number(d.getAttribute("data-goto"))); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") show(i + 1);
      if (e.key === "ArrowRight") show(i - 1);
    });

    let startX = null;
    reader.addEventListener("touchstart", function (e) {
      startX = e.changedTouches[0].clientX;
    }, { passive: true });
    reader.addEventListener("touchend", function (e) {
      if (startX == null) return;
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 40) {
        if (dx > 0) show(i + 1);
        else show(i - 1);
      }
      startX = null;
    });
    show(0);

    reader.querySelectorAll("[data-fade-art]").forEach(function (img) {
      function on() { img.classList.add("is-on"); }
      if (img.complete && img.naturalWidth) on();
      img.addEventListener("load", on);
      img.addEventListener("error", function () { img.remove(); });
    });

    const fb = reader.querySelector("[data-feedback]");
    if (fb) {
      fb.addEventListener("submit", function (e) {
        e.preventDefault();
        const rating = (fb.rating && fb.rating.value) || "";
        const note = (fb.note && fb.note.value) || "";
        const status = fb.querySelector("[data-feedback-status]");
        fetch("/api/feedback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            token: reader.dataset.token,
            rating: rating,
            note: note,
            template_id: reader.dataset.template,
          }),
        }).then(function (r) { return r.json(); }).then(function () {
          if (status) {
            status.hidden = false;
            status.textContent = "תודה. השמעתם לנו.";
          }
        }).catch(function () {
          if (status) {
            status.hidden = false;
            status.textContent = "לא הצלחנו לשמור עכשיו, נסו שוב.";
          }
        });
      });
    }
  }

  const grid = document.querySelector("[data-library]");
  const empty = document.querySelector("[data-library-empty]");
  if (grid) {
    const items = loadLib();
    if (!items.length) {
      if (empty) empty.hidden = false;
    } else {
      if (empty) empty.hidden = true;
      items.forEach(function (book) {
        const a = document.createElement("a");
        a.className = "book-card";
        a.href = "/s/" + encodeURIComponent(book.token);
        const img = document.createElement("img");
        img.alt = "";
        img.src = book.cover || "";
        img.addEventListener("error", function () {
          const ph = document.createElement("div");
          ph.className = "cover-ph";
          img.replaceWith(ph);
        });
        const body = document.createElement("div");
        body.className = "book-card-body";
        const h = document.createElement("h3");
        h.textContent = book.title || "סיפור";
        const meta = document.createElement("p");
        meta.textContent = book.name || "";
        const moral = document.createElement("p");
        moral.textContent = book.moral || "";
        body.appendChild(h);
        body.appendChild(meta);
        body.appendChild(moral);
        a.appendChild(img);
        a.appendChild(body);
        grid.appendChild(a);
      });
    }
  }

  const share = document.querySelector("[data-share]");
  const status = document.querySelector("[data-share-status]");
  if (share) {
    share.addEventListener("click", async function () {
      const url = window.location.href;
      try {
        if (navigator.share) {
          await navigator.share({ title: document.title, url: url });
        } else if (navigator.clipboard) {
          await navigator.clipboard.writeText(url);
          if (status) {
            status.hidden = false;
            status.textContent = "הקישור הועתק.";
          }
        }
      } catch (_) {
        if (status) {
          status.hidden = false;
          status.textContent = url;
        }
      }
    });
  }
})();
