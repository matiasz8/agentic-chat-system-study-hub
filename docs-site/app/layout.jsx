import { Footer, Layout, Navbar } from 'nextra-theme-docs'
import { Head } from 'nextra/components'
import { getPageMap } from 'nextra/page-map'
import 'nextra-theme-docs/style.css'

export const metadata = {
  title: {
    default: 'Agentic Chat System — Study Hub',
    template: '%s — Agentic Chat Study Hub'
  },
  description: 'Study material for agentic chat systems: LangGraph workflows, generative UI and prompt validation.'
}

const navbar = <Navbar logo={<b>Agentic Chat — Study Hub</b>} />
const footer = <Footer>Internal PoC — NaNLABS</Footer>

export default async function RootLayout({ children }) {
  return (
    <html lang="es" dir="ltr" suppressHydrationWarning>
      <Head />
      <body>
        <Layout navbar={navbar} pageMap={await getPageMap()} footer={footer}>
          {children}
        </Layout>
      </body>
    </html>
  )
}
