import nextra from 'nextra'

const withNextra = nextra({
  // Code blocks are indexed by default; keeping that on means you can search for a
  // function or step name and land on the page that uses it.
  search: { codeblocks: true }
})

export default withNextra({
  reactStrictMode: true
})
