import nextra from 'nextra'

const withNextra = nextra({
  theme: 'nextra-theme-docs',
  themeConfig: './theme.config.jsx',
})

export default withNextra({
  reactStrictMode: true,
  webpack: (config, { isServer }) => {
    if (isServer) {
      config.ignoreWarnings = [{ module: /refractor/ }]
    }
    return config
  },
})
