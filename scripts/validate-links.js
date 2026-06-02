import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pagesDir = path.join(__dirname, '../pages');

// Collect all valid routes
const routes = new Set();
const mdxFiles = [];

function getAllMdxFiles(dir) {
  const files = fs.readdirSync(dir);
  files.forEach(file => {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      getAllMdxFiles(fullPath);
    } else if (file.endsWith('.mdx')) {
      mdxFiles.push(fullPath);
      const relativePath = path.relative(pagesDir, fullPath);
      let route = '/' + relativePath.replace(/\\/g, '/').replace('.mdx', '').replace('/index', '');
      routes.add(route);
    }
  });
}

getAllMdxFiles(pagesDir);

// Extract all links from MDX files
const linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
const brokenLinks = [];

mdxFiles.forEach(file => {
  const content = fs.readFileSync(file, 'utf-8');
  const relativePath = path.relative(pagesDir, file);
  
  let match;
  let lineNum = 1;
  const lines = content.split('\n');
  
  lines.forEach((line, idx) => {
    let linkMatch;
    while ((linkMatch = linkRegex.exec(line)) !== null) {
      const href = linkMatch[2];
      
      // Skip external links
      if (href.startsWith('http://') || href.startsWith('https://')) {
        return;
      }
      
      // Skip anchors to same page
      if (href.startsWith('#')) {
        return;
      }
      
      // Extract route (without anchor)
      const [route] = href.split('#');
      
      // Normalize route
      const normalized = route.endsWith('/') ? route.slice(0, -1) : route;
      
      if (!routes.has(normalized) && normalized !== '') {
        brokenLinks.push({
          file: relativePath,
          line: idx + 1,
          href: href,
          route: normalized
        });
      }
    }
  });
  
  linkRegex.lastIndex = 0;
});

if (brokenLinks.length > 0) {
  console.error('\n❌ BROKEN LINKS DETECTED:\n');
  brokenLinks.forEach(link => {
    console.error(`  ${link.file}:${link.line}`);
    console.error(`    Link: ${link.href}`);
    console.error(`    Route not found: ${link.route}`);
    console.error('');
  });
  process.exit(1);
} else {
  console.log('✓ All links validated');
  console.log(`✅ ${mdxFiles.length} files checked, ${routes.size} routes available`);
}
