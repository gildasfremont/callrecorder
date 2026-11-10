// Le message de la bulle du bas : « Laisser un message » ouvre la zone de texte, rien ne s'enregistre tout seul, et la
// page reste calée en bas pour qu'on voie tout. En bas à gauche, face à Envoyer, Dicter lance la dictée du navigateur
// (Chrome, Edge, Safari) ; Pause la suspend. Le bouton garde le focus : la barre d'espace dicte et met en pause, et un
// clic dans le texte permet de taper. Pendant la dictée, le rond rouge du bouton suit le volume de la voix.
// Au-dessus du texte, seulement ce qui ne va pas. Envoyer part en texte au service des notes. Sans reconnaissance
// vocale (Firefox…), juste le texte et Envoyer.
(function () {
  var form = document.querySelector('.message'), open = document.querySelector('.open-message');
  if (!form || !open) return;
  var endpoint = 'https://callrecorder-notes.vercel.app/api/note';
  var box = form.querySelector('textarea'), bar = form.querySelector('.rec-bar'), state = form.querySelector('.rec-state');
  var toggle = form.querySelector('.rec-toggle'), send = form.querySelector('.send'), thanks = form.querySelector('.sent-status span');
  var another = form.querySelector('.another'), key = form.querySelector('.rec-key');
  var Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  var rec = null, heard = false, check = null, meter = null;
  var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  toggle.hidden = !Recognition;

  // La bulle est au bout de la page : quand elle grandit, on reste calé en bas.
  function atEnd() { return window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 48; }
  function toEnd(smooth) {
    window.scrollTo({ top: document.documentElement.scrollHeight, behavior: smooth && !calm ? 'smooth' : 'auto' });
  }

  // Ce qui ne va pas, au-dessus du texte ; rien à dire, la ligne disparaît.
  function say(text, kind) {
    state.textContent = text || '';
    state.className = 'rec-state' + (kind ? ' ' + kind : '');
    bar.hidden = !text;
  }

  // La zone grandit avec le texte, et Envoyer ne s'allume qu'avec un message.
  function fit() {
    var end = atEnd();
    box.style.height = 'auto';
    box.style.height = box.scrollHeight + 'px';
    send.disabled = !box.value.trim();
    if (end) toEnd();
  }

  // Le volume de la voix, de 0 à 1, dans --niveau : le halo du rond rouge le suit. Le contexte audio naît dans le clic,
  // sinon le navigateur le laisse en veille. Sans micro accessible, ou si l'on préfère moins d'animations, le rond reste
  // fixe.
  function listenLevel() {
    var AC = window.AudioContext || window.webkitAudioContext;
    if (calm || !AC || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) return;
    var ctx = new AC(), m = { ctx: ctx, stream: null, raf: 0 };
    meter = m;
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
      m.stream = stream;
      if (meter !== m) return quiet(m);
      var an = ctx.createAnalyser(), mute = ctx.createGain(), buf = new Float32Array(512), level = 0;
      an.fftSize = 512;
      mute.gain.value = 0;
      ctx.createMediaStreamSource(stream).connect(an);
      an.connect(mute);
      mute.connect(ctx.destination);
      if (ctx.resume) ctx.resume();
      (function tick() {
        if (meter !== m) return;
        an.getFloatTimeDomainData(buf);
        var sum = 0;
        for (var i = 0; i < buf.length; i++) sum += buf[i] * buf[i];
        var v = Math.min(1, Math.max(0, (Math.sqrt(Math.sqrt(sum / buf.length)) - .1) * 2.4));
        level += (v - level) * (v > level ? .5 : .15);
        toggle.style.setProperty('--niveau', level.toFixed(3));
        m.raf = requestAnimationFrame(tick);
      })();
    }).catch(function () {});
  }
  function quiet(m) {
    cancelAnimationFrame(m.raf);
    if (m.stream) m.stream.getTracks().forEach(function (t) { t.stop(); });
    if (m.ctx.state !== 'closed') m.ctx.close();
  }
  function stopLevel() {
    if (meter) quiet(meter);
    meter = null;
    toggle.style.removeProperty('--niveau');
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
    stopLevel();
    toggle.textContent = 'Dicter';
    toggle.classList.remove('on');
    key.textContent = 'Espace pour dicter';
    say(message, kind);
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
      if (state.classList.contains('problem')) say();
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
    toggle.textContent = 'Pause';
    toggle.classList.add('on');
    key.textContent = 'Espace pour la pause';
    say();
    try { rec.start(); } catch (e) { return stop('La dictée n’a pas démarré : tapez votre message.', 'problem'); }
    listenLevel();
    check = setTimeout(diagnose, 4000);
  }

  // Le bouton garde le focus, même dans Safari qui ne le donne pas au clic : la barre d'espace le rappuie.
  toggle.addEventListener('click', function () { if (rec) stop(); else start(); toggle.focus(); });

  // À l'ouverture, le curseur est dans le texte : on tape tout de suite (S17). Dicter garde son bouton, et la barre
  // d'espace quand il a le focus. La dictée ne démarre jamais toute seule.
  function begin() {
    form.classList.remove('sent');
    fit();
    if (Recognition) { toggle.textContent = 'Dicter'; toggle.classList.remove('on'); key.textContent = 'Espace pour dicter'; }
    box.focus({ preventScroll: true });
    say();
    toEnd(true);
  }

  open.addEventListener('click', function () {
    open.hidden = true;
    form.hidden = false;
    begin();
  });
  another.addEventListener('click', begin);

  // ⌘/Ctrl + Entrée envoie, depuis le texte comme depuis Dicter.
  form.addEventListener('keydown', function (e) {
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
      say(r.status === 429 ? 'Beaucoup de messages aujourd’hui : réessayez demain, ou écrivez-moi sur LinkedIn.' : 'L’envoi n’a pas marché. Réessayez, ou écrivez-moi sur LinkedIn.', 'problem');
    }).catch(function () {
      say('L’envoi n’a pas marché. Réessayez, ou écrivez-moi sur LinkedIn.', 'problem');
    }).then(fit);
  });
})();
