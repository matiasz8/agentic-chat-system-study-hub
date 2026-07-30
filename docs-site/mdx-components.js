// Nextra 4 requires a file at the project root exporting exactly this hook name.
// It merges the docs theme's MDX components with any page-level overrides.
import { useMDXComponents as getThemeComponents } from 'nextra-theme-docs'

const themeComponents = getThemeComponents()

export function useMDXComponents(components) {
  return {
    ...themeComponents,
    ...components
  }
}
