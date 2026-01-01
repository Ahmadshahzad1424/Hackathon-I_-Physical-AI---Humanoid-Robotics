const { themes: prismThemes } = require('prism-react-renderer');

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Advanced Robotics Education Platform',
  favicon: 'img/favicon.jpg',

  // Future flags
  future: {
    v4: true,
  },

<<<<<<< HEAD
  // 1. Site URL (Where your site will be hosted)
  url: 'https://Ahmadshahzad1424.github.io', 
  
  // 2. Base URL (Your repository name with slashes)
  baseUrl: '/Hackathon-I_-Physical-AI---Humanoid-Robotics/',
=======
  // Set the production url of your site here
  url: 'https://hackathon-i-physical-ai-humanoid-ro-tau.vercel.app/,
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',
>>>>>>> fbe4b552d109f4c9fcdd748c923ac89b3879c245

  // 3. GitHub Deployment Config
  organizationName: 'Ahmadshahzad1424', // Changed from PANAVERSITY
  projectName: 'Hackathon-I_-Physical-AI---Humanoid-Robotics', // Updated to match your repo URL

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
          // Updated Edit URL to your repo
          editUrl:
            'https://github.com/Ahmadshahzad1424/Hackathon-I_-Physical-AI---Humanoid-Robotics/tree/main/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Updated Edit URL to your repo
          editUrl:
            'https://github.com/Ahmadshahzad1424/Hackathon-I_-Physical-AI---Humanoid-Robotics/tree/main/',
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],

  themeConfig: {
    image: 'img/logo.jpg',

    // FORCE DARK MODE (Keeps your "Wow" look active)
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },

    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI & Humanoid Robotics Logo',
        src: 'img/logo.jpg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Modules',
        },
        { to: '/blog', label: 'Blog', position: 'left' },
        {
          // Updated to your GitHub Repo
          href: 'https://github.com/Ahmadshahzad1424/Hackathon-I_-Physical-AI---Humanoid-Robotics',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Modules',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'ROS 2 & URDF',
              to: '/docs/urdf-structure/understanding-urdf',
            },
            {
              label: 'Digital Twin',
              to: '/docs/digital-twin/introduction',
            },
            {
              label: 'AI Robot Brain',
              to: '/docs/ai-robot-brain/introduction',
            },
            {
              label: 'Vision-Language-Action',
              to: '/docs/vla/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/docusaurus',
            },
            {
              label: 'Discord',
              href: 'https://discordapp.com/invite/docusaurus',
            },
            {
              label: 'X',
              href: 'https://x.com/docusaurus',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              // Updated to your GitHub Repo
              label: 'GitHub',
              href: 'https://github.com/Ahmadshahzad1424/Hackathon-I_-Physical-AI---Humanoid-Robotics',
            },
          ],
        },
      ],
      // Updated Copyright Name
      copyright: `Copyright © ${new Date().getFullYear()} Ahmad Shahzad. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },
};

module.exports = config;
