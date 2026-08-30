# Link Bio IG — Imperio Holístico™

Landing de bio de Instagram para Marcelo Andrés Proaño · Escalling™ · Edume Global™.
Modelada sobre la estructura de strategycoach.us, con identidad, voz y copy propios.

## Archivos

| Archivo | Qué es |
|---|---|
| `page.html` | **Fuente única.** Todo el sitio: markup, CSS y JS. Es también el cuerpo que se publica como Artifact. |
| `index.html` | Generado. Documento completo con `<head>`, meta OG y favicon. **No lo edites a mano.** |
| `build.sh` | Regenera `index.html` desde `page.html`. |
| `fotos/` | Carpeta vacía para tus imágenes reales. |

Después de tocar `page.html`:

```bash
./build.sh
```

Para publicar: sube `index.html` (es autocontenido, sin dependencias externas salvo Google Fonts)
a Vercel, Netlify, Cloudflare Pages o tu hosting. Un solo archivo.

---

## Dirección de arte

- **Paleta**: obsidiana sesgada a violeta (`#0A0910`) + oro de pan de oro (`#D6A544`) + hueso cálido (`#F4EFE6`). Violeta (`#5B4A9C`) solo como aura ambiental.
- **Tipografía** — es la firma de la página y refleja tus dos mundos:
  - **Archivo** (grotesca, 800/900) = *el sistema*. Todos los titulares.
  - **Newsreader itálica** = *el alma*. Una frase por titular irrumpe en serif dorada.
  - **JetBrains Mono** = *los datos*. Eyebrows, cifras, etiquetas, contador.
- **Movimiento**: revelado con desenfoque al scroll, titular palabra por palabra, marquesinas infinitas que pausan al pasar el cursor, contadores animados, burbujas de chat en secuencia, globo de puntos en canvas, foco luminoso que sigue el cursor en el hero, cuenta regresiva en vivo. Todo se desactiva con `prefers-reduced-motion`.
- Un solo mundo visual (oscuro, deliberado). No hay tema claro: la página se pinta explícitamente y se ve igual en cualquier host.

## Estructura (paridad exacta con la referencia)

Nav → Hero (+ marquesina de casos) → Cifras → Crew → Las dos trampas → Sobre mí →
El Círculo Escalling™ (+ chats de DM) → Para quién es → Mapa/globo → Wins → Las 3 Fases →
Las 5 Voces de Marca™ → Filosofía → La prueba (+ cha-chings) → FAQ → CTA final → Footer

**Un solo CTA en toda la página**, como manda tu método: *escríbeme la palabra `IMPERIO` por DM*.
Ningún link directo, ningún segundo CTA.

---

## ⚠️ Qué tienes que reemplazar antes de publicar

Todo lo editable vive en un bloque al inicio del `<script>` en `page.html`, marcado
`DATOS EDITABLES`. Busca esa línea.

### 1. Tu handle de Instagram — **obligatorio**

```js
const IG = "https://instagram.com/marceloproano";   // ← tu @ real
```

Es un marcador de posición. Una sola línea: al cambiarla se actualizan los 4 enlaces de la página.

### 2. El feed de ventas (`CHA`) — **son datos de muestra**

Los montos, nombres y fechas de las tarjetas "cha-ching" los inventé para mostrar el formato.
Reemplázalos por registros reales o quita la sección.

### 3. Los casos sin cifra verificada (`CASOS`, `WINS`)

Con cifras reales de tu skill: **Lissett** ($80/sesión → $30.000/mes en 60 días),
**Fabiana** ($66.964 en 60 días), **Rainier** ($60/sesión → $39.961/mes en 3 meses) y tu propio
caso (−$150K → $65.000/mes).

**Héctor, Paola y Marina** aparecen sin cifra ("Caso doc.") porque no tenía sus números.
Complétalos o quítalos.

### 4. La comunidad (`CREW`) — **sin @, a propósito**

Puse nombre + sub-nicho en vez de handles de Instagram. No inventé arrobas porque podrían
apuntar a cuentas reales de terceros. Cámbialos por los handles verdaderos de tu crew
(con permiso de ellos) si quieres el efecto de la referencia.

### 5. Fotos

Los retratos son marcos generados con monograma. Para poner una foto real, añade
`background-image` al elemento — el monograma y la trama de puntos desaparecen solos:

```html
<div class="ph ph-sq" style="background-image:url('fotos/marcelo-principal.jpg')"></div>
```

Los tres huecos de la sección "Sobre mí" ya llevan el nombre de archivo sugerido en `data-foto`.
Para los avatares de la crew y los casos, edita la función `photo()` en el script.

### 6. El VSL

El botón del hero y las tarjetas de caso abren un modal con un hueco. Pega tu `<iframe>` de
YouTube o Vimeo dentro de `.modal-body` en `page.html`.
(En la versión publicada como Artifact el iframe externo queda bloqueado por seguridad; en
`index.html` desplegado en tu dominio funciona normal.)

### 7. La cuenta regresiva

```js
const CIERRE_CADA_DIAS = 7;   // ciclo del contador
```

Es un ciclo perpetuo de 7 días, no una fecha fija. Si prefieres una fecha real de cierre,
cambia la función `tick()` para restar contra un timestamp concreto.

---

## Nota sobre las cifras

El footer lleva un descargo: las cifras son reportadas por los propios clientes, son resultados
individuales y no constituyen promesa de ingresos. Mantenlo. Si publicas cifras que no puedes
respaldar con documentación, tienes exposición legal real (y la referencia tiene el mismo
descargo por la misma razón).
