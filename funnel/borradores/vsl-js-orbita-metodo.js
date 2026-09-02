/* Retirado el 02/09/2026: el SVG #orbita ya no está en la página.
   El método se cuenta ahora en tres fases planas —Atraer · Conectar · Cerrar—.
   Se guarda por los textos de los nodos, que son buenos. */

/* ── El método en órbita ────────────────────────────────────────── */
const METODO = [
  {n:"Tu oferta", sub:"Posicionamiento", ia:false, r:118, desde:-96, nodos:[
    ["Micro nicho","El sitio exacto donde eres la única opción evidente."],
    ["Promesa","Dicha con las palabras que tu cliente ya usa."],
    ["Precio","El que vale tu transformación, no el que te da miedo."],
  ]},
  {n:"Segundo cerebro", sub:"La Biblia + agentes de IA", ia:true, r:176, desde:-104, nodos:[
    ["La Biblia","Paradigmas, deseos y miedos de tu cliente ideal, por escrito."],
    ["Agentes","Entrenados en tu voz, dentro de nuestro software privado."],
    ["Guiones","Ángulos nuevos sin volver a quedarte en blanco."],
    ["Criterio","Respuestas de DM resueltas como las darías tú."],
  ]},
  {n:"Conversión", sub:"Leads, llamadas y cierres", ia:false, r:234, desde:-100, nodos:[
    ["Contenido","Epifanía situacional: se ven a sí mismos y se mueven."],
    ["Anuncios","Alcance que no depende del algoritmo."],
    ["Conversación","Estructura validada, sin perseguir a nadie."],
    ["CRM","Cada lead con nombre, etapa y siguiente paso."],
    ["Llamada","Calificada, no curiosa."],
    ["Script dorado","Cerrar sin presionar y sin rogar."],
  ]},
];

(() => {
  const svg = $("#orbita"), det = $("#detalle"), chips = $("#pilarChips");
  if(!svg) return;
  const C = 260;
  const pol = (a,r) => [C + r*Math.cos((a-90)*Math.PI/180), C + r*Math.sin((a-90)*Math.PI/180)];

  let capas = "", radios = "";
  METODO.forEach((cap, ci) => {
    let nodos = "";
    cap.nodos.forEach((nd, i) => {
      const a = cap.desde + (360/cap.nodos.length)*i;
      const [x,y] = pol(a, cap.r);
      const [rx,ry] = pol(a, cap.r - 13);
      radios += `<line class="radio" x1="${C}" y1="${C}" x2="${rx.toFixed(1)}" y2="${ry.toFixed(1)}"/>`;
      const fuera = cap.r > 190;
      const [ex,ey] = pol(a, cap.r + (fuera ? 24 : -24));
      nodos += `<g class="nodo-g" data-c="${ci}" data-n="${i}">
          <circle class="disco" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="12"/>
          <text class="eti" x="${ex.toFixed(1)}" y="${(ey+3).toFixed(1)}">${esc(nd[0])}</text>
        </g>`;
    });
    capas += `<g class="capa${cap.ia?" ia":""}" data-c="${ci}">
        <circle class="aro-o" cx="${C}" cy="${C}" r="${cap.r}"/>${nodos}</g>`;
  });

  svg.innerHTML = `
    <g class="gira-o">${radios}</g>
    ${capas}
    <circle cx="${C}" cy="${C}" r="62" fill="#12101E" stroke="#D6A54455" stroke-width="1.2"/>
    <text class="nucleo-s" x="${C}" y="${C-16}">EL MÉTODO</text>
    <text class="nucleo-t" x="${C}" y="${C+4}" font-size="17">Escalling™</text>
    <text class="nucleo-s" x="${C}" y="${C+22}">3 CAPAS · 13 PIEZAS</text>`;

  chips.innerHTML = METODO.map((c,i) => `
    <button class="pilar-chip${c.ia?" ia":""}" data-c="${i}">
      <i>0${i+1}</i><b>${esc(c.n)}</b><span>${c.nodos.length}</span>
    </button>`).join("");

  const inicio = {i:"El método", b:"Tres capas que se sostienen",
    p:"La oferta te hace único. El segundo cerebro te multiplica. La conversión lo cobra."};
  const pinta = (ci, ni) => {
    if(ci == null) det.innerHTML = `<i>${esc(inicio.i)}</i><b>${esc(inicio.b)}</b><p>${esc(inicio.p)}</p>`;
    else{
      const c = METODO[ci], nd = c.nodos[ni];
      det.innerHTML = `<i>${esc(c.n)}</i><b>${esc(nd[0])}</b><p>${esc(nd[1])}</p>`;
    }
  };
  pinta(null);

  $$(".nodo-g", svg).forEach(g => {
    const act = () => {
      $$(".nodo-g", svg).forEach(x => x.classList.remove("on"));
      g.classList.add("on");
      pinta(+g.dataset.c, +g.dataset.n);
    };
    g.addEventListener("pointerenter", act);
    g.addEventListener("click", act);
  });

  let filtro = null;
  const filtrar = ci => {
    filtro = filtro === ci ? null : ci;
    svg.classList.toggle("filtrando", filtro !== null);
    $$(".capa", svg).forEach(c => c.classList.toggle("viva", +c.dataset.c === filtro));
    $$(".pilar-chip", chips).forEach(b => b.classList.toggle("act", +b.dataset.c === filtro));
    if(filtro !== null) pinta(filtro, 0); else pinta(null);
  };
  $$(".pilar-chip", chips).forEach(b => {
    b.addEventListener("click", () => filtrar(+b.dataset.c));
    b.addEventListener("pointerenter", () => {
      if(filtro === null){
        svg.classList.add("filtrando");
        $$(".capa", svg).forEach(c => c.classList.toggle("viva", c.dataset.c === b.dataset.c));
      }
    });
    b.addEventListener("pointerleave", () => {
      if(filtro === null){ svg.classList.remove("filtrando"); $$(".capa", svg).forEach(c => c.classList.remove("viva")); }
    });
  });
})();
