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

// Le sommaire en pastilles (téléphone) : un fondu du côté où des pastilles sont cachées, pour montrer qu'il défile.
(() => {
  document.querySelectorAll(".toc nav").forEach(nav => {
    const maj = () => {
      nav.classList.toggle("avant", nav.scrollLeft > 4);
      nav.classList.toggle("apres", nav.scrollLeft + nav.clientWidth < nav.scrollWidth - 4);
    };
    maj();
    nav.addEventListener("scroll", maj, { passive: true });
    addEventListener("resize", maj);
    // La pastille de la partie lue reste visible.
    new MutationObserver(() => {
      const a = nav.querySelector("[aria-current]");
      if (a && getComputedStyle(nav).overflowX === "auto") nav.scrollTo({ left: a.offsetLeft - 16, behavior: "smooth" });
    }).observe(nav, { subtree: true, attributes: true, attributeFilter: ["aria-current"] });
  });
})();

// Sur téléphone, une capture de l'app est trop petite pour être lue : au toucher, elle s'ouvre à sa taille, et se
// parcourt du doigt. Fermer, Échap ou le geste retour du système la referment.
(() => {
  const captures = [...document.querySelectorAll(".stage > img, .feature figure img, details.row .answer img")];
  if (!captures.length || !window.HTMLDialogElement) return;
  const petit = matchMedia("(max-width: 760px)");
  let d;
  const ouvre = img => {
    if (!d) {
      d = document.createElement("dialog");
      d.className = "agrandie";
      d.innerHTML = '<button class="button fermer" type="button">Fermer</button><div class="defile"><img alt=""></div>';
      d.querySelector(".fermer").addEventListener("click", () => d.close());
      document.body.append(d);
    }
    const grande = d.querySelector("img");
    grande.alt = img.alt;
    grande.src = img.src;  // la plus grande, pas celle que le srcset a choisie pour la petite largeur
    // À la taille d'une fenêtre de Mac vue de près : deux fois et demie la largeur de l'écran, au plus l'image entière
    // (son width déclaré, en résolution double).
    const pleine = (+img.getAttribute("width") || img.naturalWidth * devicePixelRatio) / 2;
    grande.style.width = Math.round(Math.min(pleine, innerWidth * 2.5)) + "px";
    d.showModal();
    const s = d.querySelector(".defile");
    s.scrollTo((s.scrollWidth - s.clientWidth) / 2, 0);
  };
  const pose = () => captures.forEach(img => {
    img.classList.toggle("agrandissable", petit.matches);
    if (petit.matches) { img.setAttribute("role", "button"); img.tabIndex = 0; }
    else { img.removeAttribute("role"); img.removeAttribute("tabindex"); }
  });
  pose();
  petit.addEventListener("change", pose);
  captures.forEach(img => {
    img.addEventListener("click", () => petit.matches && ouvre(img));
    img.addEventListener("keydown", e => { if (petit.matches && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); ouvre(img); } });
  });
})();
