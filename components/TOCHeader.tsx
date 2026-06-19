'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/router'

export function TOCHeader() {
  const router = useRouter()

  useEffect(() => {
    let wrapper: HTMLElement | null = null
    let contentSection: HTMLElement | null = null
    let footerSection: HTMLElement | null = null
    let toggleButton: HTMLElement | null = null

    const setupTOC = () => {
      // Find TOC nav element
      let tocNav = document.querySelector('nav.nextra-toc') as HTMLElement
      if (!tocNav) {
        tocNav = document.querySelector('[aria-label*="Table of Contents"]') as HTMLElement
      }
      if (!tocNav) {
        tocNav = document.querySelector('.nextra-toc') as HTMLElement
      }

      if (!tocNav) {
        console.log('TOC not found')
        return
      }

      // Remove old wrapper if exists
      const oldWrapper = tocNav.querySelector('[data-toc-hide-section]')
      if (oldWrapper) {
        oldWrapper.remove()
      }

      // Load initial visibility state
      const savedVisible = localStorage.getItem('sidebar-right-open')
      const isVisible = savedVisible === null ? true : JSON.parse(savedVisible)

      // Create wrapper with proper structure
      wrapper = document.createElement('div')
      wrapper.setAttribute('data-toc-hide-section', 'true')
      wrapper.style.cssText = `
        display: flex;
        flex-direction: column;
        height: 100%;
      `

      // Get all TOC content first
      const originalHTML = tocNav.innerHTML

      // Create scrollable content section
      contentSection = document.createElement('div')
      contentSection.setAttribute('data-toc-content', 'true')
      contentSection.style.cssText = `
        flex: 1;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 8px 0;
      `
      contentSection.innerHTML = originalHTML

      // Create footer section
      footerSection = document.createElement('div')
      footerSection.setAttribute('data-toc-footer', 'true')
      footerSection.className = 'nx-sticky nx-bottom-0 nx-bg-white dark:nx-bg-dark nx-mx-4 nx-py-4 nx-shadow-[0_-12px_16px_#fff] nx-flex nx-items-center nx-gap-2 dark:nx-border-neutral-800 dark:nx-shadow-[0_-12px_16px_#111] contrast-more:nx-border-neutral-400 contrast-more:nx-shadow-none contrast-more:dark:nx-shadow-none nx-border-t'
      
      // Create toggle button
      toggleButton = document.createElement('button')
      toggleButton.className = 'max-md:nx-hidden nx-h-7 nx-rounded-md nx-transition-colors nx-text-gray-600 dark:nx-text-gray-400 nx-px-2 hover:nx-bg-gray-100 hover:nx-text-gray-900 dark:hover:nx-bg-primary-100/5 dark:hover:nx-text-gray-50'
      
      const updateButtonState = (visible: boolean) => {
        if (!toggleButton || !contentSection || !footerSection) return
        
        if (visible) {
          toggleButton.setAttribute('title', 'Hide table of contents')
          toggleButton.innerHTML = `
            <svg height="12" width="12" viewBox="0 0 16 16" fill="currentColor">
              <path fill-rule="evenodd" d="M11.823 7.177L9.427 4.781A.25.25 0 009 5.004v4.792a.25.25 0 01-.427-.177L11.823 8.177a.25.25 0 010-.354z" class=""></path>
              <path fill-rule="evenodd" d="M16 1.75C16 .784 15.216 0 14.25 0H1.75C.784 0 0 .784 0 1.75v12.5C0 15.216.784 16 1.75 16h12.5A1.75 1.75 0 0016 14.25V1.75zm-1.75-.25a.25.25 0 01.25.25v12.5a.25.25 0 01-.25.25H6.5v-13h7.75zm-12.5 13H11v-13H1.75a.25.25 0 00-.25.25v12.5a.25.25 0 00.25.25z" class=""></path>
            </svg>
          `
          contentSection.style.display = 'block'
          footerSection.setAttribute('data-toggle-animation', 'off')
        } else {
          toggleButton.setAttribute('title', 'Show table of contents')
          toggleButton.innerHTML = `
            <svg height="12" width="12" viewBox="0 0 16 16" fill="currentColor">
              <path fill-rule="evenodd" d="M4.177 7.823l2.396-2.396A.25.25 0 017 5.604v4.792a.25.25 0 01-.427.177L4.177 8.177a.25.25 0 010-.354z" class="nx-origin-[35%] nx-rotate-180"></path>
              <path fill-rule="evenodd" d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v12.5A1.75 1.75 0 0114.25 16H1.75A1.75 1.75 0 010 14.25V1.75zm1.75-.25a.25.25 0 00-.25.25v12.5c0 .138.112.25.25.25H9.5v-13H1.75zm12.5 13H11v-13h3.25a.25.25 0 01.25.25v12.5a.25.25 0 01-.25.25z"></path>
            </svg>
          `
          contentSection.style.display = 'none'
          footerSection.setAttribute('data-toggle-animation', 'hide')
        }
      }

      toggleButton.onclick = (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (!contentSection) return
        const currentVisible = contentSection.style.display !== 'none'
        const newVisible = !currentVisible
        localStorage.setItem('sidebar-right-open', JSON.stringify(newVisible))
        updateButtonState(newVisible)
      }

      footerSection.appendChild(toggleButton)

      // Assemble structure
      wrapper.appendChild(contentSection)
      wrapper.appendChild(footerSection)

      // Clear and replace TOC content
      tocNav.innerHTML = ''
      tocNav.appendChild(wrapper)
      
      // Set initial state
      updateButtonState(isVisible)
    }

    // Setup TOC after page loads
    const timer = setTimeout(setupTOC, 500)

    return () => clearTimeout(timer)
  }, [router.asPath]) // Re-run when route changes

  return null
}
