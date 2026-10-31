// La note vocale de la bulle du bas : enregistrée dans le navigateur en WAV 16 kHz mono, envoyée au service des notes.
(function () {
  var voice = document.querySelector('.voice');
  if (!voice) return;
  var endpoint = 'https://callrecorder-notes.vercel.app/api/note';
  var maxSeconds = 90, rate = 16000;
  var bars = voice.querySelector('.bars'), time = voice.querySelector('time'), msg = voice.querySelector('.rec-msg');
  var ctx, stream, node, chunks, started, timer;

  function state(s, text) { voice.dataset.state = s; msg.textContent = text || ''; }

  function stop() {
    clearInterval(timer);
    if (node) node.disconnect();
    if (stream) stream.getTracks().forEach(function (t) { t.stop(); });
    if (ctx) ctx.close();
    node = stream = ctx = null;
  }

  function wav(samples, from) {
    var n = Math.floor(samples.length * rate / from), out = new DataView(new ArrayBuffer(44 + n * 2));
    function str(o, s) { for (var i = 0; i < s.length; i++) out.setUint8(o + i, s.charCodeAt(i)); }
    str(0, 'RIFF'); out.setUint32(4, 36 + n * 2, true); str(8, 'WAVE'); str(12, 'fmt ');
    out.setUint32(16, 16, true); out.setUint16(20, 1, true); out.setUint16(22, 1, true);
    out.setUint32(24, rate, true); out.setUint32(28, rate * 2, true); out.setUint16(32, 2, true); out.setUint16(34, 16, true);
    str(36, 'data'); out.setUint32(40, n * 2, true);
    for (var i = 0; i < n; i++) {
      // Moyenne des échantillons d'origine qui tombent dans chaque échantillon à 16 kHz.
      var a = Math.floor(i * from / rate), b = Math.max(a + 1, Math.floor((i + 1) * from / rate)), sum = 0;
      for (var j = a; j < b; j++) sum += samples[j] || 0;
      var v = Math.max(-1, Math.min(1, sum / (b - a)));
      out.setInt16(44 + i * 2, v < 0 ? v * 0x8000 : v * 0x7fff, true);
    }
    return new Blob([out], { type: 'audio/wav' });
  }

  function bar(level) {
    var i = document.createElement('i');
    i.style.height = Math.max(3, Math.min(24, level * 160)) + 'px';
    bars.appendChild(i);
    if (bars.children.length > 80) bars.removeChild(bars.firstChild);
  }

  voice.querySelector('.rec-start').addEventListener('click', function () {
    if (!navigator.mediaDevices || !window.AudioContext && !window.webkitAudioContext) {
      return state('error', 'Votre navigateur ne sait pas enregistrer. Écrivez-moi sur LinkedIn.');
    }
    navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } }).then(function (s) {
      stream = s;
      ctx = new (window.AudioContext || window.webkitAudioContext)();
      var src = ctx.createMediaStreamSource(s);
      node = ctx.createScriptProcessor(4096, 1, 1);
      chunks = [];
      node.onaudioprocess = function (e) {
        var d = e.inputBuffer.getChannelData(0), sum = 0;
        chunks.push(new Float32Array(d));
        for (var i = 0; i < d.length; i++) sum += d[i] * d[i];
        bar(Math.sqrt(sum / d.length));
      };
      src.connect(node); node.connect(ctx.destination);
      bars.textContent = ''; time.textContent = '0:00';
      started = Date.now();
      timer = setInterval(function () {
        var t = Math.floor((Date.now() - started) / 1000);
        time.textContent = Math.floor(t / 60) + ':' + String(t % 60).padStart(2, '0');
        if (t >= maxSeconds) send();
      }, 250);
      state('rec');
    }).catch(function () {
      state('error', 'Le micro n’est pas accessible. Autorisez-le pour ce site, ou écrivez-moi sur LinkedIn.');
    });
  });

  voice.querySelector('.rec-cancel').addEventListener('click', function () { stop(); state('idle'); });
  voice.querySelector('.rec-send').addEventListener('click', send);

  function send() {
    if (voice.dataset.state !== 'rec') return;
    var from = ctx.sampleRate, seconds = (Date.now() - started) / 1000;
    stop();
    if (seconds < 1.5) return state('idle');
    var total = chunks.reduce(function (n, c) { return n + c.length; }, 0), all = new Float32Array(total), o = 0;
    chunks.forEach(function (c) { all.set(c, o); o += c.length; });
    state('sending', 'Envoi…');
    fetch(endpoint, { method: 'POST', headers: { 'content-type': 'audio/wav' }, body: wav(all, from) }).then(function (r) {
      if (r.ok) state('done', 'Merci, c’est envoyé. Je la lirai transcrite très vite.');
      else if (r.status === 429) state('error', 'Beaucoup de notes aujourd’hui : réessayez demain, ou écrivez-moi sur LinkedIn.');
      else state('error', 'L’envoi n’a pas marché. Réessayez, ou écrivez-moi sur LinkedIn.');
    }).catch(function () { state('error', 'L’envoi n’a pas marché. Réessayez, ou écrivez-moi sur LinkedIn.'); });
  }
})();
