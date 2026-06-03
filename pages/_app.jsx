import { useRouter } from 'next/router'
import { TOCHeader } from '../components/TOCHeader'

export default function App({ Component, pageProps }) {
  return (
    <>
      <TOCHeader />
      <Component {...pageProps} />
    </>
  )
}
