// Le message de la bulle du bas : tapé, ou dicté par la reconnaissance vocale du navigateur (Chrome, Edge, Safari),
// puis envoyé en texte au service des notes. Sans reconnaissance (Firefox…), la dictée du clavier fait l'affaire.
(function () {
  var form = document.querySelector('.message');
  if (!form) return;
  var endpoint = 'https://callrecorder-notes.vercel.app/api/note';
  var box = form.querySelector('textarea'), dictate = form.querySelector('.dictate'), status = form.querySelector('.message-status');
  var send = form.querySelector('[type=submit]');
  var Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var rec = null;

  function stopDictation() {
    if (!rec) return;
    rec.onend = null;
    try { rec.stop(); } catch (e) {}
    rec = null;
    dictate.classList.remove('on');
    dictate.querySelector('span').textContent = 'Dicter';
  }

  if (Recognition) {
    dictate.hidden = false;
    dictate.addEventListener('click', function () {
      if (rec) return stopDictation();
      // Le texte dicté s'ajoute à ce qui est déjà écrit, et reste modifiable.
      var before = box.value.trim(), said = '';
      rec = new Recognition();
      rec.lang = 'fr-FR';
      rec.continuous = true;
      rec.interimResults = true;
      rec.onresult = function (e) {
        var now = '';
        for (var i = e.resultIndex; i < e.results.length; i++) {
          if (e.results[i].isFinal) said += e.results[i][0].transcript.trim() + ' ';
          else now += e.results[i][0].transcript;
        }
        box.value = ((before ? before + ' ' : '') + said + now).trim();
      };
      rec.onerror = function (e) {
        stopDictation();
        if (e.error === 'not-allowed' || e.error === 'service-not-allowed') status.textContent = 'Le micro n’est pas accessible : tapez votre message, ou autorisez le micro pour ce site.';
        else if (e.error !== 'no-speech' && e.error !== 'aborted') status.textContent = 'La dictée n’a pas marché : tapez votre message.';
      };
      // Chrome s'arrête après un silence : on relance tant que le bouton est enfoncé.
      rec.onend = function () { if (rec) try { rec.start(); } catch (e) { stopDictation(); } };
      status.textContent = '';
      dictate.classList.add('on');
      dictate.querySelector('span').textContent = 'Arrêter';
      try { rec.start(); } catch (e) { stopDictation(); }
    });
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    stopDictation();
    var text = box.value.trim();
    if (!text) return box.focus();
    send.disabled = true;
    status.textContent = 'Envoi…';
    fetch(endpoint, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ text: text }) }).then(function (r) {
      if (r.ok) { box.value = ''; status.textContent = 'Merci, c’est envoyé. Je vous lis très vite.'; }
      else if (r.status === 429) status.textContent = 'Beaucoup de messages aujourd’hui : réessayez demain, ou écrivez-moi sur LinkedIn.';
      else status.textContent = 'L’envoi n’a pas marché. Réessayez, ou écrivez-moi sur LinkedIn.';
    }).catch(function () {
      status.textContent = 'L’envoi n’a pas marché. Réessayez, ou écrivez-moi sur LinkedIn.';
    }).then(function () { send.disabled = false; });
  });
})();
