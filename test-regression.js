import { Marked } from 'marked';
import katexExtension from './katex-extension.js';
import legacyKatexExtension from './legacy-katex-extension.js';

import fs from 'fs';
import path from 'path';
const testCasesFilePath = path.join(process.cwd(), 'test-cases.json');
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

let pass = true;

testCases.forEach((markdown) => {
    const tokens = getKatexTokens(markdown, katexExtension)
    const legacyTokens = getKatexTokens(markdown, legacyKatexExtension)

    // console.log('tokens', tokens)
    // console.log('legacyTokens', legacyTokens)

    if (tokens.length !== legacyTokens.length) {
        pass = false
        console.error('  MISMATCH: Token count differs!')
        console.error('    tokens:', tokens)
    } else {
        for (let i = 0; i < tokens.length; i++) {
            const token = tokens[i]
            const legacyToken = legacyTokens[i]

            if (token.type !== legacyToken.type ||
                token.raw !== legacyToken.raw ||
                token.text !== legacyToken.text ||
                token.displayMode !== legacyToken.displayMode) {
                pass = false
                console.error('  MISMATCH at index', i)
                console.error('    Expected:', token)
                console.error('    Actual:', legacyToken)
                break
            }
        }
    }
})

if (pass) {
    console.log('\n🎉 All regression tests passed!');
} else {
    console.error('\n❌ Some regression tests failed.');
}