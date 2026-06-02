#!/usr/bin/env node

/**
 * Validate all internal routes in MDX files
 * Ensures all hrefs point to existing pages
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Recursively get all mdx files
function getAllMdxFiles(dir) {
  let files = [];
  const items = fs.readdirSync(dir);
  
  for (const item of items) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      files = files.concat(getAllMdxFiles(fullPath));
    } else if (item.endsWith('.mdx')) {
      files.push(fullPath);
    }
  }
  
  return files;
}

// Get all pages
const pagesDir = path.join(__dirname, '../pages');
const allPages = new Set();

// Collect all valid routes
const mdxFiles = getAllMdxFiles(pagesDir);
mdxFiles.forEach(file => {
  const relative = path.relative(pagesDir, file);
  let route = '/' + relative
    .replace(/\.mdx$/, '')
    .replace(/\/index$/, '')
    .replace(/\\/g, '/');
  
  allPages.add(route);
  // Also add with slash at end (Nextra handles both)
  if (!route.endsWith('/')) {
    allPages.add(route + '/');
  }
});

console.log(`✓ Found ${allPages.size} valid routes`);

// Find all href links
const errors = [];

for (const file of mdxFiles) {
  const content = fs.readFileSync(file, 'utf8');
  const relativePath = path.relative(pagesDir, file);
  
  // Find all href="/..." patterns
  const hrefRegex = /href=["']([^"']+)["']/g;
  let match;
  
  while ((match = hrefRegex.exec(content)) !== null) {
    const href = match[1];
    
    // Skip external links
    if (href.startsWith('http') || href.startsWith('mailto:') || href.startsWith('#')) {
      continue;
    }
    
    // Normalize path
    let cleanPath = href.split('?')[0].split('#')[0]; // Remove query and hash
    if (!cleanPath.endsWith('/')) {
      cleanPath += '/';
    }
    
    // Check if route exists
    if (!allPages.has(cleanPath) && !allPages.has(cleanPath.slice(0, -1))) {
      errors.push(`❌ ${relativePath}: href="${href}" → route not found`);
    }
  }
}

if (errors.length > 0) {
  console.error('\n' + errors.join('\n'));
  console.error(`\n❌ Found ${errors.length} broken routes`);
  process.exit(1);
} else {
  console.log('✅ All routes valid!');
  process.exit(0);
}
