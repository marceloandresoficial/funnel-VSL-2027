# Estudio de Funnel — Escalling™

Superficie **interna**. No la ve ningún cliente: es donde tú y yo construimos el funnel.

## Arquitectura

```
funnel/
  studio.html          ← el cascarón del estudio (fuente de la UI)
  paginas/
    _kit.css           ← Kit de Marca: tokens y componentes de TODO el funnel
    _kit.js            ← comportamiento compartido + puente con el estudio
    vsl.html               esbozo
    vsl-retargeting.html   esbozo
    sesion-confirmada.html esbozo
    preparacion.html       esbozo
    programa.html          esbozo
    bio-instagram.html     LISTA
    borradores/        ← primeras versiones completas que escribí antes de tu aviso
  build.py / build.sh  ← ensambla todo
  artifact.html        ← generado · lo que se publica
  index.html           ← generado · documento completo, desplegable
```

Cada página vive en su propio archivo con una cabecera `<!--PAGINA {...} -->`.
El estudio las carga en un iframe aislado, así que una página no puede romper a otra.

```bash
./build.sh
```

## Las herramientas (riel derecho)

| | Qué hace |
|---|---|
| **Versión PC / Tablet / Móvil** | Cambia el ancho del lienzo. La página es la real, no una simulación. |
| **Editar texto** | Clic en cualquier texto → escribes encima. El panel da tamaño de letra, grosor, espaciado, interlineado, color del kit, alineación, y espacio y ancho del bloque. `Ctrl+Z` deshace. `Esc` sale. |
| **Ver recursos** | Inventario de todo lo que la página necesita, contado. Pegas un enlace o subes una imagen y te dice cuántos faltan. El punto naranja en el icono avisa cuando falta algo. |
| **Ver código** | El HTML final de la página, con los cambios y recursos ya aplicados. Copiar o descargar. **Guardar lo regenera y lo deja abierto**, con la hora arriba, listo para copiar y pegar. |
| **Kit de marca** | Los 6 colores (editables: cambias uno y cambia en las 6 páginas), la escala tipográfica completa con tamaños y pesos, las 3 voces tipográficas y los componentes. |

### Copiar el código

La vista se recorta a 200 000 caracteres para que el panel no se atasque, y lo dice
en un aviso arriba. **`Copiar todo` copia el archivo entero**, no lo que ves: la VSL
son 3,1 millones de caracteres. No selecciones el texto a mano — copiarías un HTML
cortado por la mitad.

## El funnel (riel izquierdo)

Las 6 páginas en orden, arrastrables para reordenar. Cada una muestra su estado
(esbozo / lista) y cuántos recursos lleva cargados. **Agregar página** crea una nueva
con el Kit ya aplicado.

### Mapa de la página

Debajo de la lista, la página **entera** en miniatura — como una captura de arriba
abajo. Se enciende con el botón **Mapa** o con la tecla `M`.

No es un segundo render: es un **clon estático** del documento vivo, sin scripts ni
animaciones y con los canvas convertidos en imagen. Por eso muestra exactamente lo que
tienes delante y cuesta poco. Las unidades de ventana (`100svh`) se congelan al valor
real del lienzo, para que el hero no se estire al medir la página completa.

| | |
|---|---|
| **Pasar el cursor** | ilumina el bloque y muestra su nombre |
| **Clic** | lleva el lienzo grande a ese bloque |
| **Arrastrar** | recorre la página como una barra de scroll |
| **Marco dorado** | qué trozo estás viendo ahora mismo |
| **Rayado diagonal** | bloque oculto |
| **Aa** | fija todos los nombres a la vista |
| **↻** | vuelve a dibujar |

Sigue la vista activa: en móvil dibuja el móvil. Se redibuja solo al editar, al cambiar
de página y al cambiar de vista.

## Cómo se guarda

1. **Automático, en tu navegador.** Cada cambio se guarda solo. Si el navegador bloquea el
   almacenamiento, el estudio lo dice arriba (`sin memoria`) y sigue funcionando.
2. **Botón Guardar.** Publica una versión nueva del artifact con todo tu trabajo dentro.
   La página se recarga y vuelve a donde estabas.
3. **Exportar.** Descarga el HTML de la página actual, listo para subir a tu hosting.

## Tu trabajo sobrevive a los rebuilds

Cuando pulsas **Guardar**, el estado (recursos cargados, ediciones de texto y estilo,
colores del kit, páginas que creaste) queda embebido en el artifact publicado.

Para que yo no lo pise al reconstruir:

```bash
# 1 · traer lo guardado desde el artifact publicado
python3 build.py --importar <artifact-descargado.html>   # → estado.json

# 2 · reconstruir: build.py inyecta estado.json de vuelta
./build.sh
```

`build.sh` sin más también conserva lo que ya tuviera `artifact.html`, así que un rebuild
normal nunca borra nada. `estado.json` es el respaldo legible de tu trabajo — vale la pena
versionarlo.

## Estado actual

| Página | Estado |
|---|---|
| **VSL** | Terminada. Tráfico frío, móvil primero. |
| **BIO Instagram** | Terminada. **Imperio Holístico™** — 19 bloques + barra fija, sistema visual propio (`kit:false`). |
| VSL Retargeting · Sesión Confirmada · Preparación · Programa | Esbozo, esperando brief |

### La VSL, por dentro

Hero a una pantalla (promesa + video + botón) · **franja de transformaciones de clientes justo bajo el botón** · barra fija con sigilo de expansión ·
**bloque de hitos** (la cifra facturada manda, el resto orbita) · las dos trampas · **diagrama orbital del método** (3 capas, 13 piezas) ·
circuito de 8 nodos · **cuentas de Instagram en dos filas deslizantes** con tratamiento holográfico ·
**resultados con cifra en otras dos filas** · **muro de fotos** con foco al pasar el cursor ·
**riel de capturas** que se desliza con el dedo (quietas, con foco y contador) · gráfico de dos caminos · rueda semanal ·
mapa mundial interactivo · quién está detrás · filtro sí/no · FAQ · calendario iClosed ·
lupa para ver cualquier prueba en grande · footer legal.

### La revisión automática

```bash
python3 revisar.py
```

Caza en segundos las tres cosas que ya nos rompieron la página **en silencio**:

1. **Un `#id` que el JS toca y que no existe en el HTML.** Un `null` ahí aborta todo el
   resto del `<script>` — así se quedaron vacíos los resultados, el muro, la rueda,
   el gráfico, los pagos y la lupa a la vez.
2. **Una clase usada en el markup sin una sola regla de CSS.** Así el icono de 24×24 de
   «pago recibido» se estiró a pantalla completa: un `$` gigante ocupando toda la VSL.
3. **JS que no compila o CSS con las llaves descuadradas.**

Pásalo antes de cada `./build.sh`. Devuelve 0 si está limpio.

### Reglas que evitan los fallos que ya nos pasaron

- **Nunca `$("#x").innerHTML = …` directo.** En la VSL se usa `pon(sel, html)` y
  `txt(sel, texto)`: si el contenedor no existe, no pasa nada. Una excepción suelta ahí
  se lleva por delante el resto del `<script>` — y eso vació media página sin avisar.
- **Un adorno que sangra a los lados no puede mover la página.** `_kit.css` lleva
  `html{overflow-x:clip}` y los bloques con velo o aura recortan lo suyo. `clip`, no
  `hidden`: no crea contenedor de scroll, así que `position:sticky` sigue vivo.
- **Cifras siempre con separador.** El contador usa `toLocaleString("es-ES")`.
  `data-crudo` en el elemento lo desactiva (años, códigos).
- **Todo componente necesita su CSS.** Sin reglas, un `<svg viewBox="0 0 24 24">` no
  mide 24 px: se estira a lo que le dé el contenedor. `revisar.py` lo detecta.
- **Los selectores de tamaño van al hijo directo.** `.hito b` alcanzaba también al `<b>`
  de dentro del párrafo y lo ponía a 118 px; `.cifra span` hacía lo mismo con el contador.
  Se escriben `.hito > b` y `.cifra > span`.
- **Un `id` no se repite**, ni dentro de dos SVG iguales: los degradados se pisan.
- **Al exportar** se quitan las tarjetas sin imagen, las galerías que quedan vacías,
  los huecos **opcionales** sin cargar y cualquier `section[data-si-vacio]` sin una sola
  prueba dentro. El estudio los sigue mostrando; el visitante no.

### La franja de transformaciones

`TRANSFORMACIONES` en `paginas/vsl.html`, junto al resto de datos editables:

```js
["Alejandro Grajeda","Arquitecto","$5K","$25K","en 90 días"]
//  nombre           rol          arrancó  llegó  plazo
```

Si **arrancó** va vacío, la tarjeta muestra solo la cifra alcanzada, sin flecha.
Hoy hay 3 transformaciones completas y 16 con la cifra de sus mini-portadas.
Cada cliente tiene un hueco de foto opcional (`cara-<nombre>`); sin foto sale su inicial.

### La BIO: Imperio Holístico™

Sistema visual propio, aislado del Kit (`"kit": false` en su cabecera): obsidiana violeta
`#08071A`, oro `#D9B45B`, y Cormorant Garamond / Cinzel / Karla. No hereda nada del funnel.

Reglas del brief que el código respeta y conviene no romper:

- **Una sola animación en toda la página**: los catorce cuadraditos del bloque 05 que se
  ordenan al entrar en pantalla, una vez. `prefers-reduced-motion` los deja ya ordenados.
- **La barra fija no aparece en el hero**, solo desde el bloque 02: ahí compite con el video,
  que es lo que hace el trabajo de confianza.
- **Listas con guion dorado, nunca palomita.** Las palomitas dicen «beneficios»;
  los guiones dicen «diagnóstico».
- **Sin contador, sin cupos, sin chat, sin segundo CTA.** Una sola acción en toda la página.
- Los ocho casos y los seis videos salen de `CASOS` y `VIDEOS`, al principio del `<script>`.
  La cita de un caso se muestra solo si existe: **nunca se inventa una.**

La versión anterior (la modelada sobre strategycoach.us) está en
`paginas/borradores/bio-instagram-strategycoach.html`.

### Falta cargar (5 recursos obligatorios)

- `cta-agenda` — destino del botón principal
- `foto-marcelo` — tu foto en «Quién está detrás»
- `legal-aviso`, `legal-privacidad`, `legal-cookies` — URLs del footer

Las imágenes de clientes ya convertidas están en `fotos/` (25 JPEG). Súbelas con
**⇪ Subir varias**: los huecos llevan el nombre del archivo y el emparejado las coloca solas.

### Formatos de imagen

El navegador **no lee TIFF, HEIC, PSD ni RAW**. El estudio lo detecta y te lo dice.
Para convertir un lote: `sips -s format jpeg -s formatOptions 80 -Z 1100 archivo.tiff --out salida.jpg`

### Peso

El proyecto lleva las imágenes incrustadas en el propio archivo. Para mantenerlo a raya:
el botón **⚖ Reoptimizar** recomprime todo al tamaño real de cada hueco, y el historial
guarda pocas versiones a propósito. Si acumulas muchas fotos, súbelas a tu hosting y pega
la URL en vez de incrustarlas.
