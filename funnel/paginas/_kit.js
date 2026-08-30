/* ═══════════════════════════════════════════════════════════════════
   KIT JS · comportamiento compartido por todas las páginas del funnel.
   Expone window.KIT para que el estudio pueda hablar con la página.
   ═══════════════════════════════════════════════════════════════════ */
(() => {
"use strict";

const $  = (s,c=document) => c.querySelector(s);
const $$ = (s,c=document) => [...c.querySelectorAll(s)];
const RM = matchMedia("(prefers-reduced-motion: reduce)").matches;
const esc = s => String(s).replace(/[&<>"]/g, m => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]));

const SIN_KIT = document.documentElement.hasAttribute("data-sin-kit");

/* ── Revelado al scroll ──────────────────────────────────────────── */
const revIO = new IntersectionObserver((es,o) => {
  es.forEach(e => { if(e.isIntersecting){ e.target.classList.add("in"); o.unobserve(e.target); } });
}, {rootMargin:"0px 0px -8% 0px", threshold:.08});
const observeRevs = () => $$(".rv:not(.in)").forEach(el => revIO.observe(el));

/* ── Nav pegajosa ────────────────────────────────────────────────── */
const nav = $(".nav");
if(nav && !document.documentElement.hasAttribute("data-sin-kit")){
  const onScroll = () => nav.classList.toggle("stuck", scrollY > 40);
  addEventListener("scroll", onScroll, {passive:true}); onScroll();
}

/* ── Cuenta regresiva ────────────────────────────────────────────── */
/* data-res-tipo="contador": si hay fecha guardada cuenta hacia ella;
   si no, usa un ciclo perpetuo de N días (data-ciclo).                */
const contadores = () => {
  const roots = $$("[data-cd]");
  if(!roots.length) return;
  const tick = () => {
    roots.forEach(root => {
      const hasta = root.dataset.hasta ? Date.parse(root.dataset.hasta) : NaN;
      let left;
      if(!isNaN(hasta)) left = Math.max(0, hasta - Date.now());
      else { const c = (+root.dataset.ciclo || 7)*864e5; left = c - (Date.now() % c); }
      const v = {d:Math.floor(left/864e5), h:Math.floor(left/36e5)%24,
                 m:Math.floor(left/6e4)%60, s:Math.floor(left/1e3)%60};
      $$("[data-u]", root).forEach(n => n.textContent = String(v[n.dataset.u]).padStart(2,"0"));
    });
  };
  tick(); setInterval(tick, 1000);
};
if(!SIN_KIT) contadores();

/* ── Conteo animado ──────────────────────────────────────────────── */
const countIO = new IntersectionObserver((es,o) => {
  es.forEach(e => {
    if(!e.isIntersecting) return;
    o.unobserve(e.target);
    const el = e.target, to = +el.dataset.count, sfx = el.dataset.suffix || "";
    if(RM){ el.textContent = to + sfx; return; }
    const t0 = performance.now(), dur = 1500;
    const step = t => {
      const p = Math.min(1,(t-t0)/dur);
      el.textContent = Math.round(to*(1-Math.pow(1-p,3))) + (p===1 ? sfx : "");
      if(p<1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  });
}, {threshold:.5});
const observeCounts = () => $$("[data-count]").forEach(el => countIO.observe(el));

/* ── Reproductores de video ──────────────────────────────────────── */
/* Un .player con data-res-tipo="video" muestra su carátula hasta que
   el estudio le carga una URL; entonces al pulsar inserta el embed.   */
const embedURL = url => {
  const yt = url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([\w-]{6,})/);
  if(yt) return `https://www.youtube.com/embed/${yt[1]}?autoplay=1&rel=0`;
  const vi = url.match(/vimeo\.com\/(?:video\/)?(\d+)/);
  if(vi) return `https://player.vimeo.com/video/${vi[1]}?autoplay=1`;
  const wi = url.match(/wistia\.com\/medias\/(\w+)/);
  if(wi) return `https://fast.wistia.net/embed/iframe/${wi[1]}?autoPlay=1`;
  return null;
};
const reproducir = player => {
  const url = player.dataset.resValor;
  if(!url){ player.classList.add("sin-video"); return; }
  const emb = embedURL(url);
  if(emb){
    const f = document.createElement("iframe");
    f.src = emb; f.allow = "autoplay; fullscreen; picture-in-picture"; f.allowFullscreen = true;
    player.append(f);
  } else {
    const v = document.createElement("video");
    v.src = url; v.controls = true; v.autoplay = true; v.playsInline = true;
    player.append(v);
  }
  $(".player-btn", player)?.remove();
  $(".player-art", player)?.remove();
  $(".player-meta", player)?.remove();
};
const armarPlayers = () => $$(".player").forEach(p => {
  const btn = $(".player-btn", p);
  if(btn && !btn.dataset.armado){ btn.dataset.armado = "1"; btn.addEventListener("click", () => reproducir(p)); }
});

/* ── Scroll suave ────────────────────────────────────────────────── */
$$('a[href^="#"]').forEach(a => a.addEventListener("click", e => {
  const el = document.getElementById(a.getAttribute("href").slice(1));
  if(!el) return;
  e.preventDefault();
  scrollTo({top: el.getBoundingClientRect().top + scrollY - 74, behavior: RM ? "auto" : "smooth"});
}));

/* ── Marquesinas: duplica el contenido para el bucle infinito ────── */
const armarMarquesinas = () => $$(".mq-t").forEach(t => {
  if(t.dataset.dup) return;
  t.dataset.dup = "1";
  t.innerHTML = t.innerHTML + t.innerHTML;
});

/* ═══════════════════════════════════════════════════════════════════
   API para el estudio
   ═══════════════════════════════════════════════════════════════════ */

/** Aplica un valor a un slot de recurso. tipo: imagen|video|link|contador|texto */
function aplicarRecurso(id, valor){
  const els = $$(`[data-res="${CSS.escape(id)}"]`);
  if(!els.length) return 0;
  els.forEach(el => {
    const tipo = el.dataset.resTipo;
    el.dataset.resValor = valor || "";
    if(!valor){ el.classList.remove("cargada"); return; }
    if(tipo === "imagen"){
      if(el.tagName === "IMG") el.src = valor;
      else { el.style.backgroundImage = `url("${valor}")`; el.classList.add("cargada"); }
    } else if(tipo === "link"){
      if(el.tagName === "A") el.href = valor;
    } else if(tipo === "contador"){
      el.dataset.hasta = valor;
    } else if(tipo === "texto"){
      el.textContent = valor;
    }
    /* video: se usa al pulsar el botón; nada que hacer ahora */
  });
  return els.length;
}

/** Inventario de recursos declarados en esta página. */
function listarRecursos(){
  const vistos = new Map();
  $$("[data-res]").forEach(el => {
    const id = el.dataset.res;
    if(vistos.has(id)){ vistos.get(id).usos++; return; }
    vistos.set(id, {
      id,
      tipo:  el.dataset.resTipo  || "texto",
      label: el.dataset.resLabel || id,
      nota:  el.dataset.resNota  || "",
      opcional: el.hasAttribute("data-res-opcional"),
      valor: el.dataset.resValor || "",
      usos:  1,
    });
  });
  return [...vistos.values()];
}

/** Re-arma todo después de que el estudio inyecta o edita contenido. */
function refrescar(){
  armarPlayers();                 // los players son del estudio: siempre
  if(SIN_KIT) return;             // la página trae sus propios comportamientos
  armarMarquesinas();
  observeRevs();
  observeCounts();
}

window.KIT = { aplicarRecurso, listarRecursos, refrescar, $, $$, esc, RM };

refrescar();
document.documentElement.dataset.kitListo = "1";
})();
