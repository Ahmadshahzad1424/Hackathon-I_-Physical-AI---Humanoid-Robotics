<!--
Sync Impact Report:
- Version change: N/A → 1.0.0
- Modified principles: All principles newly defined
- Added sections: Core Principles, Constraints, Development Workflow, Governance
- Removed sections: None
- Templates requiring updates: ✅ All templates updated to align with new principles
- Follow-up TODOs: None
-->
# AI-Spec-Driven Technical Book with Embedded RAG Chatbot Constitution

## Core Principles

### I. Spec-First Workflow
All development follows the Spec-Kit Plus methodology; Every feature must have complete specification before implementation begins; Requirements, architecture, and tasks are documented before code is written.

### II. Technical Accuracy
All content must be based on official documentation and verified sources; No hallucinated APIs, libraries, or technical information; All code examples must be runnable and well-documented with clear explanations.

### III. Reproducible Setup
All infrastructure and deployment processes must be completely reproducible; Third-party developers must be able to clone and run the project without modification; GitHub-based source control with clear documentation of all dependencies.

### IV. Free-Tier Compatibility
All infrastructure choices must remain within free-tier limits; Stack components (OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, Qdrant Cloud) must be cost-effective and sustainable.

### V. RAG Accuracy
The embedded chatbot must only respond based on book content or user-selected text; No responses outside the grounded knowledge base; Clear attribution to source material required.

### VI. Docusaurus Standards
All book content must follow Docusaurus best practices; Clean, developer-focused writing with consistent formatting; Accessible and well-structured documentation.

## Constraints

- GitHub-based source control with proper branching and PR workflows
- Free-tier compatible infrastructure only (no paid services)
- No hallucinated APIs, libraries, or responses from the RAG system
- End-to-end reproducibility required for all components
- All code examples must be runnable and well-documented
- Deployment on GitHub Pages for public accessibility

## Development Workflow

- All features must begin with a complete specification using Spec-Kit Plus templates
- Code authored using Claude Code with precise file references and minimal changes
- Testing required for all functionality with clear acceptance criteria
- Documentation updates must accompany all code changes
- Review process includes validation of technical accuracy and reproducibility

## Governance

This constitution supersedes all other development practices and must be followed for all project activities. All pull requests and code reviews must verify compliance with these principles. Any architectural changes that affect the core principles require constitution amendments with proper documentation and approval. All team members are responsible for maintaining these standards throughout the development lifecycle.

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
