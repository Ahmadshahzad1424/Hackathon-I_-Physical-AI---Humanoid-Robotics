import type {ReactNode} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

// Import our new landing page components
import HeroSection from '@site/src/components/LandingPage/HeroSection';
import BookOverview from '@site/src/components/LandingPage/BookOverview';
import ModulesGrid from '@site/src/components/LandingPage/ModulesGrid';
import CTAButtons from '@site/src/components/LandingPage/CTAButtons';

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Physical AI & Humanoid Robotics`}
      description="Comprehensive guide to Physical AI and Humanoid Robotics - Vision-Language-Action models, ROS 2, Digital Twins, and AI-Robot Brains">
      <main className="landing-page">
        <HeroSection />
        <BookOverview />
        <ModulesGrid />
        <CTAButtons />
      </main>
    </Layout>
  );
}
