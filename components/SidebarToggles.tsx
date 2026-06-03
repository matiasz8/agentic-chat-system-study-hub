'use client'

import { useState, useEffect } from 'react'
import { Menu, X, ChevronRight, ChevronLeft } from 'lucide-react'

export function SidebarToggles() {
  const [leftOpen, setLeftOpen] = useState(true)
  const [rightOpen, setRightOpen] = useState(true)

  useEffect(() => {
    // Load initial state from localStorage
    const savedLeftState = localStorage.getItem('sidebar-left-open')
    const savedRightState = localStorage.getItem('sidebar-right-open')
    
    if (savedLeftState !== null) setLeftOpen(JSON.parse(savedLeftState))
    if (savedRightState !== null) setRightOpen(JSON.parse(savedRightState))
  }, [])

  const toggleLeftSidebar = () => {
    const newState = !leftOpen
    setLeftOpen(newState)
    localStorage.setItem('sidebar-left-open', JSON.stringify(newState))
    
    // Trigger the toggle button click on the actual sidebar
    const toggleButton = document.querySelector('[aria-label="Toggle sidebar"]') as HTMLButtonElement || 
                        document.querySelector('button[aria-label*="sidebar" i]') as HTMLButtonElement
    if (toggleButton && typeof (toggleButton as HTMLElement).click === 'function') {
      (toggleButton as HTMLElement).click()
    }
  }

  const toggleRightSidebar = () => {
    const newState = !rightOpen
    setRightOpen(newState)
    localStorage.setItem('sidebar-right-open', JSON.stringify(newState))
    
    // Toggle TOC visibility
    const tocNav = document.querySelector('nav[aria-label*="Table of Contents" i]') as HTMLElement ||
                   document.querySelector('[role="region"][aria-label*="Table" i]') as HTMLElement ||
                   document.querySelector('.nextra-toc') as HTMLElement
    
    if (tocNav) {
      if (newState) {
        (tocNav as HTMLElement).style.display = 'block'
      } else {
        (tocNav as HTMLElement).style.display = 'none'
      }
    }
  }

  return (
    <div className="flex gap-2 items-center">
      <button
        onClick={toggleLeftSidebar}
        className="p-2 hover:bg-gray-200 dark:hover:bg-gray-800 rounded-md transition-colors"
        aria-label={leftOpen ? 'Hide sidebar' : 'Show sidebar'}
        title={leftOpen ? 'Ocultar navegación' : 'Mostrar navegación'}
      >
        {leftOpen ? (
          <ChevronLeft size={20} />
        ) : (
          <Menu size={20} />
        )}
      </button>
      
      <button
        onClick={toggleRightSidebar}
        className="p-2 hover:bg-gray-200 dark:hover:bg-gray-800 rounded-md transition-colors"
        aria-label={rightOpen ? 'Hide table of contents' : 'Show table of contents'}
        title={rightOpen ? 'Ocultar tabla de contenidos' : 'Mostrar tabla de contenidos'}
      >
        {rightOpen ? (
          <ChevronRight size={20} />
        ) : (
          <X size={20} />
        )}
      </button>
    </div>
  )
}
