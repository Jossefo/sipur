(function () {
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
      const old = form.querySelector(".errors");
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
    const pages = Array.from(reader.querySelectorAll("[data-page]"));
    const dots = Array.from(reader.querySelectorAll("[data-goto]"));
    const prev = reader.querySelector("[data-prev]");
    const next = reader.querySelector("[data-next]");
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
