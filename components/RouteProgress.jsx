'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'

export default function RouteProgress({ 
  route, 
  routeName, 
  modules = [],
  currentPath
}) {
  const router = useRouter()
  const [activeIndex, setActiveIndex] = useState(-1)
  const [completedModules, setCompletedModules] = useState({})
  const [isClient, setIsClient] = useState(false)

  // Cargar progreso desde localStorage al montar
  useEffect(() => {
    setIsClient(true)
    if (typeof window !== 'undefined' && route) {
      const saved = localStorage.getItem(`route_progress_${route}`)
      if (saved) {
        try {
          setCompletedModules(JSON.parse(saved))
        } catch (e) {
          console.error('Error loading progress:', e)
        }
      }
    }
  }, [route])

  // Detectar cuál módulo está activo basado en la URL
  useEffect(() => {
    const path = currentPath || router.asPath
    const active = modules.findIndex(m => path.includes(m.path?.replace(/^\//, '')))
    setActiveIndex(active)
  }, [router.asPath, currentPath, modules])

  // Contar módulos completados (combinar localStorage + props)
  const completedCount = modules.length > 0 ? modules.filter((m, idx) => m.done || completedModules[idx]).length : 0
  const progressPercent = modules.length > 0 ? Math.round((completedCount / modules.length) * 100) : 0

  // Toggle para marcar módulo como completado
  const toggleModule = (idx) => {
    if (!isClient) return
    
    const updated = { ...completedModules }
    if (updated[idx]) {
      delete updated[idx]
    } else {
      updated[idx] = true
    }
    
    setCompletedModules(updated)
    
    // Guardar en localStorage
    if (typeof window !== 'undefined' && route) {
      localStorage.setItem(`route_progress_${route}`, JSON.stringify(updated))
    }
  }

  const isModuleCompleted = (idx) => completedModules[idx] || modules[idx]?.done
  const isCompleted = progressPercent === 100

  // Trigger confetti animation when 100% complete
  useEffect(() => {
    if (isCompleted && typeof window !== 'undefined') {
      // Simple confetti animation by adding class
      const widget = document.querySelector('.route-progress-widget')
      if (widget && !widget.classList.contains('celebration-triggered')) {
        widget.classList.add('celebrating')
        widget.classList.add('celebration-triggered')
        // Remove celebrating class after animation
        setTimeout(() => {
          widget.classList.remove('celebrating')
        }, 3000)
      }
    }
  }, [isCompleted])

  if (!route || modules.length === 0) {
    return null
  }

  return (
    <div className="route-progress-widget">
      <style jsx>{`
        .route-progress-widget {
          background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
          border: 1px solid #cbd5e0;
          border-radius: 12px;
          padding: 16px;
          margin: 16px 0;
          font-size: 14px;
          position: relative;
          overflow: hidden;
        }

        .route-progress-widget.celebrating {
          animation: celebrateShake 0.6s ease-in-out;
          box-shadow: 0 0 30px rgba(102, 126, 234, 0.6), 
                      0 0 60px rgba(118, 75, 162, 0.4);
        }

        @keyframes celebrateShake {
          0%, 100% { transform: scale(1) rotate(0deg); }
          25% { transform: scale(1.05) rotate(2deg); }
          50% { transform: scale(1.1) rotate(-2deg); }
          75% { transform: scale(1.05) rotate(1deg); }
        }

        /* Confetti particles */
        .route-progress-widget.celebrating::before,
        .route-progress-widget.celebrating::after {
          content: '✨🎉🎊⭐🌟💫';
          position: absolute;
          top: 50%;
          left: 50%;
          font-size: 24px;
          pointer-events: none;
          z-index: 10;
          animation: confettiFall 2.5s ease-out forwards;
        }

        .route-progress-widget.celebrating::before {
          animation: confettiFallLeft 2.5s ease-out forwards;
          content: '✨';
        }

        .route-progress-widget.celebrating::after {
          animation: confettiFallRight 2.5s ease-out forwards;
          content: '🎉';
        }

        @keyframes confettiFallLeft {
          0% {
            transform: translate(0, 0) rotate(0deg);
            opacity: 1;
          }
          100% {
            transform: translate(-100px, 150px) rotate(360deg);
            opacity: 0;
          }
        }

        @keyframes confettiFallRight {
          0% {
            transform: translate(0, 0) rotate(0deg);
            opacity: 1;
          }
          100% {
            transform: translate(100px, 150px) rotate(-360deg);
            opacity: 0;
          }
        }

        .dark .route-progress-widget {
          background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
          border-color: #4a5568;
        }

        .route-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 12px;
        }

        .route-title {
          font-weight: 600;
          font-size: 13px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
          color: #2d3748;
        }

        .dark .route-title {
          color: #e2e8f0;
        }

        .progress-badge {
          background: #667eea;
          color: white;
          font-size: 12px;
          padding: 2px 8px;
          border-radius: 12px;
          font-weight: 500;
        }

        .progress-bar {
          width: 100%;
          height: 4px;
          background: #cbd5e0;
          border-radius: 2px;
          overflow: hidden;
          margin-bottom: 12px;
        }

        .dark .progress-bar {
          background: #4a5568;
        }

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
          border-radius: 2px;
          transition: width 0.3s ease;
        }

        .modules-list {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .module-item {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 8px;
          border-radius: 6px;
          font-size: 12px;
          transition: all 0.2s ease;
          color: #4a5568;
          text-decoration: none;
        }

        .dark .module-item {
          color: #cbd5e0;
        }

        .module-link {
          display: flex;
          align-items: center;
          gap: 8px;
          flex: 1;
          text-decoration: none;
          color: inherit;
        }

        .module-item:hover {
          background: rgba(102, 126, 234, 0.1);
          color: #667eea;
        }

        .dark .module-item:hover {
          background: rgba(102, 126, 234, 0.15);
          color: #b0b7ff;
        }

        .module-item.active {
          background: rgba(102, 126, 234, 0.2);
          color: #667eea;
          font-weight: 500;
        }

        .dark .module-item.active {
          background: rgba(102, 126, 234, 0.25);
          color: #b0b7ff;
        }

        .module-status {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 16px;
          height: 16px;
          border-radius: 50%;
          flex-shrink: 0;
        }

        .module-status.done {
          background: #48bb78;
          color: white;
          font-size: 10px;
          font-weight: bold;
        }

        .module-status.pending {
          background: #cbd5e0;
          color: #718096;
          font-size: 11px;
        }

        .dark .module-status.pending {
          background: #4a5568;
          color: #a0aec0;
        }

        .module-status.active {
          background: #667eea;
          color: white;
          animation: pulse 2s infinite;
        }

        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }

        .module-title {
          flex: 1;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .module-checkbox {
          background: none;
          border: 1.5px solid #cbd5e0;
          color: #718096;
          width: 20px;
          height: 20px;
          border-radius: 50%;
          cursor: pointer;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 12px;
          font-weight: bold;
          transition: all 0.2s ease;
          flex-shrink: 0;
          padding: 0;
        }

        .module-checkbox:hover {
          border-color: #667eea;
          color: #667eea;
          background: rgba(102, 126, 234, 0.05);
        }

        .module-checkbox.checked {
          background: #48bb78;
          border-color: #48bb78;
          color: white;
        }

        .module-checkbox.checked:hover {
          background: #38a169;
          border-color: #38a169;
        }

        .dark .module-checkbox {
          border-color: #4a5568;
          color: #a0aec0;
        }

        .dark .module-checkbox:hover {
          border-color: #667eea;
          color: #667eea;
          background: rgba(102, 126, 234, 0.1);
        }

        .route-footer {
          margin-top: 12px;
          padding-top: 12px;
          border-top: 1px solid #e2e8f0;
          font-size: 11px;
          color: #718096;
          text-align: center;
        }

        .dark .route-footer {
          border-top-color: #4a5568;
          color: #a0aec0;
        }

        .progress-message {
          color: #718096;
        }

        .dark .progress-message {
          color: #a0aec0;
        }

        .completion-message {
          font-size: 13px;
          font-weight: 600;
          color: #48bb78;
          text-transform: uppercase;
          letter-spacing: 0.5px;
          animation: completionPulse 0.6s ease-out;
        }

        .dark .completion-message {
          color: #68d391;
        }

        @keyframes completionPulse {
          0% {
            opacity: 0;
            transform: scale(0.8);
          }
          50% {
            transform: scale(1.1);
          }
          100% {
            opacity: 1;
            transform: scale(1);
          }
        }
      `}</style>

      <div className="route-header">
        <span className="route-title">📚 {routeName}</span>
        <span className="progress-badge">{completedCount}/{modules.length}</span>
      </div>

      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progressPercent}%` }} />
      </div>

      <div className="modules-list">
        {modules.map((module, idx) => (
          <div
            key={idx}
            className={`module-item ${idx === activeIndex ? 'active' : ''}`}
          >
            <a href={module.path} className="module-link">
              <div className={`module-status ${idx === activeIndex ? 'active' : isModuleCompleted(idx) ? 'done' : 'pending'}`}>
                {idx === activeIndex ? '▶' : isModuleCompleted(idx) ? '✓' : idx + 1}
              </div>
              <div className="module-title">{module.title}</div>
            </a>
            <button
              className={`module-checkbox ${isModuleCompleted(idx) ? 'checked' : ''}`}
              onClick={(e) => {
                e.preventDefault()
                toggleModule(idx)
              }}
              title={isModuleCompleted(idx) ? 'Marcar como incompleto' : 'Marcar como completado'}
              aria-label={`Marcar módulo ${idx + 1} como ${isModuleCompleted(idx) ? 'incompleto' : 'completado'}`}
            >
              {isModuleCompleted(idx) ? '✓' : '○'}
            </button>
          </div>
        ))}
      </div>

      <div className="route-footer">
        {isCompleted ? (
          <div className="completion-message">
            🎉 ¡Felicidades! Completaste {routeName} 🎊
          </div>
        ) : (
          <div className="progress-message">
            Progreso: {progressPercent}% completado
          </div>
        )}
      </div>
    </div>
  )
}
