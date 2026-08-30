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
| **Ver código** | El HTML final de la página, con los cambios y recursos ya aplicados. Copiar o descargar. |
| **Kit de marca** | Los 6 colores (editables: cambias uno y cambia en las 6 páginas), la escala tipográfica completa con tamaños y pesos, las 3 voces tipográficas y los componentes. |

## El funnel (riel izquierdo)

Las 6 páginas en orden, arrastrables para reordenar. Cada una muestra su estado
(esbozo / lista) y cuántos recursos lleva cargados. **Agregar página** crea una nueva
con el Kit ya aplicado.

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

**BIO Instagram** está terminada: 11 recursos obligatorios (tu @, el VSL, 3 fotos,
5 videos de caso, el contador) y 16 opcionales (los avatares de la crew).

**Las otras 5 están creadas pero sin diseñar**, esperando tu brief. Cada una muestra en
pantalla lo que necesito de ti:

- El objetivo único de la página y qué acción tiene que provocar.
- Qué le pasa por la cabeza a quien llega (de dónde viene, qué ya sabe).
- Qué bloques quieres: video, prueba social, objeciones, pasos, precio, FAQ…
- El copy o las ideas fuerza que van sí o sí.
- Qué recursos va a tener.

En `paginas/borradores/` quedaron las versiones completas que alcancé a escribir de las
cinco antes de que me dijeras que esperara. Están en tu voz y con tus casos reales —
tómalas como punto de partida o ignóralas.

## Límites conocidos

- **Los videos de YouTube/Vimeo no se reproducen dentro del artifact publicado**: la
  política de seguridad de claude.ai bloquea iframes externos. En `index.html` desplegado
  en tu dominio funcionan normal. La URL sí se guarda y sí sale en el código exportado.
- **Las imágenes subidas se guardan dentro de la página** (reescaladas a 1600 px). Para
  muchas fotos pesadas conviene subirlas a tu hosting y pegar la URL.
