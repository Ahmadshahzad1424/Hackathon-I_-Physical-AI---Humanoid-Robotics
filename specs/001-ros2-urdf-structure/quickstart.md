# Quickstart: ROS 2 for Physical AI & Humanoid Robotics Documentation

## Prerequisites

- Node.js 18+ installed
- Git installed
- Basic knowledge of ROS 2 concepts (helpful but not required)

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```
   This will start the Docusaurus server and open the documentation site in your browser at `http://localhost:3000`.

## Project Structure

```
docs/                    # Documentation files
├── intro.md            # Introduction to the documentation
├── ros2-basics/        # Chapter 1: ROS 2 fundamentals
├── ros2-communication/ # Chapter 2: ROS 2 communication
└── urdf-structure/     # Chapter 3: URDF structure
```

## Adding New Content

1. **Create a new markdown file** in the appropriate directory
2. **Add it to the sidebar** in `sidebars.js`
3. **Use Docusaurus features** like:
   - Code blocks with syntax highlighting
   - Admonitions for notes and warnings
   - Math equations using KaTeX
   - Diagrams using Mermaid

## Building for Production

```bash
npm run build
```

This creates a `build/` directory with a production-ready version of the site that can be deployed to GitHub Pages.

## Deployment

The site is configured for GitHub Pages deployment. After building, the contents of the `build/` directory can be deployed to the `gh-pages` branch or used with GitHub Actions for automated deployment.

## Running Examples

Many chapters include ROS 2 and URDF examples. These can be found in the `static/examples/` directory and are referenced from the documentation. To run ROS 2 examples, you'll need a ROS 2 installation (Humble Hawksbill or later recommended).