/* ── staging script: logo-glitch ── */

(function(){
  var source = document.getElementById("fritz-glitch-source");
  var ACCENT_PALETTE = source.dataset.accentPalette.split(" ");
  var CHANNELS = source.dataset.channels.split(" ");
  var BEAT_MS = 100;
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function parseLayout(g){
    return {
      node: g.dataset.node,
      tx: parseFloat(g.dataset.tx),
      scale: parseFloat(g.dataset.scale),
      fill: g.dataset.fill,
      baseD: Array.prototype.map.call(g.querySelectorAll("path.base"), function(p){ return p.getAttribute("d"); }),
      accents: Array.prototype.map.call(g.querySelectorAll("path.accent"), function(p){
        return { d: p.getAttribute("d"), fill: p.getAttribute("fill") };
      })
    };
  }

  var LAYOUTS = Array.prototype.map.call(
    source.querySelectorAll(".fritz-layout:not(.fritz-canon)"), parseLayout
  );
  var CANON = parseLayout(source.querySelector(".fritz-canon"));

  function pick(arr){ return arr[Math.floor(Math.random() * arr.length)]; }

  function beatHTML(layout, baseFill, accentFills){
    var base = layout.baseD.map(function(d){ return '<path d="' + d + '" fill="' + baseFill + '"/>'; }).join("");
    var accents = layout.accents.map(function(a, i){
      return '<path d="' + a.d + '" fill="' + (accentFills ? accentFills[i] : a.fill) + '"/>';
    }).join("");
    return '<g transform="translate(' + layout.tx + ',0.4247) scale(' + layout.scale + ')">' + base + accents + '</g>';
  }

  function randomBeat(){
    var layout = pick(LAYOUTS);
    var baseFill = pick(CHANNELS);
    var accentFills = layout.accents.map(function(){ return pick(ACCENT_PALETTE); });
    return beatHTML(layout, baseFill, accentFills);
  }

  var CANON_HTML = beatHTML(CANON, CANON.fill, null);

  function initLockup(root){
    var slot = root.querySelector("#mark-slot") || root.querySelector('[id$="mark-slot"]');
    if (!slot) return;
    slot.innerHTML = CANON_HTML;
    if (reduceMotion) return;

    var timers = [];
    var playing = false;

    function clearTimers(){ timers.forEach(clearTimeout); timers = []; }

    function play(){
      if (playing) return;
      playing = true;
      clearTimers();
      var seq = LAYOUTS.map(function(l){ return beatHTML(l, l.fill, null); });
      seq.push(randomBeat());
      seq.push(randomBeat());
      seq.forEach(function(html, i){
        timers.push(setTimeout(function(){ slot.innerHTML = html; }, i * BEAT_MS));
      });
      timers.push(setTimeout(function(){
        slot.innerHTML = CANON_HTML;
        playing = false;
      }, seq.length * BEAT_MS));
    }

    function reset(){
      clearTimers();
      playing = false;
      slot.innerHTML = CANON_HTML;
    }

    root.addEventListener("mouseenter", play);
    root.addEventListener("focus", play);
    root.addEventListener("mouseleave", reset);
    root.addEventListener("blur", reset);
  }

  document.querySelectorAll("[data-fritz-hover-lockup]").forEach(initLockup);

  // Play the glitch once on load so every visitor sees the mark animate at least once
  setTimeout(function(){
    document.querySelectorAll("[data-fritz-hover-lockup]").forEach(function(el){
      el.dispatchEvent(new Event("mouseenter"));
    });
  }, 500);
})();