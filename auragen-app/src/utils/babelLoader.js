/**
 * babelLoader
 * -----------
 * Lazy-loads Babel standalone from a CDN and compiles a raw source string
 * into a component function. Pure logic, no React/JSX here so it can be
 * unit-tested or swapped out independently of the rendering shell.
 *
 * Contract: the source must assign the root component to a top-level
 * identifier named `Component`, e.g.
 *   const Component = () => <div>hello</div>;
 */

const BABEL_SRC = 'https://unpkg.com/@babel/standalone@7.24.7/babel.min.js';

let babelLoadPromise = null;

export function loadBabel() {
  if (typeof window !== 'undefined' && window.Babel) return Promise.resolve(window.Babel);
  if (babelLoadPromise) return babelLoadPromise;

  babelLoadPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = BABEL_SRC;
    script.async = true;
    script.onload = () => resolve(window.Babel);
    script.onerror = () => reject(new Error('Failed to load Babel standalone from CDN'));
    document.head.appendChild(script);
  });

  return babelLoadPromise;
}

/**
 * SECURITY NOTE: this evaluates arbitrary JS with `new Function`, the
 * same trust model as any in-browser code playground. Only compile code
 * you control or trust; for user-submitted code, run this inside a
 * sandboxed <iframe> instead of the host page.
 */
export function compileComponent(sourceCode, Babel, scope = {}) {
<<<<<<< Updated upstream
  const transformed = Babel.transform(sourceCode, {
    presets: ['react', 'env'],
    filename: 'dynamic-component.jsx',
=======
  console.log("========== RAW JSX ==========");
  console.log(sourceCode);

  // Defense-in-depth: strip stray markdown code fences in case any
  // slipped through backend sanitization (e.g. ```jsx ... ```).
  const cleanedSource = sourceCode
    .replace(/^```[a-zA-Z]*\s*\n?/, "")
    .replace(/\n?```\s*$/, "")
    .trim();

  const transformed = Babel.transform(cleanedSource, {
    presets: ["react"],
    filename: "dynamic-component.jsx",
>>>>>>> Stashed changes
  }).code;

  const scopeKeys = Object.keys(scope);
  const scopeValues = scopeKeys.map((k) => scope[k]);

  // eslint-disable-next-line no-new-func
  const factory = new Function(
    ...scopeKeys,
    `${transformed}\n;return typeof Component !== 'undefined' ? Component : undefined;`
  );

  const CompiledComponent = factory(...scopeValues);
  if (!CompiledComponent) {
    throw new Error(
      'Compiled code did not define a `Component` identifier. Assign your root component to `Component`.'
    );
  }
  return CompiledComponent;
}
