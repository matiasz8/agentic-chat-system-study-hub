'use client';

import { CopyIcon, CheckIcon } from 'lucide-react';
import { useState, lazy, Suspense } from 'react';

interface CodeBlockProps {
  code: string;
  language?: string;
  title?: string;
  showLineNumbers?: boolean;
  highlight?: number[];
}

// Lazy load the syntax highlighter component
const SyntaxHighlighter = lazy(async () => {
  const [{ Prism }, { atomOneDark }] = await Promise.all([
    import('react-syntax-highlighter'),
    import('react-syntax-highlighter/dist/esm/styles/hljs'),
  ]);
  
  return {
    default: (props: any) => {
      return <Prism {...props} style={atomOneDark} />;
    },
  };
});

const CodeFallback = ({ code }: { code: string }) => (
  <pre className="bg-gray-900 text-gray-100 p-4 rounded overflow-x-auto text-sm">
    <code>{code}</code>
  </pre>
);

export function CodeBlock({
  code,
  language = 'python',
  title,
  showLineNumbers = true,
  highlight = [],
}: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="my-6 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
      {title && (
        <div className="bg-gray-100 dark:bg-gray-800 px-4 py-2 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">
            {title}
          </span>
          <button
            onClick={copyToClipboard}
            className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded transition-colors"
            title="Copy code"
          >
            {copied ? (
              <CheckIcon size={16} className="text-green-600" />
            ) : (
              <CopyIcon size={16} className="text-gray-600 dark:text-gray-400" />
            )}
          </button>
        </div>
      )}

      <div className="overflow-x-auto">
        <Suspense fallback={<CodeFallback code={code} />}>
          <SyntaxHighlighter
            language={language}
            showLineNumbers={showLineNumbers}
            wrapLines={true}
          >
            {code}
          </SyntaxHighlighter>
        </Suspense>
      </div>
    </div>
  );
}

export function BasicExample({ code, title }: { code: string; title?: string }) {
  return (
    <div className="my-8 p-4 bg-blue-50 dark:bg-blue-900 dark:bg-opacity-20 border-l-4 border-blue-500 rounded">
      <h4 className="font-bold text-blue-900 dark:text-blue-200 mb-3">
        ✅ Ejemplo: {title || 'Código básico'}
      </h4>
      <CodeBlock code={code} language="python" title={title} />
    </div>
  );
}

export function AdvancedExample({ code, title }: { code: string; title?: string }) {
  return (
    <div className="my-8 p-4 bg-purple-50 dark:bg-purple-900 dark:bg-opacity-20 border-l-4 border-purple-500 rounded">
      <h4 className="font-bold text-purple-900 dark:text-purple-200 mb-3">
        🚀 Ejemplo Avanzado: {title || 'Código production-ready'}
      </h4>
      <CodeBlock code={code} language="python" title={title} />
    </div>
  );
}

export function Exercise({
  title,
  problem,
  hints = [],
}: {
  title: string;
  problem: string;
  hints?: string[];
}) {
  const [showHints, setShowHints] = useState(false);

  return (
    <div className="my-8 p-4 bg-amber-50 dark:bg-amber-900 dark:bg-opacity-20 border-l-4 border-amber-500 rounded">
      <h4 className="font-bold text-amber-900 dark:text-amber-200 mb-3">
        ✏️ Ejercicio: {title}
      </h4>
      <div className="text-gray-700 dark:text-gray-300 mb-4">{problem}</div>
      
      {hints.length > 0 && (
        <>
          <button
            onClick={() => setShowHints(!showHints)}
            className="text-sm text-amber-600 dark:text-amber-400 hover:underline mb-2"
          >
            {showHints ? '▼ Ocultar pistas' : '▶ Ver pistas'}
          </button>
          
          {showHints && (
            <div className="mt-3 bg-white dark:bg-gray-800 p-3 rounded border border-amber-200 dark:border-amber-700">
              {hints.map((hint, idx) => (
                <div key={idx} className="mb-2 last:mb-0">
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    <span className="font-semibold">💡 Pista {idx + 1}:</span> {hint}
                  </p>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
