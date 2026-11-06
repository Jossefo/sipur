/* GitHub Pages adapter. Python remains the single source of story-generation logic. */
(function () {
  "use strict";
  const base = new URL("./", location.href);
  const root = document.documentElement;
  let worker, serial = 0;
  const pending = new Map();
  function runEngine(request) {
    if (!worker) {
      worker = new Worker(new URL("static/js/engine-worker.js", base), {type:"module"});
      worker.onmessage = ({data}) => {
        const task = pending.get(data.id);
        if (task) { pending.delete(data.id); data.error ? task.reject(new Error(data.error)) : task.resolve(data.result); }
      };
      worker.onerror = () => {
        pending.forEach(task => task.reject(new Error("לא הצלחנו לטעון את עולם הסיפורים. בדקו את החיבור ונסו שוב.")));
        pending.clear(); worker.terminate(); worker = null;
      };
    }
    return new Promise((resolve, reject) => {
      const id = ++serial;
      const timer = setTimeout(() => { pending.delete(id); reject(new Error("הטעינה ארכה יותר מדי. בדקו את החיבור ונסו שוב.")); }, 120000);
      pending.set(id, {resolve:result => {clearTimeout(timer);resolve(result);},reject:error => {clearTimeout(timer);reject(error);}});
      worker.postMessage({...request,id,base:base.href});
    });
  }
  function ready() { window.sipurReady = true; document.dispatchEvent(new Event("sipur:ready")); }
  function status(message) {
    const el = document.querySelector("[data-engine-status]");
    if (el) { el.hidden = false; el.textContent = message; }
  }
  function bookArt(book, index) {
    const page = book.story.pages[index], art = book.art[index];
    const section = document.createElement("section");
    section.className = "book-page" + (index === 0 ? " is-on" : ""); section.dataset.page = index; section.hidden = index !== 0;
    const visual = document.createElement("div"); visual.className = "page-art";
    const svg = document.createElement("div"); svg.className = "art-svg";
    // Only our Python SVG renderer produces this value; shared payloads cannot supply SVG markup.
    const parsed = new DOMParser().parseFromString(art.svg, "image/svg+xml");
    if (parsed.documentElement.localName === "svg") svg.appendChild(document.importNode(parsed.documentElement, true));
    visual.appendChild(svg);
    if (art.image && /^\/static\/images\/[a-z-]+\.webp$/.test(art.image)) {
      const img = document.createElement("img"); img.className = "art-img"; img.alt = ""; img.dataset.fadeArt = "";
      img.loading = index === 0 ? "eager" : "lazy"; img.src = new URL(art.image.slice(1), base).href; visual.appendChild(img);
    }
    const text = document.createElement("p"); text.className = "page-text"; text.textContent = page.t;
    section.append(visual, text);
    if (page.p === "moral_landing" || (index === book.story.pages.length - 1 && book.story.moral)) {
      const moral = document.createElement("p"); moral.className = "page-moral"; moral.textContent = "מוסר השכל: " + book.story.moral; section.appendChild(moral);
    }
    const num = document.createElement("p"); num.className = "page-num"; num.textContent = "עמוד " + (index + 1) + " מתוך " + book.story.pages.length; section.appendChild(num);
    return section;
  }
  async function loadReader() {
    const reader = document.querySelector("[data-reader]");
    if (!reader) { ready(); return; }
    reader.hidden = true;
    try {
      let book, isDemo = !location.hash;
      if (isDemo) {
        const world = new URLSearchParams(location.search).get("demo") === "sea" ? "sea" : "forest";
        const response = await fetch(new URL("data/demo-" + world + ".json", base));
        if (!response.ok) throw new Error("לא הצלחנו לטעון את הסיפור לדוגמה.");
        book = await response.json();
      } else {
        const token = location.hash.slice(1);
        if (!/^[A-Za-z0-9_-]{1,12000}$/.test(token)) throw new Error("הקישור לסיפור אינו תקין.");
        try { const cached = sessionStorage.getItem("sipur.current"); if (cached) { const value = JSON.parse(cached); if (value.token === token) book = value; } } catch (_) { /* Storage is optional. */ }
        if (!book) {
          status("פותחים את הספר… בטעינה הראשונה זה עשוי לקחת מעט זמן.");
          book = await runEngine({action:"decode",token:token});
        }
      }
      const story = book.story;
      reader.dataset.demo = String(isDemo); reader.dataset.token = book.token;
      for (const key of ["title", "name", "age", "moral"]) reader.dataset[key] = story[key] || "";
      reader.dataset.template = story.template_id || ""; reader.dataset.fingerprint = story.fingerprint || ""; reader.dataset.pages = story.pages.length;
      reader.dataset.cover = book.art[0].image ? new URL(book.art[0].image.slice(1), base).href : new URL("static/images/bedtime-world.webp",base).href;
      document.title = story.title + " — סיפור";
      reader.querySelector("h1").textContent = story.title;
      reader.querySelector(".story-meta").textContent = "הסיפור של " + story.name + " · גיל " + story.age + " · " + story.pages.length + " עמודים";
      const demo = reader.querySelector(".demo-banner"); if (demo) demo.hidden = !isDemo;
      const progress = reader.querySelector(".progress");
      reader.querySelectorAll("[data-page]").forEach(page => page.remove());
      let anchor = progress;
      story.pages.forEach((_, i) => { const page = bookArt(book,i); anchor.after(page); anchor = page; });
      const dots = reader.querySelector(".dots"); dots.replaceChildren();
      story.pages.forEach((_,i) => { const dot = document.createElement("button"); dot.type="button";dot.className="dot";dot.dataset.goto=i;dot.setAttribute("aria-label","עמוד "+(i+1));dots.appendChild(dot); });
      reader.hidden = false; status(""); const progressText = document.querySelector("[data-engine-status]"); if (progressText) progressText.hidden = true;
      ready();
    } catch (error) { status(error.message || "לא הצלחנו לפתוח את הסיפור. אפשר לחזור וליצור סיפור חדש."); }
  }
  function bindForm() {
    const form = document.querySelector("[data-validate]");
    if (!form) return;
    form.addEventListener("submit", async event => {
      if (event.defaultPrevented) return;
      event.preventDefault();
      const button = form.querySelector('[type="submit"]'), message = form.querySelector("[data-form-status]");
      const values = new FormData(form);
      button.disabled = true; message.hidden = false;
      message.textContent = "טוענים את עולם הסיפורים… בפעם הראשונה זה עשוי לקחת מעט זמן.";
      try {
        let saved = [];
        try { saved = JSON.parse(localStorage.getItem("sipur.library.v1") || "[]"); } catch (_) { /* Optional */ }
        if (!Array.isArray(saved)) saved = [];
        const book = await runEngine({action:"generate",values:{name:values.get("name").trim(),age:values.get("age"),events:[1,2,3].map(n=>values.get("event"+n).trim())},
          used_templates:saved.map(b=>b.template).filter(Boolean),used_fingerprints:saved.map(b=>b.fingerprint).filter(Boolean)});
        try { sessionStorage.setItem("sipur.current",JSON.stringify(book)); } catch (_) { /* Shared links still work. */ }
        location.assign(new URL("reader.html",base).href + "#" + book.token);
      } catch (error) { message.textContent = error.message; button.disabled = false; }
    });
  }
  if (document.querySelector("[data-reader]")) loadReader();
  else { ready(); bindForm(); }
})();
