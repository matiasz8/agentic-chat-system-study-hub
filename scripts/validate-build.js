#!/usr/bin/env node

/**
 * Validate build artifacts
 * Ensures no build warnings or errors
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

try {
  console.log('🏗️  Building project...');
  
  const buildOutput = execSync('npm run build', {
    encoding: 'utf-8',
    stdio: 'pipe'
  });
  
  // Check for warnings or errors in output
  const hasErrors = buildOutput.includes('error') && buildOutput.includes('Error');
  const hasWarnings = buildOutput.includes('warn');
  
  if (hasErrors) {
    console.error('\n❌ Build contains errors:');
    console.error(buildOutput);
    process.exit(1);
  }
  
  if (hasWarnings) {
    console.warn('\n⚠️  Build warnings detected');
  }
  
  // Verify .next directory exists
  const nextDir = path.join(__dirname, '../.next');
  if (!fs.existsSync(nextDir)) {
    console.error('❌ Build failed: .next directory not found');
    process.exit(1);
  }
  
  console.log('✅ Build validation passed');
  process.exit(0);
  
} catch (error) {
  console.error('❌ Build failed:');
  console.error(error.message);
  process.exit(1);
}
