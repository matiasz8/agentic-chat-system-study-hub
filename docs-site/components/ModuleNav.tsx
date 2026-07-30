import Link from 'next/link';
import { ChevronRight, ChevronLeft } from 'lucide-react';

interface ModuleNavItem {
  title: string;
  href: string;
  completed?: boolean;
  duration?: string;
  level?: 'básico' | 'intermedio' | 'avanzado';
}

interface ModuleNavProps {
  current: string;
  section: string;
  modules: ModuleNavItem[];
  showProgressBar?: boolean;
}

export function ModuleNav({
  current,
  section,
  modules,
  showProgressBar = true,
}: ModuleNavProps) {
  const currentIndex = modules.findIndex(
    (m) => m.href === current
  );
  const hasPrevious = currentIndex > 0;
  const hasNext = currentIndex < modules.length - 1;
  const previous = hasPrevious ? modules[currentIndex - 1] : null;
  const next = hasNext ? modules[currentIndex + 1] : null;
  const completed = modules.filter((m) => m.completed).length;
  const progress = Math.round((completed / modules.length) * 100);

  const getLevelColor = (level?: string) => {
    switch (level) {
      case 'básico':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'intermedio':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'avanzado':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200';
    }
  };

  return (
    <div className="my-8 space-y-6">
      {/* Progress bar */}
      {showProgressBar && (
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="font-semibold text-gray-700 dark:text-gray-300">
              Progreso de sección
            </span>
            <span className="text-gray-600 dark:text-gray-400">
              {completed}/{modules.length}
            </span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className="bg-blue-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {/* Navigation buttons */}
      <div className="grid grid-cols-2 gap-4">
        {/* Previous */}
        {previous ? (
          <Link
            href={previous.href}
            className="group flex items-start gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-gray-400 dark:hover:border-gray-600 transition-colors"
          >
            <ChevronLeft
              size={20}
              className="text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-400 flex-shrink-0 mt-0.5"
            />
            <div className="text-sm">
              <div className="text-gray-600 dark:text-gray-400">Anterior</div>
              <div className="font-semibold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400">
                {previous.title}
              </div>
              {previous.duration && (
                <div className="text-xs text-gray-500 mt-1">
                  ⏱️ {previous.duration}
                </div>
              )}
            </div>
          </Link>
        ) : (
          <div />
        )}

        {/* Next */}
        {next ? (
          <Link
            href={next.href}
            className="group flex items-start justify-end gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-gray-400 dark:hover:border-gray-600 transition-colors text-right"
          >
            <div className="text-sm">
              <div className="text-gray-600 dark:text-gray-400">Siguiente</div>
              <div className="font-semibold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400">
                {next.title}
              </div>
              {next.duration && (
                <div className="text-xs text-gray-500 mt-1">
                  ⏱️ {next.duration}
                </div>
              )}
            </div>
            <ChevronRight
              size={20}
              className="text-gray-400 group-hover:text-gray-600 dark:group-hover:text-gray-400 flex-shrink-0 mt-0.5"
            />
          </Link>
        ) : (
          <div />
        )}
      </div>

      {/* Module list sidebar */}
      <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
        <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
          📚 Módulos de {section}
        </h4>
        <div className="space-y-2">
          {modules.map((module) => (
            <Link
              key={module.href}
              href={module.href}
              className={`block p-2 rounded text-sm transition-colors ${
                module.href === current
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-900 dark:text-blue-100 font-semibold'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
              }`}
            >
              <div className="flex items-center justify-between">
                <span>{module.title}</span>
                {module.completed && (
                  <span className="text-green-600 dark:text-green-400">
                    ✓
                  </span>
                )}
              </div>
              {module.level && (
                <div className={`text-xs mt-1 inline-block px-2 py-0.5 rounded ${getLevelColor(module.level)}`}>
                  {module.level}
                </div>
              )}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
