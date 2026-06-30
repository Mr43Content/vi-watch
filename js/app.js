// Countdown to GTA VI launch — 19 Nov 2026, 00:00 local
(function () {
  var target = new Date("2026-11-19T00:00:00");

  function pad(n) { return String(n).padStart(2, "0"); }

  function tick() {
    if (!document.getElementById("cd-days")) return;
    var now = new Date();
    var diff = target - now;
    if (diff <= 0) {
      document.getElementById("cd-days").textContent = "00";
      document.getElementById("cd-hours").textContent = "00";
      document.getElementById("cd-mins").textContent = "00";
      document.getElementById("cd-secs").textContent = "00";
      return;
    }
    var s = Math.floor(diff / 1000);
    var days = Math.floor(s / 86400);
    var hours = Math.floor((s % 86400) / 3600);
    var mins = Math.floor((s % 3600) / 60);
    var secs = s % 60;

    document.getElementById("cd-days").textContent = days;
    document.getElementById("cd-hours").textContent = pad(hours);
    document.getElementById("cd-mins").textContent = pad(mins);
    document.getElementById("cd-secs").textContent = pad(secs);
  }

  tick();
  setInterval(tick, 1000);
})();

// News ticker — reads data/news.json (auto-updated by the GitHub Action)
(function () {
  var el = document.getElementById("ticker-track");
  if (!el) return;

  fetch("data/news.json")
    .then(function (r) { return r.json(); })
    .then(function (items) {
      if (!items || !items.length) return;
      var html = items
        .map(function (i) {
          return '<span><b>' + i.date + '</b> — <a href="' + i.link + '" target="_blank" rel="noopener">' + i.title + "</a></span>";
        })
        .join("");
      // duplicate content so the marquee loop has no visible seam
      el.innerHTML = html + html;
    })
    .catch(function () {
      el.innerHTML = "<span>Letzte Meldungen folgen in Kürze …</span>";
    });
})();
