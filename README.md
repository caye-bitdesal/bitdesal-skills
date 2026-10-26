# Agent Skills (Cursor y Claude)

Colección pública de [Agent Skills](https://agentskills.io/specification):
instrucciones reutilizables que guían al agente en flujos de trabajo concretos.
Hay una variante por programa cuando aplica. Cualquiera puede copiarlas, usarlas y contribuir.

**Licencia:** [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) (GPL-3.0)

## ¿Qué es una skill?

Una skill es un directorio con un archivo `SKILL.md` (y opcionalmente archivos
de referencia). Cursor y Claude Code las cargan cuando las invocas por nombre
o cuando el agente detecta que encajan con tu petición.

## Estructura del repo

```text
cursor/<nombre-skill>/     # variantes para Cursor  → .cursor/skills/
claude/<nombre-skill>/     # variantes para Claude  → .claude/skills/
```

Cada carpeta de skill lleva su `SKILL.md` **en la raíz** de esa skill. No
anides `cursor/` o `claude/` *dentro* de la skill.

### Inventario rápido

| Carpeta | Skills |
|---------|--------|
| **cursor/** | `add-project-case-study`, `bitdesal-cleanup`, `bitdesal-create-ci`, `bitdesal-create-kmp-spec`, `bitdesal-create-review`, `bitdesal-create-spec`, `bitdesal-create-ticket`, `bitdesal-draft-idea`, `bitdesal-evaluate`, `bitdesal-kmp-use-case-spec`, `bitdesal-review-last-commit` |
| **claude/** | `bitdesal-create-ci`, `bitdesal-draft-idea`, `bitdesal-kmp-use-case-spec` |

Si una skill solo aparece en `cursor/`, hoy no hay variante para Claude Code en
este repo (puedes copiar la de Cursor y adaptar rutas `.cursor/` → `.claude/` si lo necesitas).

## Instalación

Clona este repositorio y copia **solo** la carpeta del programa que uses:

| Programa | Desde este repo | Destino (proyecto) | Destino (personal) |
|----------|-----------------|--------------------|--------------------|
| **Cursor** | `cursor/<nombre-skill>/` | `.cursor/skills/<nombre-skill>/` | `~/.cursor/skills/<nombre-skill>/` |
| **Claude Code** | `claude/<nombre-skill>/` | `.claude/skills/<nombre-skill>/` | `~/.claude/skills/<nombre-skill>/` |

Cursor:

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cp -r TU_REPO/cursor/bitdesal-draft-idea /ruta/a/tu-proyecto/.cursor/skills/
```

Claude Code:

```bash
cp -r TU_REPO/claude/bitdesal-draft-idea /ruta/a/tu-proyecto/.claude/skills/
```

Estructura esperada tras copiar (Cursor):

```text
.cursor/skills/
└── bitdesal-draft-idea/
    ├── SKILL.md
    └── …
```

No instales skills en `~/.cursor/skills-cursor/` — ese directorio es interno de Cursor.

## Uso

1. Copia la skill a la ruta de tu programa (tabla de arriba).
2. Abre el proyecto en Cursor o Claude Code.
3. Invoca la skill en el chat, por ejemplo:
   - *"Usa la skill add-project-case-study para añadir el proyecto FooBar"*
   - *"/bitdesal-draft-idea app para que vecinos se presten herramientas en el edificio"*

El agente leerá `SKILL.md` y seguirá el flujo definido.

## Skills disponibles

| Skill | Descripción | Cursor | Claude | Contexto |
|-------|-------------|--------|--------|----------|
| [add-project-case-study](./cursor/add-project-case-study/) | Crea una página de caso de estudio al estilo Kivra/Yössä (`/projects/{slug}`) y añade la tarjeta del proyecto en `/projects`. Incluye i18n (es/en/fi), assets y variante live o legacy. | [cursor/](./cursor/add-project-case-study/) | — | [bitdesal-web](https://github.com/caye-bitdesal/bitdesal-web) |
| [bitdesal-cleanup](./cursor/bitdesal-cleanup/) | Encuentra y elimina código Kotlin/Android muerto en Weel (cadenas inalcanzables, recursos sin uso). | [cursor/](./cursor/bitdesal-cleanup/) | — | Weel (`picalandroid`) |
| [bitdesal-create-ci](./cursor/bitdesal-create-ci/) | Añade GitHub Actions de CI y revisión de código con IA (Android, KMP o Ktor server). Sin workflow de release. | [cursor/](./cursor/bitdesal-create-ci/) | [claude/](./claude/bitdesal-create-ci/) | Cualquier repo Kotlin con Gradle |
| [bitdesal-create-kmp-spec](./cursor/bitdesal-create-kmp-spec/) | Entrevista una feature KMP (ámbito de clientes primero: server, Android, desktop, web, iOS), luego genera `spec.json` + HTML con tareas incrementales en `:core`, `:server` y `:app:shared`. | [cursor/](./cursor/bitdesal-create-kmp-spec/) | — | Proyectos KMP tipo Tabala (`specs/<slug>/`) |
| [bitdesal-create-review](./cursor/bitdesal-create-review/) | *(Legacy)* Solo revisión de código con IA para apps Android. Preferir `bitdesal-create-ci` para CI + review. | [cursor/](./cursor/bitdesal-create-review/) | — | Cualquier repo Android |
| [bitdesal-create-spec](./cursor/bitdesal-create-spec/) | Entrevista una feature (enfoque Android/UI), genera `spec.json` + HTML autocontenido con imágenes y tareas incrementales. | [cursor/](./cursor/bitdesal-create-spec/) | — | Apps Android (`specs/<slug>/`) |
| [bitdesal-create-ticket](./cursor/bitdesal-create-ticket/) | Redacta un issue de GitHub a partir de una descripción breve, aclara dudas y lo crea con `gh`. | [cursor/](./cursor/bitdesal-create-ticket/) | — | Cualquier repo con `gh` |
| [bitdesal-draft-idea](./cursor/bitdesal-draft-idea/) | Convierte unas líneas de idea en briefs PDF (ES y EN): requisitos, competencia, monetización, riesgos, plan de acción, puntuaciones 1–5 y página de descarga. | [cursor/](./cursor/bitdesal-draft-idea/) | [claude/](./claude/bitdesal-draft-idea/) | Cualquier repo (`ideas/<slug>/`) |
| [bitdesal-evaluate](./cursor/bitdesal-evaluate/) | Triaje de hallazgos del bot de review en PR: validar, aplicar fixes mínimos, un commit por issue resuelto. | [cursor/](./cursor/bitdesal-evaluate/) | — | Tras `bitdesal-create-ci` / review en PR |
| [bitdesal-kmp-use-case-spec](./cursor/bitdesal-kmp-use-case-spec/) | Analiza ViewModels, repositorios, Composables y READMEs del proyecto; genera spec por casos de uso (`analyze-all` para todo el repo), cobertura vs huecos, tests deduplicados y diagramas Mermaid. | [cursor/](./cursor/bitdesal-kmp-use-case-spec/) | [claude/](./claude/bitdesal-kmp-use-case-spec/) | Proyectos KMP (`specs/kmp-use-cases/…`) |
| [bitdesal-review-last-commit](./cursor/bitdesal-review-last-commit/) | Revisa el último commit local (KMP: Kotlin, Gradle, SQLDelight, config) con Claude Fable; seguimiento de hallazgos abiertos por rama; hook tras `git commit` o `/bitdesal-review-last-commit`. | [cursor/](./cursor/bitdesal-review-last-commit/) | — | Proyectos KMP con skill + hook instalados |

## Contribuir

1. Si la skill debe existir en ambos programas, añade
   `cursor/<nombre-skill>/` y `claude/<nombre-skill>/`, cada uno con su
   `SKILL.md` en la raíz (rutas de instalación acordes: `.cursor/skills/` vs
   `.claude/skills/`).
2. Si solo aplica a Cursor, colócala únicamente bajo `cursor/`.
3. Actualiza la tabla de **Skills disponibles** y el **Inventario rápido** en este README.
4. Abre un pull request.

Convenciones:

- `name` en minúsculas con guiones (máx. 64 caracteres).
- `description` en tercera persona, con qué hace y cuándo usarla.
- Mantén `SKILL.md` conciso; el detalle largo va en `reference.md` u otros archivos enlazados.

## Licencia

Este repositorio se distribuye bajo **GPL-3.0**. Puedes usar, modificar y redistribuir las skills según los términos de la licencia. Al redistribuir código derivado, debes mantener la misma licencia y documentar los cambios.

Ver el archivo `LICENSE` en la raíz del repositorio (o [gnu.org/licenses/gpl-3.0](https://www.gnu.org/licenses/gpl-3.0.html)).
