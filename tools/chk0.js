/* Runs before anything else. Two jobs:
   1. change the placeholder text, which proves scripts execute at all here
      (on iOS a file opened in Files/Quick Look renders the HTML but never
      runs JS, and the page just sits on the placeholder)
   2. surface any startup error on screen, since a phone has no console */
(function () {
  var box = document.getElementById('fatal');
  window.__fatal = function (msg) {
    if (!box) return;
    box.hidden = false;
    box.textContent = 'Başlatılamadı:\n\n' + msg;
  };
  window.onerror = function (msg, src, line, col, err) {
    window.__fatal(msg + '\n\n' + (src || '?') + ' : ' + line + ':' + col +
                   (err && err.stack ? '\n\n' + err.stack : ''));
    return false;
  };
  var c = document.getElementById('country');
  if (c) c.textContent = 'Harita hazırlanıyor…';
})();