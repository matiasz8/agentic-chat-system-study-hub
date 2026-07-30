'use client';

import dynamic from 'next/dynamic';
import { CopyIcon, CheckIcon } from 'lucide-react';
import { useState, Suspense } from 'react';

interface CodeBlockProps {
  code: string;
  language?: string;
  title?: string;
  showLineNumbers?: boolean;
  highlight?: number[];
}

// Fallback component while SyntaxHighlighter is loading
function CodeFallback({ code }: { code: string }) {
  return (
    <pre className="bg-gray-900 text-gray-100 p-4 rounded overflow-x-auto text-sm">
      <code>{code}</code>
    </pre>
  );
}

// Dynamic import of SyntaxHighlighter - lazy loads on demand
const SyntaxHighlighter = dynamic(
  () => import('react-syntax-highlighter').then((mod) => mod.default),
  {
    loading: () => <div className="bg-gray-900 p-4 rounded text-gray-400 text-sm">Cargando sintaxis...</div>,
    ssr: false,
  }
);

export function CodeBlockOptimized({
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
        <div className="bg-gray-100 dark:bg-gray-800 px-4 py-2 text-sm font-semibold text-gray-700 dark:text-gray-200">
          {title}
        </div>
      )}

      <div className="relative bg-gray-900">
        <button
          onClick={copyToClipboard}
          className="absolute top-2 right-2 p-2 rounded hover:bg-gray-700 transition-colors z-10"
          aria-label="Copy code"
        >
          {copied ? (
            <CheckIcon className="w-4 h-4 text-green-400" />
          ) : (
            <CopyIcon className="w-4 h-4 text-gray-400" />
          )}
        </button>

        <Suspense fallback={<CodeFallback code={code} />}>
          <SyntaxHighlighter
            language={language}
            showLineNumbers={showLineNumbers}
            wrapLines
            lineProps={(lineNumber: number) =>
              highlight.includes(lineNumber)
                ? { style: { backgroundColor: 'rgba(255, 255, 0, 0.1)' } }
                : {}
            }
          >
            {code}
          </SyntaxHighlighter>
        </Suspense>
      </div>
    </div>
  );
}
