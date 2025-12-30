---
id: 1
title: Create Constitution
stage: constitution
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: claude
command: /sp.constitution
labels: [constitution,spec-first,technical-book,rag]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

```
/sp.constitution

Project: AI-Spec-Driven Technical Book with Embedded RAG Chatbot

Core principles:
- Spec-first workflow using Spec-Kit Plus
- Technical accuracy based on official documentation
- Clear, developer-focused writing
- Reproducible setup and deployment

Key standards:
- Book written with Docusaurus and deployed on GitHub Pages
- Content authored using Claude Code
- RAG chatbot grounded only in book content or user-selected text
- Stack: OpenAI Agents/ChatKit SDKs, FastAPI, Neon Serverless Postgres, Qdrant Cloud (Free Tier)
- Runnable, well-documented code examples

Constraints:
- GitHub-based source control
- Free-tier compatible infrastructure only
- No hallucinated APIs, libraries, or responses
- End-to-end reproducibility required

Success criteria:
- Live book accessible on GitHub Pages
- Embedded RAG chatbot answers questions accurately from book content
- User-selected text queries handled correctly
- Project can be cloned and run by a third party without modification
```

## Response snapshot

Constitution created for AI-Spec-Driven Technical Book with Embedded RAG Chatbot project with the following principles:
- I. Spec-First Workflow
- II. Technical Accuracy
- III. Reproducible Setup
- IV. Free-Tier Compatibility
- V. RAG Accuracy
- VI. Docusaurus Standards

Plus constraints, development workflow, and governance sections.

## Outcome

- ✅ Impact: Created initial project constitution with 6 core principles
- 🧪 Tests: N/A
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Plan specification using /sp.specify
- 🧠 Reflection: Constitution properly captures all specified requirements and constraints

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Not applicable
- Next experiment (smallest change to try): Begin specification work