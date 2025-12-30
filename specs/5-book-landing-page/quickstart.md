# Quickstart: High-Conversion UI/UX Starting Page for Physical AI & Humanoid Robotics Book

## Prerequisites

- Node.js (v16 or higher)
- npm or yarn package manager
- Git for version control

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd frontend_book
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the development server**
   ```bash
   npm run start
   # or
   yarn start
   ```

4. **Open your browser**
   - Navigate to `http://localhost:3000`
   - The landing page will be visible at the root URL

## Customization

1. **Update book information**
   - Edit the data in `src/components/LandingPage/HeroSection.jsx` for book title and description
   - Update `src/components/LandingPage/BookOverview.jsx` with scope, tools, and skills

2. **Modify module cards**
   - Update the module data in `src/components/LandingPage/ModulesGrid.jsx`
   - Add or remove modules as needed

3. **Adjust styling**
   - Modify CSS variables in `src/css/custom.css`
   - Update color palette (dark slate/black background with neon blue/purple accents)

## Building for Production

```bash
npm run build
# or
yarn build
```

## Deployment

The site is configured for deployment to GitHub Pages:
1. Build the site: `npm run build`
2. The static files will be in the `build/` directory
3. Deploy these files to your hosting platform (GitHub Pages)

## Development Workflow

1. Make changes to the components in `src/components/LandingPage/`
2. The development server will automatically reload
3. Test responsive behavior using browser dev tools
4. Ensure all CTAs are visible and functional
5. Verify the dark mode styling looks correct