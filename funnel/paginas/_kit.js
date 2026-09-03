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

/* Red de seguridad: pase lo que pase con el observador, nada visible puede
   quedarse en opacity 0. Una página en blanco no la salva nadie. */
setTimeout(() => $$(".rv:not(.in)").forEach(el => {
  if(el.getBoundingClientRect().top < innerHeight * 1.6) el.classList.add("in");
}), 1800);

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
pieAlFinal();

/* ── Conteo animado ──────────────────────────────────────────────── */
const countIO = new IntersectionObserver((es,o) => {
  es.forEach(e => {
    if(!e.isIntersecting) return;
    o.unobserve(e.target);
    const el = e.target, to = +el.dataset.count, sfx = el.dataset.suffix || "";
    const dec = +(el.dataset.dec || 0);            /* decimales: 1.5M, 4.8× … */
    /* 66964 se lee mal; 66.964 se lee. Salvo que se pida crudo (años, códigos). */
    const cifra = v => el.hasAttribute("data-crudo")
      ? v.toFixed(dec)
      : v.toLocaleString("es-ES", {minimumFractionDigits:dec, maximumFractionDigits:dec});
    if(RM){ el.textContent = cifra(to) + sfx; return; }
    const t0 = performance.now(), dur = 1500;
    const step = t => {
      const p = Math.min(1,(t-t0)/dur);
      const v = to * (1 - Math.pow(1-p,3));
      el.textContent = cifra(dec ? +v.toFixed(dec) : Math.round(v)) + (p===1 ? sfx : "");
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
const esIncrustacion = v => /^\s*</.test(v || "");

const reproducir = player => {
  const url = valores.get(player.dataset.res) || player.dataset.resValor;
  if(!url){ player.classList.add("sin-video"); return; }
  if(esIncrustacion(url)){                       // el usuario pegó un <iframe>
    $(".player-btn", player)?.remove();
    $(".player-art", player)?.remove();
    $(".player-meta", player)?.remove();
    player.insertAdjacentHTML("beforeend", url);
    return;
  }
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

/* Las imágenes se aplican con UNA regla CSS por recurso, no con un
   style= por elemento: si la foto se usa 16 veces (marquesinas
   duplicadas), el dato viaja una sola vez. */
const reglasImg = new Map();
/* Los valores largos (imágenes en base64, códigos de incrustación) viven
   aquí y NO en el atributo del elemento: si el recurso se usa 8 veces,
   el dato se guardaba 8 veces y multiplicaba el peso de la página. */
const valores = new Map();
const MARCA = "\u00b7cargado";
function pintarReglas(){
  let st = document.getElementById("__recursos");
  if(!st){ st = document.createElement("style"); st.id = "__recursos"; document.head.append(st); }
  st.textContent = [...reglasImg].map(([id, url]) =>
    `[data-res="${id}"]{background-image:url("${url}")}`).join("\n");
}

/** Aplica un valor a un slot de recurso. tipo: imagen|video|link|contador|texto */
function aplicarRecurso(id, valor){
  const els = $$(`[data-res="${CSS.escape(id)}"]`);
  if(!els.length) return 0;
  els.forEach(el => {
    const tipo = el.dataset.resTipo;
    if(valor) valores.set(id, valor); else valores.delete(id);
    el.dataset.resValor = !valor ? "" : (valor.length > 300 ? MARCA : valor);
    if(!valor){ el.classList.remove("cargada"); reglasImg.delete(id); return; }
    if(tipo === "imagen"){
      if(el.tagName === "IMG"){ el.src = valor; el.loading = "lazy"; el.decoding = "async"; }
      else {
        el.style.removeProperty("background-image");   // por si venía de una versión vieja
        el.classList.add("cargada");
        reglasImg.set(id, valor);
        /* La caja adopta la proporción real: sin franjas ni recortes. */
        if(el.classList.contains("entera") || el.hasAttribute("data-res-ajusta")){
          const im = new Image();
          im.onload = () => el.style.aspectRatio = im.naturalWidth + " / " + im.naturalHeight;
          im.src = valor;
        }
      }
    } else if(tipo === "embed"){
      /* Calendario, formulario, widget: se pinta de inmediato. */
      el.innerHTML = esIncrustacion(valor)
        ? valor
        : `<iframe src="${valor.replace(/"/g,"&quot;")}" loading="lazy"
             allow="camera; microphone; fullscreen; payment"></iframe>`;
      /* innerHTML no ejecuta <script>: hay que recrearlos para que el
         reproductor o el widget arranquen de verdad. */
      $$("script", el).forEach(viejo => {
        const nuevo = document.createElement("script");
        [...viejo.attributes].forEach(a => nuevo.setAttribute(a.name, a.value));
        nuevo.textContent = viejo.textContent;
        viejo.replaceWith(nuevo);
      });
      el.classList.add("cargada");
    } else if(tipo === "link"){
      if(el.tagName === "A") el.href = valor;
    } else if(tipo === "contador"){
      el.dataset.hasta = valor;
    } else if(tipo === "texto"){
      el.textContent = valor;
    }
    /* video: se usa al pulsar el botón; nada que hacer ahora */
  });
  if(els[0]?.dataset.resTipo === "imagen") pintarReglas();
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
      valor: valores.get(id) || el.dataset.resValor || "",
      usos:  1,
    });
  });
  return [...vistos.values()];
}

/** El pie siempre cierra. Si algo lo dejó en otro sitio —un arrastre en el
    estudio, un estado antiguo, un pegado a medias— vuelve solo a su lugar.
    Es idempotente: si ya está el último, no toca el DOM. */
function pieAlFinal(){
  const pie = $("footer.foot") || $("body > footer");
  if(pie && pie !== document.body.lastElementChild &&
     !pie.nextElementSibling?.matches?.("script")) document.body.append(pie);
}

/** Re-arma todo después de que el estudio inyecta o edita contenido. */
function refrescar(){
  pieAlFinal();                   // pase lo que pase, el pie cierra
  sellarBloques();                // ids estables de bloque para el estudio
  armarPlayers();                 // los players son del estudio: siempre
  if(SIN_KIT) return;             // la página trae sus propios comportamientos
  armarMarquesinas();
  observeRevs();
  observeCounts();
}

/* ── Rutas estables (mismo cálculo que usa el estudio) ───────────── */
function rutaDe(el){
  const p = [];
  let cur = el;
  while(cur?.parentElement && cur.parentElement.tagName !== "BODY"){
    p.unshift([...cur.parentElement.children].indexOf(cur));
    cur = cur.parentElement;
  }
  if(cur?.parentElement?.tagName === "BODY"){
    sellarBloques();
    p.unshift("b" + (cur.dataset.bloque ?? [...cur.parentElement.children].indexOf(cur)));
  }
  return p.join("-");
}
function porRuta(ruta){
  if(ruta === "") return document.body;
  const seg = String(ruta).split("-");
  let el = /^b/.test(seg[0])
    ? document.querySelector(`body > [data-bloque="${CSS.escape(seg[0].slice(1))}"]`)
    : document.body.children[+seg[0]];
  for(const i of seg.slice(1)){ el = el?.children[+i]; if(!el) return null; }
  return el;
}

/* ── Enlaces: TODOS los <a href>, internos y externos ────────────── */
function listarEnlaces(){
  return $$("a[href]").map(a => {
    const href = a.getAttribute("href") || "";
    return {
      ruta: rutaDe(a),
      href,
      texto: (a.textContent || "").trim().replace(/\s+/g," ").slice(0, 60) || "(sin texto)",
      interno: href.startsWith("#"),
      res: a.dataset.res || "",
      destinoExiste: href.startsWith("#") ? !!document.getElementById(href.slice(1)) : null,
    };
  });
}
function aplicarEnlace(ruta, href){
  const a = porRuta(ruta);
  if(a && a.tagName === "A"){ a.setAttribute("href", href); return true; }
  return false;
}

/* ── Bloques: la estructura de primer nivel de la página ─────────── */
const NOMBRES = {NAV:"Navegación", HEADER:"Cabecera", SECTION:"Sección",
                 FOOTER:"Pie", MAIN:"Contenido", ASIDE:"Lateral", DIV:"Bloque"};

function sellarBloques(){
  [...document.body.children].forEach((el, i) => {
    if(el.dataset.bloque === undefined) el.dataset.bloque = i;
  });
}

function listarBloques(){
  sellarBloques();
  return [...document.body.children]
    .filter(el => !/^(SCRIPT|STYLE|TEMPLATE)$/.test(el.tagName))
    .map(el => {
      const eyebrow = $(".eyebrow", el)?.textContent.trim();
      const titulo  = $("h1,h2,h3", el)?.textContent.trim();
      const secciones = [...el.children].filter(c => !/^(SCRIPT|STYLE)$/.test(c.tagName));
      return {
        id: el.dataset.bloque,
        tag: el.tagName.toLowerCase(),
        tipo: NOMBRES[el.tagName] || "Bloque",
        ancla: el.id || "",
        nombre: (eyebrow || titulo || NOMBRES[el.tagName] || el.tagName)
                  .replace(/\s+/g," ").slice(0, 46),
        secciones: secciones.length,
        elementos: el.querySelectorAll("*").length,
        recursos: el.querySelectorAll("[data-res]").length,
        enlaces: el.querySelectorAll("a[href]").length,
        oculto: el.hasAttribute("data-oculto"),
      };
    });
}

/** Aplica orden y visibilidad de bloques. orden = ids en el orden deseado. */
/** El nombre visible de un bloque: lo que lees en «Bloques y secciones». */
function selloDe(el){
  const eyebrow = $(".eyebrow", el)?.textContent.trim();
  const titulo  = $("h1,h2,h3", el)?.textContent.trim();
  return (el.id || eyebrow || titulo || el.className || el.tagName)
           .replace(/\s+/g, " ").trim().slice(0, 46);
}

/** Mapa {id: nombre} para poder recuperar tus elecciones aunque cambien los ids. */
function sellosBloques(){
  sellarBloques();
  const m = {};
  for(const el of document.body.children) m[el.dataset.bloque] = selloDe(el);
  return m;
}

function aplicarEstructura({orden = [], ocultos = [], sellos = null} = {}){
  sellarBloques();
  const body = document.body;
  let porId = new Map([...body.children].map(el => [el.dataset.bloque, el]));

  /* Los ids son la posición del bloque, así que en cuanto se añade o se quita
     una sección todos se corren y tus elecciones acaban señalando al bloque de
     al lado —así se ocultó «Antes de agendar» sin que nadie lo pidiera—. Si el
     estado trae los nombres de cuando se guardó, se reencaminan por nombre. */
  if(sellos){
    const ahora = {};
    for(const el of body.children) ahora[selloDe(el)] = el.dataset.bloque;
    const nuevo = {};
    let movido = false;
    for(const [viejo, nombre] of Object.entries(sellos)){
      const actual = ahora[nombre];
      if(actual !== undefined && actual !== viejo){ nuevo[viejo] = actual; movido = true; }
    }
    if(movido){
      const traduce = id => nuevo[String(id)] ?? String(id);
      orden   = orden.map(traduce);
      ocultos = ocultos.map(traduce);
    }
  }
  /* Un orden guardado puede traer ids que ya no existen —la página cambió desde
     que se guardó—. Reordenar solo con los que sobreviven dejaría a los bloques
     no mencionados colgando al principio, que es como el pie acababa arriba.
     Así que se reconstruye la secuencia entera: primero los ids pedidos que aún
     existen, y detrás los demás en el orden que ya tenían en el documento. */
  const pedidos = orden.map(String).filter(id => porId.has(id));
  const resto   = [...porId.keys()].filter(id => !pedidos.includes(id));
  [...pedidos, ...resto].forEach(id => body.append(porId.get(id)));
  porId.forEach((el, id) => {
    const esconder = ocultos.map(String).includes(String(id));
    el.toggleAttribute("data-oculto", esconder);
  });
  pieAlFinal();                     // el pie cierra, mande lo que mande el orden
  /* Los <script> vuelven al final para no quedar en medio del contenido. */
  $$("body > script").forEach(s => body.append(s));
}

/** Inserta un bloque nuevo (HTML) al final o después de otro. */
/** Marca como borrado lo que el estudio haya quitado. No se elimina del DOM:
    se marca, para que los índices de los hermanos no se corran y las rutas
    guardadas de todo lo demás sigan apuntando a su sitio. Al exportar, lo
    marcado no viaja. */
function aplicarBorrados(rutas = []){
  $$("[data-borrado]").forEach(e => e.removeAttribute("data-borrado"));
  for(const r of rutas){
    const el = porRuta(r);          // el porRuta del kit toma solo la ruta
    if(el) el.setAttribute("data-borrado", "");
  }
}

function insertarBloque(html, despuesDe){
  const t = document.createElement("template");
  t.innerHTML = html.trim();
  const el = t.content.firstElementChild;
  if(!el) return null;
  const ancla = despuesDe != null
    ? [...document.body.children].find(c => c.dataset.bloque === String(despuesDe))
    : null;
  if(ancla) ancla.after(el); else document.body.append(el);
  el.dataset.bloque = "n" + Date.now().toString(36);
  $$("body > script").forEach(s => document.body.append(s));
  refrescar();
  return el.dataset.bloque;
}

/* ── Iluminación holográfica: solo mientras el cursor esté encima ── */

let holoEl = null, holoCapa = null, holoRAF = 0;

function capaHolo(){
  if(holoCapa?.isConnected) return holoCapa;
  holoCapa = document.createElement("div");
  holoCapa.id = "__holo";
  holoCapa.innerHTML = `<div class="caja"><span class="destello"></span>
    <i class="esq ai"></i><i class="esq ad"></i><i class="esq bi"></i><i class="esq bd"></i></div>`;
  document.body.append(holoCapa);
  addEventListener("scroll", pintarHolo, {passive:true});
  addEventListener("resize", pintarHolo);
  return holoCapa;
}
function pintarHolo(){
  if(!holoEl || !holoCapa) return;
  cancelAnimationFrame(holoRAF);
  holoRAF = requestAnimationFrame(() => {
    const r = holoEl.getBoundingClientRect();
    const c = $(".caja", holoCapa);
    const m = 6;
    Object.assign(c.style, {left:(r.left-m)+"px", top:(r.top-m)+"px",
      width:(r.width+m*2)+"px", height:(r.height+m*2)+"px"});
  });
}
/** Enciende el holograma sobre un elemento (null lo apaga). */
function iluminar(el){
  holoEl = el;
  if(!el){ holoCapa?.remove(); holoCapa = null; return; }
  capaHolo(); pintarHolo();
}

/** Lleva el lienzo al elemento y lo ilumina. Para el hover del estudio. */
function enfocar(sel, {porRuta: esRuta = false, centrar = true} = {}){
  const el = esRuta ? porRuta(sel) : $(`[data-res="${CSS.escape(sel)}"]`);
  if(!el) return false;
  const r = el.getBoundingClientRect();
  const dentro = r.top > 60 && r.bottom < innerHeight - 20;
  if(centrar && !dentro) el.scrollIntoView({block:"center", behavior: RM ? "auto" : "smooth"});
  iluminar(el);
  return true;
}
function apagar(){ iluminar(null); }

/* ── Resaltar: llevar el lienzo al elemento y marcarlo ───────────── */
let latido;
function resaltar(sel, {porRuta: esRuta = false} = {}){
  const el = esRuta ? porRuta(sel) : $(`[data-res="${CSS.escape(sel)}"]`);
  if(!el) return false;
  el.scrollIntoView({block:"center", behavior: RM ? "auto" : "smooth"});
  $$("[data-latido]").forEach(x => x.removeAttribute("data-latido"));
  el.setAttribute("data-latido","");
  clearTimeout(latido);
  latido = setTimeout(() => el.removeAttribute("data-latido"), 2200);
  return true;
}
function quitarResaltado(){ $$("[data-latido]").forEach(x => x.removeAttribute("data-latido")); }

/* ── Modo recursos: clic en la página para cargar el recurso ─────── */
let modoRec = false;
function modoRecursos(on){
  modoRec = on;
  document.documentElement.toggleAttribute("data-modo-recursos", on);
  $$("[data-res]").forEach(el => {
    el.toggleAttribute("data-res-vacio", on && !el.dataset.resValor);
  });
}
document.addEventListener("click", e => {
  if(!modoRec) return;
  const el = e.target.closest?.("[data-res]");
  if(!el) return;
  e.preventDefault(); e.stopPropagation();
  parent.postMessage({kit:"abrir-recurso", id: el.dataset.res}, "*");
}, true);

/* ── Redimensionar un bloque arrastrando ─────────────────────────── */
/* Muestra los espacios de arriba y abajo y deja ajustarlos con el cursor. */

let redimEl = null, redimCapa = null, redimRAF = 0;
const px = v => Math.round(parseFloat(v) || 0);

function capaRedim(){
  if(redimCapa && redimCapa.isConnected) return redimCapa;
  redimCapa = document.createElement("div");
  redimCapa.id = "__redim";
  redimCapa.innerHTML = `
    <div class="marco"></div>
    <div class="banda arriba"></div><div class="banda abajo"></div>
    <div class="valor arriba"></div><div class="valor abajo"></div>
    <div class="tirador arriba" data-lado="Top">↕ arriba</div>
    <div class="tirador abajo" data-lado="Bottom">↕ abajo</div>
    <div class="guia"></div>`;
  document.body.append(redimCapa);
  $$(".tirador, .banda", redimCapa).forEach(t => t.addEventListener("pointerdown", arrastrar));
  addEventListener("scroll", pintarRedim, {passive:true});
  addEventListener("resize", pintarRedim);
  return redimCapa;
}

function pintarRedim(){
  if(!redimEl || !redimCapa) return;
  cancelAnimationFrame(redimRAF);
  redimRAF = requestAnimationFrame(() => {
    const r = redimEl.getBoundingClientRect();
    const cs = getComputedStyle(redimEl);
    const pt = px(cs.paddingTop), pb = px(cs.paddingBottom);
    const q = sel => $(sel, redimCapa);

    Object.assign(q(".marco").style,
      {left:r.left+"px", top:r.top+"px", width:r.width+"px", height:r.height+"px"});

    Object.assign(q(".banda.arriba").style,
      {left:r.left+"px", width:r.width+"px", top:r.top+"px", height:pt+"px",
       display: pt > 2 ? "block" : "none"});
    Object.assign(q(".banda.abajo").style,
      {left:r.left+"px", width:r.width+"px", top:(r.bottom-pb)+"px", height:pb+"px",
       display: pb > 2 ? "block" : "none"});

    Object.assign(q(".tirador.arriba").style, {left:(r.left+r.width/2)+"px", top:(r.top+pt-8)+"px"});
    Object.assign(q(".tirador.abajo").style,  {left:(r.left+r.width/2)+"px", top:(r.bottom-pb-8)+"px"});

    q(".valor.arriba").textContent = pt + " px arriba";
    q(".valor.abajo").textContent  = pb + " px abajo";
    Object.assign(q(".valor.arriba").style, {left:(r.left+r.width/2)+"px", top:(r.top+pt/2-9)+"px",
      display: pt > 26 ? "block" : "none"});
    Object.assign(q(".valor.abajo").style,  {left:(r.left+r.width/2)+"px", top:(r.bottom-pb/2-9)+"px",
      display: pb > 26 ? "block" : "none"});
  });
}

function arrastrar(e){
  if(!redimEl) return;
  e.preventDefault();
  const tir = e.currentTarget;
  const lado = tir.dataset.lado || (tir.classList.contains("arriba") ? "Top" : "Bottom");
  const prop = "padding" + lado;
  const cs = getComputedStyle(redimEl);
  const inicio = px(cs[prop]);
  const y0 = e.clientY;
  const antes = {paddingTop: cs.paddingTop, paddingBottom: cs.paddingBottom};
  tir.classList.add("activo");
  tir.setPointerCapture(e.pointerId);

  redimCapa.classList.add("arrastrando");
  const mover = ev => {
    const d = (ev.clientY - y0) * (lado === "Top" ? 1 : -1);
    const v = Math.max(0, Math.min(400, Math.round((inicio + d) / 2) * 2));
    redimEl.style[prop] = v + "px";
    const g = $(".guia", redimCapa);
    g.textContent = v + " px";
    g.style.display = "block";
    g.style.left = ev.clientX + "px";
    g.style.top = (ev.clientY - 26) + "px";
    pintarRedim();
  };
  const soltar = () => {
    tir.classList.remove("activo");
    redimCapa.classList.remove("arrastrando");
    $(".guia", redimCapa).style.display = "none";
    tir.removeEventListener("pointermove", mover);
    tir.removeEventListener("pointerup", soltar);
    parent.postMessage({kit:"redim", ruta: rutaDe(redimEl), antes,
      ahora:{paddingTop: redimEl.style.paddingTop || antes.paddingTop,
             paddingBottom: redimEl.style.paddingBottom || antes.paddingBottom}}, "*");
  };
  tir.addEventListener("pointermove", mover);
  tir.addEventListener("pointerup", soltar);
}

/** Activa el redimensionado sobre un elemento (o lo apaga con null). */
function redimensionar(el){
  redimEl = el;
  if(!el){ redimCapa?.remove(); redimCapa = null; return; }
  capaRedim();
  pintarRedim();
}

/** De qué tamaño se ve realmente un slot, para no subir fotos gigantes. */
function medidaDe(id){
  const el = $(`[data-res="${CSS.escape(id)}"]`);
  if(!el) return 0;
  const r = el.getBoundingClientRect();
  return Math.round(Math.max(r.width, r.height));
}

/* ── Galerías: zonas donde el estudio puede añadir huecos nuevos ─── */

function galerias(){
  return $$("[data-galeria]").map(g => ({
    clave: g.dataset.galeria,
    titulo: g.dataset.galeriaTitulo || g.dataset.galeria,
    tarjetas: g.children.length,
  }));
}

/** Añade un hueco clonando la última tarjeta: hereda estructura y estilo. */
function crearSlot(galeria, {id, label, nota = "", titulo = "", sub = ""} = {}){
  const g = $(`[data-galeria="${CSS.escape(galeria)}"]`);
  if(!g || !g.lastElementChild || !id) return false;
  if($(`[data-res="${CSS.escape(id)}"]`)) return false;        // ya existe

  const nueva = g.lastElementChild.cloneNode(true);
  const slot = $("[data-res]", nueva);
  if(!slot){ return false; }

  slot.dataset.res = id;
  slot.dataset.resLabel = label || id;
  slot.dataset.resNota = nota;
  delete slot.dataset.resValor;
  slot.classList.remove("cargada");
  slot.style.removeProperty("background-image");
  slot.style.setProperty("--hu", String(Math.floor(Math.random()*360)));
  const eti = $("span", slot);
  if(eti) eti.textContent = titulo || "Nuevo";

  /* Textos de la tarjeta: los dos primeros elementos con texto propio */
  const textos = [...nueva.querySelectorAll("b, .cuenta-a, .portada-n, .tesela-v b, .captura-e")]
                 .filter(e => !slot.contains(e));
  if(textos[0]) textos[0].textContent = titulo || "Sin nombre";
  if(textos[1]) textos[1].textContent = sub;
  nueva.querySelectorAll(".portada-m, .cuenta-s, .portada-c, .tesela-v span")
       .forEach(e => { if(!textos.includes(e)) e.textContent = sub; });

  nueva.removeAttribute("data-latido");
  g.append(nueva);
  refrescar();
  return true;
}

window.KIT = { aplicarRecurso, listarRecursos, refrescar, resaltar, quitarResaltado, medidaDe,
               galerias, crearSlot,
               enfocar, apagar, iluminar, pintarHolo,
               redimensionar, pintarRedim,
               listarEnlaces, aplicarEnlace, listarBloques, aplicarEstructura, sellosBloques,
               insertarBloque, aplicarBorrados, modoRecursos, rutaDe, porRuta, $, $$, esc, RM };

refrescar();
document.documentElement.dataset.kitListo = "1";
})();
