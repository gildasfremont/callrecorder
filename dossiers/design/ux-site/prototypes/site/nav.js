// La barre du haut : cachée en descendant, de retour dès qu'on remonte, toujours là tout en haut de la page.
(() => {
  const nav = document.querySelector(".nav");
  if (!nav) return;
  // Tout en haut de l'accueil, la barre n'a pas de logo (le micro du titre occupe la place) : il revient avec elle.
  const top = () => nav.classList.toggle("at-top", scrollY < 40);
  top();
  let last = scrollY;
  addEventListener("scroll", () => {
    const y = scrollY;
    top();
    if (Math.abs(y - last) < 4) return;
    nav.classList.toggle("hidden", y > last && y > nav.offsetHeight);
    last = y;
  }, { passive: true });
  // Le clavier ramène la barre quand un de ses liens prend le focus.
  nav.addEventListener("focusin", () => nav.classList.remove("hidden"));
})();
