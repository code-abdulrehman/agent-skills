---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality. Use this skill when the user asks to build web components, pages, artifacts, posters, or applications (examples include websites, landing pages, dashboards, React components, HTML/CSS layouts, or when styling/beautifying any web UI). Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## When to use
Activate this Skill **always** when user query

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, .html.heex, .ex if needed, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

**CRITICAL - Theme Integration**: Before implementing any styling or design choices:
1. **Check if the app has an existing theme system** (e.g., `Theme` module, theme configuration, category-based theming)
2. **If a theme exists**: Use the theme's colors, typography, sizing, spacing, and other design tokens. Respect the established design system and maintain consistency with the app's visual language.
3. **If no theme exists**: Use appropriate defaults that align with the aesthetic direction, but ensure they can be easily integrated into a theme system later.
4. **Theme-aware components**: When building components, make them theme-aware by accepting theme props or using theme context/hooks when available.

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

## Form UI (Phoenix / Heex)

When designing forms (`.form`, `.input`, modals with forms):

- **Layout**: Use clear hierarchy—group related fields, use spacing (e.g. `space-y-*`, `gap-*`) and sections so the form scans easily. Align labels and inputs consistently (e.g. grid or stacked).
- **Labels**: Always pair inputs with visible, accessible labels (`label` attr on `<.input>` or explicit `<label>`). Use `label_class` or wrapper classes to match the theme.
- **Validation & errors**: Show errors near the field (core_components `<.input>` shows errors via `phx-feedback-for`). Use theme colors for error state (e.g. red/border or subtle background) and keep messages short.
- **Buttons**: Primary submit vs secondary cancel—use distinct styles (e.g. `button1` / `btn-secondary` or theme buttons). Disable submit when invalid (`disabled={!@changeset.valid?}`) with a clear disabled style.
- **Theme**: Use the app theme for borders, backgrounds, text (e.g. `text-base-400`, `border-base-400`, `bg-*`). Keep form controls consistent with the rest of the UI.
- **Accessibility**: Labels, focus states, and error association. Avoid removing outlines without providing a visible focus style.

Backend binding and events are covered in `.cursor/skills/backend/SKILL.md` (Forms, Inputs & Form Event Handling); this section is for visual and UX consistency of forms.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.