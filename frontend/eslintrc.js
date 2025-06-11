module.exports = {
extends: [
'eslint:recommended',
'plugin:@typescript-eslint/recommended',
'plugin:svelte/recommended'
],
parser: '@typescript-eslint/parser',
plugins: ['@typescript-eslint'],
root: true,
env: {
browser: true,
node: true
}
};
