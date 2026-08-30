const WHATSAPP_NUMBER = "";
const PREFILL = "שלום, אשמח להתחיל סיפור שבועי. שם הילד/ה: , גיל: , שלושה דברים שקרו השבוע: 1)  2)  3)";

function orderLink() {
  if (!WHATSAPP_NUMBER) return "";
  return "https://wa.me/" + WHATSAPP_NUMBER.replace(/[^\d]/g, "") + "?text=" + encodeURIComponent(PREFILL);
}

document.querySelectorAll("[data-order]").forEach((el) => {
  el.addEventListener("click", (e) => {
    const url = orderLink();
    if (!url) {
      e.preventDefault();
      document.querySelectorAll(".note").forEach((n) => n.classList.add("show"));
      return;
    }
    el.setAttribute("href", url);
  });
});
