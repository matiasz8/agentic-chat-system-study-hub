import React from 'react';

interface TableRow {
  [key: string]: string | React.ReactNode;
}

interface ModuleTableProps {
  columns: string[];
  rows: TableRow[];
  title?: string;
  description?: string;
}

export const ModuleTable: React.FC<ModuleTableProps> = ({ 
  columns, 
  rows, 
  title, 
  description 
}) => {
  return (
    <div className="module-table-wrapper my-6">
      {title && <h3 className="mb-2">{title}</h3>}
      {description && <p className="text-sm text-gray-600 mb-4">{description}</p>}
      
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-blue-50 dark:bg-blue-900/20">
              {columns.map((col) => (
                <th 
                  key={col}
                  className="px-4 py-3 text-left font-semibold text-sm border border-gray-200 dark:border-gray-700"
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, idx) => (
              <tr 
                key={idx}
                className={`${
                  idx % 2 === 0 
                    ? 'bg-white dark:bg-slate-900' 
                    : 'bg-gray-50 dark:bg-slate-800/50'
                } hover:bg-blue-50/50 dark:hover:bg-blue-900/10 transition-colors`}
              >
                {columns.map((col) => (
                  <td 
                    key={`${idx}-${col}`}
                    className="px-4 py-3 text-sm border border-gray-200 dark:border-gray-700"
                  >
                    {row[col]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ModuleTable;
