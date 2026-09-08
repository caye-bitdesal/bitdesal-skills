# bitdesal-draft-idea (Cursor)

Convierte una idea en unas pocas líneas en un brief de producto en **PDF**,
en español y en inglés: idea, requisitos (móvil + backend), competencia,
monetización, riesgos, plan de acción y puntuaciones 1–5 con media.

Variante **Cursor** de esta skill. La de Claude Code está en
`claude/bitdesal-draft-idea/`.

## Cómo invocarlo

En el chat de Cursor:

```text
/bitdesal-draft-idea <tu idea en 3–8 líneas>
```

Si omites el texto, el agente te pedirá esa descripción corta.

## Qué produce

```text
ideas/<slug>/
  idea.json                 # fuente bilingüe
  <slug>-idea-es.pdf        # brief en español
  <slug>-idea-en.pdf        # brief in English
  <slug>-download.html      # botones para guardar donde quieras
```

Al terminar, el agente abre la página de descarga. Cada botón dispara el
diálogo de guardar del navegador. También puedes pegar una ruta de carpeta
para que copie ambos PDF ahí.

## Puntuaciones (1–5, más alto = más atractivo)

| Sección | 1 | 5 |
|---------|---|---|
| Requirements | Muy compleja | Muy poco compleja |
| Competition | Mucha competencia | Ninguna competencia |
| Monetization | Poco potencial económico | Alto potencial a corto y largo plazo |
| Risks | Mucho riesgo | Sin riesgo |
| Action plan | Lento / difícil | Relativamente rápido |

**Total** = suma de las cinco ÷ 5 (un decimal).

## Regenerar los PDF

```bash
python3 .cursor/skills/bitdesal-draft-idea/scripts/generate_idea_pdf.py \
  --brief ideas/<slug>/idea.json \
  --out ideas/<slug>
```

Sin dependencias de Python de terceros.

## Instalación

```bash
cp -r cursor/bitdesal-draft-idea /ruta/a/tu-proyecto/.cursor/skills/
# o personal:
cp -r cursor/bitdesal-draft-idea ~/.cursor/skills/
```
