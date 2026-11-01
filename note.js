// Le message de la bulle du bas : « Laissez-moi un message » ouvre la dictée du navigateur (Chrome, Edge, Safari).
// En haut, l'état : on écoute ou non, Arrêter / Reprendre, et ce qui ne va pas. Dessous, le texte, modifiable ; puis
// Envoyer, qui part en texte au service des notes. Sans reconnaissance vocale (Firefox…), juste le texte et Envoyer.
(function () {
  var form = document.querySelector('.message'), open = document.querySelector('.open-message');
  if (!form || !open) return;
  var endpoint = 'https://callrecorder-notes.vercel.app/api/note';
  var box = form.querySelector('textarea'), bar = form.querySelector('.rec-bar'), state = form.querySelector('.rec-state');
  var toggle = form.querySelector('.rec-toggle'), send = form.querySelector('.send'), thanks = form.querySelector('.sent-status');
  var Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var rec = null, heard = false, check = null;
  toggle.hidden = !Recognition;

  // kind : 'on' (on écoute), 'problem' (ce qui ne va pas), rien (à l'arrêt).
  function say(text, kind) {
    state.textContent = text;
    state.className = 'rec-state' + (kind ? ' ' + kind : '');
  }

  // La zone grandit avec le texte, et Envoyer ne s'allume qu'avec un message.
  function fit() {
    box.style.height = 'auto';
    box.style.height = box.scrollHeight + 'px';
    send.disabled = !box.value.trim();
  }
  box.addEventListener('input', fit);

  // « Par défaut - Micro MacBook Air (Built-in) » → « Micro MacBook Air ».
  function micName(label) { return label.replace(/^(Par défaut|Default)\s*-\s*/i, '').replace(/\s*\([^)]*\)\s*$/, '').trim(); }

  // Rien entendu : souvent, le navigateur écoute un autre micro que celui du système (des écouteurs pas portés, un
  // micro virtuel). Chrome le dit : on compare son micro à celui du système, et on nomme les deux.
  function diagnose() {
    if (!rec || heard || !navigator.mediaDevices) return;
    navigator.mediaDevices.enumerateDevices().then(function (list) {
      var system = list.filter(function (d) { return d.kind === 'audioinput' && d.deviceId === 'default'; })[0];
      if (!system || !system.label) return say('Je ne vous entends pas : vérifiez votre micro, ou tapez votre message.', 'problem');
      return navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
        var used = micName(stream.getAudioTracks()[0].label);
        stream.getTracks().forEach(function (t) { t.stop(); });
        if (!rec || heard) return;
        var wanted = micName(system.label);
        say(used && used !== wanted
          ? 'Votre navigateur écoute « ' + used + ' ». Choisissez « ' + wanted + ' » dans l’icône micro de la barre d’adresse.'
          : 'Je ne vous entends pas : parlez près de « ' + wanted + ' », ou tapez votre message.', 'problem');
      });
    }).catch(function () {});
  }

  function stop(message, kind) {
    clearTimeout(check);
    if (rec) {
      rec.onend = null;
      try { rec.stop(); } catch (e) {}
      rec = null;
    }
    toggle.textContent = 'Reprendre';
    say(message || 'Dictée arrêtée.', kind);
  }

  function start() {
    // Le texte dicté s'ajoute à ce qui est déjà écrit, et reste modifiable.
    var before = box.value.trim(), said = '';
    heard = false;
    rec = new Recognition();
    rec.lang = 'fr-FR';
    rec.continuous = true;
    rec.interimResults = true;
    rec.onsoundstart = function () { heard = true; };
    rec.onresult = function (e) {
      if (!heard || state.classList.contains('problem')) say('J’écoute…', 'on');
      heard = true;
      var now = '';
      for (var i = e.resultIndex; i < e.results.length; i++) {
        if (e.results[i].isFinal) said += e.results[i][0].transcript.trim() + ' ';
        else now += e.results[i][0].transcript;
      }
      box.value = ((before ? before + ' ' : '') + said + now).trim();
      fit();
      box.scrollTop = box.scrollHeight;
    };
    rec.onerror = function (e) {
      // Un silence ou une relance : la dictée continue (onend la relance).
      if (e.error === 'no-speech' || e.error === 'aborted') return;
      if (e.error === 'not-allowed' || e.error === 'service-not-allowed') stop('Le micro n’est pas autorisé pour ce site : autorisez-le, ou tapez votre message.', 'problem');
      else if (e.error === 'audio-capture') stop('Aucun micro trouvé : tapez votre message.', 'problem');
      else stop('La dictée n’a pas marché : tapez votre message.', 'problem');
    };
    // Chrome s'arrête après un silence : on relance tant qu'on n'a pas arrêté.
    rec.onend = function () { if (rec) try { rec.start(); } catch (e) { stop(); } };
    toggle.textContent = 'Arrêter';
    say('J’écoute…', 'on');
    try { rec.start(); } catch (e) { stop('La dictée n’a pas démarré : tapez votre message.', 'problem'); }
    check = setTimeout(diagnose, 4000);
  }

  toggle.addEventListener('click', function () { if (rec) { stop(); box.focus(); } else start(); });

  open.addEventListener('click', function () {
    open.hidden = true;
    form.hidden = false;
    fit();
    if (Recognition) { bar.hidden = false; start(); }
    else box.focus();
  });

  // ⌘/Ctrl + Entrée envoie.
  box.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : send.click(); }
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var text = box.value.trim();
    if (!text) return box.focus();
    if (rec) stop();
    send.disabled = true;
    fetch(endpoint, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ text: text }) }).then(function (r) {
      if (r.ok) { box.value = ''; form.classList.add('sent'); thanks.textContent = 'Merci, c’est envoyé. Je vous lis très vite.'; return; }
      bar.hidden = false;
      say(r.status === 429 ? 'Beaucoup de messages aujourd’hui : réessayez demain, ou écrivez-moi sur LinkedIn.' : 'L’envoi n’a pas marché. Réessayez, ou écrivez-moi sur LinkedIn.', 'problem');
    }).catch(function () {
      bar.hidden = false;
      say('L’envoi n’a pas marché. Réessayez, ou écrivez-moi sur LinkedIn.', 'problem');
    }).then(fit);
  });
})();
