# Estudio del Sitio — Edume Global™ 2027

Superficie **interna**. Aquí se diseña el sitio nuevo; en GoHighLevel solo se pega.

Mismo motor que el Estudio de Funnel, con una diferencia que lo cambia todo:
la exportación está pensada para **pegar dentro de GoHighLevel**, no para publicar
un documento suelto.

## Arquitectura

```
Nuevo Sitio Web Edume Global 2027/
  sitio.json           ← el mapa del sitio: qué páginas hay, en qué orden y área
  estudio.html         ← el cascarón del estudio (fuente de la UI)
  paginas/
    _kit.css           ← Kit de Marca: tokens y componentes de TODAS las páginas
    _kit.js            ← comportamiento compartido + puente con el estudio
    <slug>.html        ← una página por archivo, con cabecera <!--PAGINA {...} -->
    borradores/        ← versiones anteriores que quieras conservar
  recursos/            ← imágenes y archivos del sitio
  build.py / build.sh  ← ensambla el estudio
  fotos.py             ← empaqueta recursos/clientes/ en paginas/_fotos.js
  previa.py            ← una página suelta, sin el estudio alrededor
  revisar.py           ← revisión estática antes de dar una página por buena
  artifact.html        ← generado · lo que se publica como Artifact
  index.html           ← generado · documento completo, se abre en el navegador
```

```bash
./build.sh
```

## El mapa del sitio manda

`sitio.json` es la única lista. Añadir una entrada **crea la página**:

```json
{ "slug": "quienes-somos", "nombre": "Quiénes somos", "icono": "◈",
  "grupo": "Sitio", "descripcion": "Autoridad y método.",
  "origen": "https://…kajabi…/quienes-somos" }
```

Al siguiente `./build.sh` aparece `paginas/quienes-somos.html` como esbozo, ya con
el Kit puesto, y con el enlace de Kajabi a la vista dentro de la propia página.
`grupo` separa el riel izquierdo por áreas (Sitio · Programas · Legales…).
Renombrar en `sitio.json` renombra la página: el mapa gana sobre la ficha.

## De aquí a GoHighLevel

En el estudio, **Ver código** tiene dos modos:

| Modo | Qué es | Para qué |
|---|---|---|
| **Bloque GoHighLevel** | Un fragmento: `<link>` de fuentes + `<style>` + `<div id="eg-pagina">` + `<script>` | Pegar en un elemento de código de GHL |
| **Documento completo** | HTML autónomo con su `<head>` | Subir a un hosting o abrir en el navegador |

El bloque de GHL no es el documento con otro envoltorio. **Todo el CSS se reescribe
para vivir dentro de `#eg-pagina`**: `body{…}` pasa a ser `#eg-pagina{…}`, y cada
regla queda acotada al contenedor. Consecuencia práctica: el diseño no puede romper
nada de la plantilla de GHL, y ningún estilo de GHL puede entrar a deformar la página.

Lo único que sale del contenedor son cuatro reglas que neutralizan los envoltorios
de GHL (`c-section`, `c-row`, `c-column`) **solo cuando contienen el bloque**, para
que la página ocupe el ancho completo en vez de quedarse dentro de una columna de
960 px con relleno.

**Previsualizar** en modo GHL no enseña la página a secas: la mete en un simulacro
de la maquetación de GoHighLevel — sección estrecha, con relleno — para que veas
antes de pegar que el bloque rompe el contenedor como debe.

### Pasos en GHL

1. Sites → la página → **Add Element → Custom Code / HTML**.
2. Ponlo en una fila a ancho completo, sin relleno.
3. **Copiar todo** en el estudio y pegar ahí dentro.
4. Guardar y ver la página publicada, no solo el editor: el editor de GHL mete su
   propio andamiaje y a veces recorta lo que el `<style>` hace.

Lo que GHL debe seguir manejando él (formularios, calendarios, pagos, popups) no se
diseña aquí: en la página van **huecos de recurso** (`data-res`) donde después pegas
el código de incrustación desde el panel **Ver recursos**.

## Las herramientas (riel derecho)

| | Qué hace |
|---|---|
| **Versión PC / Tablet / Móvil** | Cambia el ancho del lienzo. La página es la real, no una simulación. |
| **Editar texto** | Clic en cualquier texto → escribes encima. Tamaño, grosor, espaciado, interlineado, color del kit, alineación, espacio y ancho del bloque. `Ctrl+Z` deshace. `Esc` sale. |
| **Bloques y secciones** | Reordena, oculta y añade secciones desde la librería. |
| **Ver recursos** | Inventario de lo que la página necesita, contado. Pegas un enlace o subes una imagen y te dice cuántos faltan. |
| **Ver código** | Los dos modos de arriba. Copiar, previsualizar o descargar. |
| **Historial** | Instantáneas del trabajo, para volver atrás. |
| **Kit de marca** | Los colores (editables: cambias uno y cambia el sitio entero), la escala tipográfica y los componentes. |

## El trabajo no se pierde

El estudio guarda en el navegador. Para que sobreviva a un rebuild:

```bash
python3 build.py --importar ~/Downloads/artifact-descargado.html
```

Eso escribe `estado.json`, y a partir de ahí cada `./build.sh` conserva recursos y
ediciones. Sin ese paso, un rebuild deja el estado que ya tuviera `artifact.html`.

## Antes de dar una página por buena

```bash
python3 revisar.py
```

Caza las tres cosas que rompen una página en silencio: un `#id` que el JS toca y no
existe, una clase usada en el markup sin ninguna regla de CSS, y JS o CSS que no
compilan.

---

## La home nueva

`paginas/inicio.html` · once secciones, en el lenguaje nuevo: marfil y berenjena,
Playfair Display para los titulares, Montserrat para todo lo demás, y el aire
vertical de una página de Apple en vez del ritmo apretado de Kajabi.

| # | Sección | Qué hace |
|---|---|---|
| 1 | Hero | Promesa, dos CTA y las cuatro cifras que animan al entrar |
| 2 | Cinta de confianza | Los cinco logos corporativos, deslizándose |
| 3 | Diferenciador | El sueño sin sistema · el sistema sin alma · el tercero |
| 4 | Metodología | Los tres pilares, uno por tarjeta, con sus componentes |
| 5 | Resultados | Muro de capturas de banco y facturación, en dos cintas |
| 6 | Collage | Las fotos cara a cara con clientes |
| 7 | Cuentas reales | Las 20 cuentas de Instagram, con nicho y seguidores |
| 8 | El mundo | Globo giratorio con los 20 países y el ranking |
| 9 | Programas | Aceleradora 100K™ y One Billion Mastermind |
| 10 | Fundador | Marcelo, con sus cifras |
| 11 | Cierre | La llamada, con la condición de entrada |

La home de hoy queda guardada como **Inicio (Kajabi actual)**, replicada al píxel
(1824 px de alto exactos, mismas medidas sección a sección), para comparar las dos
en el estudio sin abrir Kajabi.

### Lo que es real y lo que falta

Real, tomado de tu propio funnel: las 220 escaladas, los 20 países con sus 220 casos,
las 20 cuentas de clientes con nicho y seguidores, las 15 fotos cara a cara, las cifras
del fundador y los tres pilares con sus componentes.

**A propósito vacío:** las 12 capturas de banco y facturación. No invento cifras de
facturación de nadie. Cárgalas desde «Ver recursos» — y hasta que no cargues ninguna,
la sección entera **no se publica**: el bloque que copias a GoHighLevel sale sin ella.

### Las caras van dentro de la página

Las 15 fotos con clientes viajan **embebidas**: `fotos.py` toma los originales de
`recursos/clientes/`, los reduce a 320 px y los deja en `paginas/_fotos.js`, que el
estudio inyecta en cada página. Consecuencia: al pegar el bloque en GoHighLevel las
caras ya están dentro y no dependen de ningún servidor.

Las mismas caras se reutilizan en las tarjetas de «Gente real, cuentas reales» — 15
de las 20 cuentas tienen foto; las otras cinco muestran su inicial. Reutilizar la
misma imagen no pesa nada: es el mismo dato.

```bash
python3 fotos.py     # tras añadir o cambiar una foto en recursos/clientes/
```

Cuesta unos 275 KB. Si prefieres aligerar la página publicada, sube las fotos a
GoHighLevel y pega las URLs desde «Ver recursos»: los huecos siguen declarados.

### Una cosa pendiente

**Logo para fondo claro.** El logo actual lleva el texto en blanco. Sobre la cabecera
marfil se muestra ennegrecido por CSS (`filter:brightness(0)`), que funciona pero
pierde el color de la marca. Sube la versión de texto oscuro y quita ese filtro en
`paginas/inicio.html`.

### Marcas que entiende el exportador

| Atributo | Qué provoca |
|---|---|
| `data-res` | Declara un hueco de recurso: aparece en «Ver recursos» |
| `data-res-opcional` | Ese hueco, si sigue vacío, no se publica |
| `data-quitar-si-vacio` | Esta tarjeta, sin imagen cargada dentro, no se publica |
| `data-galeria` / `data-galeria-caja` | Una galería que se quedó sin piezas no se publica vacía |
| `data-si-vacio` | Esta sección, sin una sola pieza cargada, no se publica |
| `data-tono="oscuro"` | La cabecera se vuelve oscura sobre esta sección |

### Red de seguridad

La página no depende de que el navegador informe de qué está a la vista. Si a 1,3 s
nadie ha informado —pasa dentro de algunos editores incrustados, y el de GoHighLevel
es uno— se muestra todo de golpe: contadores, barras, globo y revelados. Mejor sin
animación de entrada que una página en blanco.

## Ver una página sola

```bash
python3 previa.py            # la home
python3 previa.py programa   # cualquier otra
```

Escribe `previa.html`: la página con su kit y sus fotos, sin el estudio alrededor.
Sirve para verla como la verá el visitante, abrirla en el móvil o enseñársela a
alguien sin darle el estudio entero. Se regenera cada vez; no la edites.
