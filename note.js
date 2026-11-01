// Le message de la bulle du bas : tapé, ou dicté par la reconnaissance vocale du navigateur (Chrome, Edge, Safari),
// puis envoyé en texte au service des notes. Sans reconnaissance (Firefox…), la dictée du clavier fait l'affaire.
(function () {
  var form = document.querySelector('.message');
  if (!form) return;
  var endpoint = 'https://callrecorder-notes.vercel.app/api/note';
  var box = form.querySelector('textarea'), dictate = form.querySelector('.dictate'), status = form.querySelector('.message-status');
  var send = form.querySelector('[type=submit]');
  var Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var rec = null, heard = false, check = null;

  // « Par défaut - Micro MacBook Air (Built-in) » → « Micro MacBook Air ».
  function micName(label) { return label.replace(/^(Par défaut|Default)\s*-\s*/i, '').replace(/\s*\([^)]*\)\s*$/, '').trim(); }

  // Rien entendu : souvent, le navigateur écoute un autre micro que celui du système (des écouteurs débranchés de
  // l'oreille, un micro virtuel). Chrome le dit : on compare son micro à celui du système, et on nomme les deux.
  function diagnose() {
    if (!rec || heard || !navigator.mediaDevices) return;
    navigator.mediaDevices.enumerateDevices().then(function (list) {
      var system = list.filter(function (d) { return d.kind === 'audioinput' && d.deviceId === 'default'; })[0];
      if (!system || !system.label) {
        status.textContent = 'Je ne vous entends pas encore : vérifiez votre micro, ou tapez votre message.';
        return;
      }
      return navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
        var used = micName(stream.getAudioTracks()[0].label);
        stream.getTracks().forEach(function (t) { t.stop(); });
        if (!rec || heard) return;
        var wanted = micName(system.label);
        status.textContent = used && used !== wanted
          ? 'Votre navigateur écoute « ' + used + ' », pas « ' + wanted + ' ». Choisissez « ' + wanted + ' » avec l’icône du micro dans la barre d’adresse, puis relancez Dicter.'
          : 'Je ne vous entends pas encore : parlez près de « ' + wanted + ' », ou tapez votre message.';
      });
    }).catch(function () {});
  }

  function stopDictation() {
    clearTimeout(check);
    if (status.textContent === 'Je vous écoute…') status.textContent = '';
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
      heard = false;
      rec = new Recognition();
      rec.lang = 'fr-FR';
      rec.continuous = true;
      rec.interimResults = true;
      rec.onsoundstart = function () { heard = true; };
      rec.onresult = function (e) {
        // Le texte arrive : plus besoin d'« écoute » ni de conseil sur le micro.
        status.textContent = '';
        heard = true;
        var now = '';
        for (var i = e.resultIndex; i < e.results.length; i++) {
          if (e.results[i].isFinal) said += e.results[i][0].transcript.trim() + ' ';
          else now += e.results[i][0].transcript;
        }
        box.value = ((before ? before + ' ' : '') + said + now).trim();
      };
      rec.onerror = function (e) {
        // Un silence ou une relance : la dictée continue (onend la relance).
        if (e.error === 'no-speech' || e.error === 'aborted') return;
        stopDictation();
        if (e.error === 'not-allowed' || e.error === 'service-not-allowed') status.textContent = 'Le micro n’est pas accessible : autorisez-le pour ce site, ou tapez votre message.';
        else if (e.error === 'audio-capture') status.textContent = 'Aucun micro trouvé : tapez votre message.';
        else status.textContent = 'La dictée n’a pas marché : tapez votre message.';
      };
      // Chrome s'arrête après un silence : on relance tant que le bouton est enfoncé.
      rec.onend = function () { if (rec) try { rec.start(); } catch (e) { stopDictation(); } };
      status.textContent = 'Je vous écoute…';
      dictate.classList.add('on');
      dictate.querySelector('span').textContent = 'Arrêter';
      try { rec.start(); } catch (e) { stopDictation(); }
      check = setTimeout(diagnose, 4000);
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
