// La fréquentation, sans cookie : la page vue et le site d'où l'on vient, puis deux gestes, copier la ligne
// d'installation et ouvrir le message. Le service compte par jour ; rien ne part depuis une copie locale du site.
(function () {
  if (location.hostname !== 'gildasfremont.github.io' || !navigator.sendBeacon) return;
  var endpoint = 'https://callrecorder-notes.vercel.app/api/visite';
  function send(data) {
    data.page = location.pathname;
    try { navigator.sendBeacon(endpoint, JSON.stringify(data)); } catch (e) {}
  }
  var params = new URLSearchParams(location.search), from = '';
  try { from = document.referrer && new URL(document.referrer).hostname; } catch (e) {}
  send({ source: params.get('ref') || params.get('utm_source') || (from !== location.hostname ? from : '') });
  document.addEventListener('click', function (e) {
    if (e.target.closest('[data-copy="cmd"]')) send({ action: 'installation' });
    else if (e.target.closest('.open-message')) send({ action: 'message' });
  });
})();
