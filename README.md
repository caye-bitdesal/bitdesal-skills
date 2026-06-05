# Cursor Agent Skills

Colección pública de [Cursor Agent Skills](https://cursor.com/docs/context/skills): instrucciones reutilizables que guían al agente en flujos de trabajo concretos. Cualquiera puede copiarlas, usarlas y contribuir.

**Licencia:** [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) (GPL-3.0)

## ¿Qué es una skill?

Una skill es un directorio con un archivo `SKILL.md` (y opcionalmente archivos de referencia). Cursor las carga cuando las invocas por nombre o cuando el agente detecta que encajan con tu petición.

## Instalación

Clona este repositorio y copia las skills que necesites en una de estas ubicaciones:

| Ámbito | Ruta | Uso |
|--------|------|-----|
| **Proyecto** | `.cursor/skills/<nombre-skill>/` | Compartida con quien clone el repo del proyecto |
| **Personal** | `~/.cursor/skills/<nombre-skill>/` | Disponible en todos tus proyectos |

Ejemplo:

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cp -r TU_REPO/add-project-case-study /ruta/a/tu-proyecto/.cursor/skills/
```

Estructura esperada tras copiar:

```
.cursor/skills/
└── add-project-case-study/
    ├── SKILL.md
    └── reference.md
```

No instales skills en `~/.cursor/skills-cursor/` — ese directorio es interno de Cursor.

## Uso

1. Copia la skill en `.cursor/skills/` (proyecto) o `~/.cursor/skills/` (personal).
2. Abre Cursor en el proyecto correspondiente.
3. Invoca la skill en el chat, por ejemplo:
   - *"Usa la skill add-project-case-study para añadir el proyecto FooBar"*
   - *"Sigue add-project-case-study y crea la página de caso de estudio"*

El agente leerá `SKILL.md` y seguirá el flujo definido. Algunas skills incluyen un `reference.md` con detalle adicional que el agente consulta cuando hace falta.

## Skills disponibles

| Skill | Descripción | Proyecto / contexto |
|-------|-------------|---------------------|
| [add-project-case-study](./add-project-case-study/) | Crea una página de caso de estudio al estilo Kivra/Yössä (`/projects/{slug}`) y añade la tarjeta del proyecto en `/projects`. Incluye i18n (es/en/fi), assets y variante live o legacy. | [bitdesal-web](https://github.com/caye-bitdesal/bitdesal-web) (Astro + Tailwind) |

## Contribuir

1. Añade un directorio `<nombre-skill>/` con `SKILL.md` y frontmatter (`name`, `description`).
2. Actualiza la tabla de **Skills disponibles** en este README.
3. Abre un pull request.

Convenciones:

- `name` en minúsculas con guiones (máx. 64 caracteres).
- `description` en tercera persona, con qué hace y cuándo usarla.
- Mantén `SKILL.md` conciso; el detalle largo va en `reference.md` u otros archivos enlazados.

## Licencia

Este repositorio se distribuye bajo **GPL-3.0**. Puedes usar, modificar y redistribuir las skills según los términos de la licencia. Al redistribuir código derivado, debes mantener la misma licencia y documentar los cambios.

Ver el archivo `LICENSE` en la raíz del repositorio (o [gnu.org/licenses/gpl-3.0](https://www.gnu.org/licenses/gpl-3.0.html)).
