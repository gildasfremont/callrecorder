// Sur téléphone, les captures de l'app sont trop petites pour se lire : un toucher les ouvre en grand, à leur taille,
// et l'on s'y promène du doigt (callrecorder-app#421, M5). Échap, le bouton Fermer ou un toucher hors de l'image referme.
(() => {
  const petit = matchMedia("(max-width: 760px)");
  const captures = [...document.querySelectorAll(".stage > img.decoupe, .stage > img.pixel, .feature figure img")];
  if (!captures.length) return;

  const loupe = document.createElement("dialog");
  loupe.className = "loupe";
  loupe.setAttribute("aria-label", "Capture agrandie");
  loupe.innerHTML = '<button type="button" class="fermer">Fermer</button><div class="defile"><img alt=""></div>';
  document.body.append(loupe);
  const grande = loupe.querySelector("img");
  const fermer = () => loupe.close();
  loupe.querySelector(".fermer").addEventListener("click", fermer);
  loupe.addEventListener("click", e => { if (e.target === loupe) fermer(); });
  loupe.addEventListener("close", () => { grande.removeAttribute("src"); document.documentElement.classList.remove("loupe-ouverte"); });

  // La plus grande image du srcset : c'est elle qu'on veut lire.
  const plusGrande = img => {
    const cands = (img.getAttribute("srcset") || "").split(",").map(c => c.trim().split(/\s+/)).filter(c => c[0]);
    cands.sort((a, b) => parseInt(b[1] || 0) - parseInt(a[1] || 0));
    return cands.length ? new URL(cands[0][0], location.href).href : img.currentSrc || img.src;
  };
  const ouvrir = img => {
    grande.src = plusGrande(img);
    grande.alt = img.alt;
    // À moitié de sa taille en pixels : nette sur un écran Retina, et lisible.
    grande.style.width = Math.max(innerWidth, (+img.getAttribute("width") || img.naturalWidth) / 2) + "px";
    document.documentElement.classList.add("loupe-ouverte");
    loupe.showModal();
  };

  const armer = () => captures.forEach(img => {
    if (petit.matches) {
      img.tabIndex = 0;
      img.setAttribute("role", "button");
      img.dataset.loupe = "";
    } else {
      img.removeAttribute("tabindex");
      img.removeAttribute("role");
      delete img.dataset.loupe;
    }
  });
  armer();
  petit.addEventListener("change", armer);
  captures.forEach(img => {
    img.addEventListener("click", () => { if (petit.matches) ouvrir(img); });
    img.addEventListener("keydown", e => { if (petit.matches && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); ouvrir(img); } });
  });
})();
