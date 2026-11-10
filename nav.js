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

// Les onglets (contrôle segmenté), sur toutes les pages : un seul arrêt de Tab par groupe, l'onglet choisi ; les
// flèches passent à l'onglet voisin et le choisissent, Début et Fin vont au premier et au dernier (S23). Chaque page
// garde son propre clic : le clavier ne fait que le déclencher.
(() => {
  document.querySelectorAll('[role="tablist"]').forEach(list => {
    const tabs = [...list.querySelectorAll('[role="tab"]')];
    if (!tabs.length) return;
    const sync = () => tabs.forEach(t => t.tabIndex = t.getAttribute("aria-selected") === "true" ? 0 : -1);
    sync();
    list.addEventListener("click", () => setTimeout(sync));
    list.addEventListener("keydown", e => {
      const i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      const n = { ArrowRight: i + 1, ArrowDown: i + 1, ArrowLeft: i - 1, ArrowUp: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
      if (n === undefined) return;
      e.preventDefault();
      const t = tabs[(n + tabs.length) % tabs.length];
      t.focus();
      t.click();
    });
  });
})();
