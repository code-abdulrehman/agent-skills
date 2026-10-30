---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces with high design quality using the project's specific stack (React, Tailwind, Radix UI, Vite). Use this skill for building components, pages, and applications.
license: Complete terms in LICENSE.txt
---

This skill guides creation of distinctive, production-grade frontend interfaces using the **required project stack**. Avoid generic "AI slop" aesthetics while strictly adhering to the technical constraints and **Clinical Security Standards**.

## Project Tech Stack (MANDATORY)

You **MUST** use the following technologies for all frontend implementation:

- **Core**: [React](https://react.dev/) + [Vite](https://vitejs.dev/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) (Use utility-first approach)
- **UI Primitives**: [@radix-ui/primitives](https://www.radix-ui.com/)
- **Data Visualization**: [Recharts](https://recharts.org/)
- **Clinical Data**: [fhir.js](https://github.com/FHIR/fhir.js) (For parsing/displaying clinical resources)
- **Content/Markdown**: `rehype-raw` + `remark-gfm`
- **Real-time**: `socket.io-client`

## Code Reusability & Architecture

- **Atomic Design**: Build reusable primitives (Buttons, Inputs) -> Molecules (Form Groups) -> Organisms (Patient Cards).
- **Custom Hooks**: Extract logic (fetching, form handling, socket events) into `src/hooks`.
- **Component Composition**: Avoid giant "God Components". Break down UI into small, focused functional components.
- **Shared Types**: Use TypeScript interfaces shared from the backend (DTOs) or generate client-side equivalents.

## State Management & Storage Rules

- **Local Storage (Permitted)**: Use *only* for non-sensitive UI persistence:
  - Theme preferences (Dark/Light mode)
  - Data table filters & sorting preferences
  - UI state (Drawer/Sidebar open/closed status)
- **Local Storage (FORBIDDEN)**: NEVER store Authentication Tokens, User PII, or Medical Data (PHI) here.
- **Session & Cookies**: 
  - storage: Use `httpOnly`, `Secure` cookies for Session IDs/Access Tokens.
  - caching: Use `React Query` (or similar) for server state caching/invalidation.

## Security & Reliability (HIPAA/PHI)

- **PHI Protection**: Medical data must live in memory only (React State/Context).
- **Data Masking**: Mask sensitive fields (e.g., SSN, Contact Info) by default in list views.
- **Auto-Logout**: Implement idle timers to clear session if the user is inactive.
- **FHIR Compliance**: When displaying medical data, adhere to FHIR resource structures.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: **STRICTLY** follow the Project Tech Stack above.
- **Differentiation**: What makes this UNFORGETTABLE?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision.

Then implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

**CRITICAL - Theme Integration**:
1. **Check for existing theme**: Use `tailwind.config.js` theme extensions (colors, screens, extend) if available.
2. **Radix Integration**: Wrap Radix primitives with Tailwind classes for styling to ensure accessibility matches aesthetics.
3. **Charts**: Custom style Recharts components to strictly match the application's theme (colors, fonts, tooltips).

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting.
- **Color & Theme**: Commit to a cohesive aesthetic. Use Tailwind colors or CSS variables.
- **Motion**: Use Tailwind's `transition` and `animate` utilities. If complex motion is needed, check for Framer Motion.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow.
- **Backgrounds**: Create atmosphere and depth.

NEVER use generic AI-generated aesthetics.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code. Minimalist designs need restraint and precision.