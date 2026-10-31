// La barre du haut : cachée en descendant, de retour dès qu'on remonte, toujours là tout en haut de la page.
(() => {
  const nav = document.querySelector(".nav");
  if (!nav) return;
  let last = scrollY;
  addEventListener("scroll", () => {
    const y = scrollY;
    if (Math.abs(y - last) < 4) return;
    nav.classList.toggle("hidden", y > last && y > nav.offsetHeight);
    last = y;
  }, { passive: true });
  // Le clavier ramène la barre quand un de ses liens prend le focus.
  nav.addEventListener("focusin", () => nav.classList.remove("hidden"));
})();
