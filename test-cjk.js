import { Marked } from 'marked';
import katexExtension from './katex-extension.js';
import legacyKatexExtension from './legacy-katex-extension.js';
import katex from 'katex';

import fs from 'fs';
import path from 'path';
const testCasesFilePath = path.join(process.cwd(), 'test-cases-cjk.json');
const testCases = JSON.parse(fs.readFileSync(testCasesFilePath, 'utf8'));

function getKatexTokens(markdown, extensionsFactory) {
    const marked = new Marked()
    marked.use(extensionsFactory());
    const tokens = marked.lexer(markdown)

    const katexTokens = []

    function traverseTokenTree(token) {
        if (token.type === 'inlineKatex' || token.type === 'blockKatex') {
            katexTokens.push(token)
        }

        if (token.tokens) {
            token.tokens.forEach(traverseTokenTree)
        }
    }
    tokens.forEach(traverseTokenTree)

    return katexTokens
}

function renderKatexTokens(tokens) {
    for (let i = 0; i < tokens.length; i++) {
        const token = tokens[i];
        try {
            if (token.type === 'inlineKatex') {
                katex.renderToString(token.text, { displayMode: false });
            } else if (token.type === 'blockKatex') {
                katex.renderToString(token.text, { displayMode: true });
            }
        } catch (error) {
            console.error('Error rendering KaTeX tokens:');
            console.error('  Raw:', token.raw);
            console.error('  Error:', error);
            return false;
        }
    }
    return true;
}

let legacyPass = true;
let pass = true;

testCases.forEach((markdown) => {
    const tokens = getKatexTokens(markdown, katexExtension)
    const legacyTokens = getKatexTokens(markdown, legacyKatexExtension)

    legacyPass &&= renderKatexTokens(legacyTokens);
    pass &&= renderKatexTokens(tokens);
})

if (legacyPass) {
    console.log('\n🎉 All legacy cjk tokens rendered successfully.');
} else {
    console.error('\n❌ Some legacy cjk tokens failed to render.');
}

if (pass) {
    console.log('\n🎉 All new cjk tokens rendered successfully.');
} else { 
    console.error('\n❌ Some new cjk tokens failed to render.');
}