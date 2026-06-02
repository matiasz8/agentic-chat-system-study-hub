import Link from 'next/link';

interface RouteNavProps {
  current: number;
  total: number;
  route: 'rapida' | 'completa';
  nextLink?: string;
  prevLink?: string;
  moduleName: string;
}

export default function RouteNav({
  current,
  total,
  route,
  nextLink,
  prevLink,
  moduleName,
}: RouteNavProps) {
  return (
    <div className="mt-12 border-t pt-8">
      <div className="flex items-center justify-between mb-4">
        <span className="text-sm text-gray-500">
          Módulo {current} de {total}
        </span>
        <div className="w-full mx-4 bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all"
            style={{ width: `${(current / total) * 100}%` }}
          />
        </div>
      </div>

      <div className="flex justify-between gap-4">
        {prevLink ? (
          <Link
            href={prevLink}
            className="px-6 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg font-medium transition-colors"
          >
            ← Anterior
          </Link>
        ) : (
          <div />
        )}

        <div className="text-center text-sm text-gray-600">
          Ruta {route === 'rapida' ? 'Rápida (7 días)' : 'Completa (21 días)'}
        </div>

        {nextLink ? (
          <Link
            href={nextLink}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
          >
            Siguiente →
          </Link>
        ) : (
          <div className="px-6 py-2 bg-green-600 text-white rounded-lg font-medium">
            ✅ Completado
          </div>
        )}
      </div>
    </div>
  );
}
