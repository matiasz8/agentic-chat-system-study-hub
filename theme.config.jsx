import { useRouter } from 'next/router'

export default {
  logo: <span>🤖 Agentic Chat System</span>,
  project: {
    link: 'https://github.com/matiasz8/agentic-chat-system-study-hub',
  },
  chat: {
    link: 'https://github.com/matiasz8/agentic-chat-system-study-hub/discussions',
  },
  docsRepositoryBase: 'https://github.com/matiasz8/agentic-chat-system-study-hub/blob/main',
  footer: {
    text: '© 2026 NaN Labs - Hub de Estudio | Repo Privado',
  },
  useNextSeoProps() {
    const { asPath } = useRouter()
    if (asPath !== '/') {
      return {
        titleTemplate: '%s – Agentic Hub',
      }
    }
    return {
      title: '🤖 Agentic Chat System - Hub de Estudio Completo',
      description: 'LangGraph + AWS Bedrock + Vercel AI + Validación',
    }
  },
  head: (
    <>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta property="og:title" content="Agentic Chat System - Study Hub" />
      <meta property="og:description" content="Hub completo: LangGraph, AWS, Vercel AI, Testing" />
      <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
    </>
  ),
  darkMode: true,
  sidebar: {
    defaultMenuCollapseLevel: 1,
    toggleButton: true,
  },
}
