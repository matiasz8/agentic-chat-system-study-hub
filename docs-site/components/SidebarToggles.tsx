'use client'

import { useState, useEffect } from 'react'
import { Menu, ChevronLeft } from 'lucide-react'

export function SidebarToggles() {
  const [leftOpen, setLeftOpen] = useState(true)

  useEffect(() => {
    // Load initial state from localStorage
    const savedLeftState = localStorage.getItem('sidebar-left-open')

    if (savedLeftState !== null) setLeftOpen(JSON.parse(savedLeftState))
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
    </div>
  )
}
