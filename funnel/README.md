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

Tráfico frío. Se acortó de 17.000 a 11.400 px quitando lo que no cerraba nada:

```
hero          la promesa + el mensaje grande: marca de referente, negocio que se
              adapta a tu vida, y la era de la confianza — no la de la atención
franja        transformaciones de clientes, deslizándose
hitos         la cifra facturada manda, el resto orbita
el problema   no está roto: está SOBRECARGADO · dos pares con ✕ en lo que ya no
              funciona: sistema viejo → Circuito de Contenido · piezas sueltas →
              Arquitectura de Conversión con IA
la transición lo que NO hacemos, tachado → «imperios de referentes»
quién está detrás  los hitos, no el discurso
la reflexión  «¿quién te dijo que tenía que ser difícil?» + tira de fotos de vida
el circuito   ESPIRAL de tres fases: La Órbita (frío) · El Umbral (cálido) ·
              El Núcleo (decide y vuelve a la órbita). Cuanto más al centro, más caliente
la prueba     cuentas de Instagram, solo la captura: sin aro, sin pie y sin marcos
              capturas sin retoque · mapa de 20 países
la llamada    qué pasa en los 45 minutos: diagnóstico · estrategia paso a paso ·
              el programa por dentro. Va justo antes del filtro, no al principio
el filtro · FAQ · agenda
```

Fuera de la página, guardados en `borradores/`: **los tres pilares**, **el gráfico de dos
caminos** y **el muro de fotos**. Ninguno hacía avanzar la venta a tráfico frío.

**Una sola comparativa, no tres.** Tres tarjetas con doce «peros» obligaban a leer;
una tabla de cinco filas se entiende de un vistazo. El bloque «El enredo contra El
Circuito» quedó en `borradores/` porque la tabla ya hace ese trabajo.

**«No somos una agencia, somos una consultora» salió del hero.** Responde una objeción que
el visitante frío todavía no se ha hecho; sigue viva donde sí toca, en el filtro y en el FAQ.

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
