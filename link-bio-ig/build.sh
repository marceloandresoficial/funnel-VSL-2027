#!/bin/sh
# Genera index.html (documento completo, desplegable) a partir de page.html
# page.html es la fuente única: también es el cuerpo que se publica como Artifact.
cd "$(dirname "$0")"
{
  printf '%s\n' '<!doctype html>' '<html lang="es">' '<head>'
  printf '%s\n' '<meta charset="utf-8">'
  printf '%s\n' '<meta name="viewport" content="width=device-width, initial-scale=1">'
  printf '%s\n' '<meta name="theme-color" content="#0A0910">'
  printf '%s\n' '<meta name="description" content="Escalling™: el sistema que convierte tu don holístico en un negocio de cinco cifras al mes. Marcelo Andrés Proaño · Edume Global™.">'
  printf '%s\n' '<meta property="og:title" content="Imperio Holístico™ · Marcelo Proaño">'
  printf '%s\n' '<meta property="og:description" content="No tienes un problema de marketing. Tienes un negocio sin CEO.">'
  printf '%s\n' '<meta property="og:type" content="website">'
  printf '%s\n' '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 40 40%27%3E%3Crect width=%2740%27 height=%2740%27 fill=%27%230A0910%27/%3E%3Ccircle cx=%2720%27 cy=%2720%27 r=%2714%27 fill=%27none%27 stroke=%27%23D6A544%27 stroke-width=%272%27/%3E%3Ccircle cx=%2720%27 cy=%2720%27 r=%275%27 fill=%27%23D6A544%27/%3E%3C/svg%3E">'
  cat page.html
  printf '%s\n' '</body>' '</html>'
} > index.html
echo "index.html generado ($(wc -c < index.html) bytes)"
