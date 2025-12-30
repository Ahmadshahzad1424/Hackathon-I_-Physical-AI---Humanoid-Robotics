# Research: High-Conversion UI/UX Starting Page for Physical AI & Humanoid Robotics Book

## Decision: Docusaurus Landing Page Implementation

**Rationale**: Based on the feature specification, the landing page needs to be implemented within the existing Docusaurus setup. The constraints specifically mention using Docusaurus theming with CSS variables and supported plugins only. This approach provides:
- Seamless integration with the existing book structure
- Responsive design out of the box
- Easy deployment to GitHub Pages
- Customizable styling with CSS variables

## Decision: Dark Mode Styling with Neon Accents

**Rationale**: The specification requires a futuristic or clean SaaS-style dark UI with dark slate/black background and neon blue or purple accents. This styling approach:
- Creates a strong AI/robotics identity
- Provides good contrast for readability
- Appeals to the target audience of developers and tech enthusiasts
- Follows modern UI trends for technical content

## Decision: Component Structure for Landing Page Sections

**Rationale**: The landing page needs to display multiple distinct sections (Hero, Book Overview, Modules, CTAs). Using React components will:
- Allow for modular, maintainable code
- Enable reusability of components like the bento grid and accordion cards
- Make it easy to update individual sections independently
- Follow Docusaurus best practices

## Alternatives Considered:

1. **Full Custom React App vs Docusaurus Integration**:
   - Alternative: Create a separate React application
   - Chosen Docusaurus because it maintains consistency with the existing book structure and deployment process

2. **Bento Grid vs Accordion Cards for Modules**:
   - Alternative: Use only one of these UI patterns
   - Research shows both have their place - bento grid for visual appeal, accordion for information density
   - Decision: Implement bento grid as primary, with accordion as fallback if needed

3. **Color Palette Options**:
   - Alternative: Different color schemes (green/teal, orange/amber)
   - Chose neon blue/purple because it aligns with the futuristic/tech aesthetic requested

## Technical Implementation Approach:

1. **Hero Section**: Custom React component with book title, theme, and learning outcomes
2. **Book Overview**: Component explaining scope, tools, and skills gained
3. **Modules Display**: Bento grid component for module cards with descriptions
4. **CTA Buttons**: High-contrast buttons for "Read the Book" and "Explore Modules"
5. **Styling**: CSS variables for the dark theme with neon accents, responsive design