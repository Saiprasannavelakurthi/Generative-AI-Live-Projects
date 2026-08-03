/**
 * babelLoader
 * -----------
 * Loads Babel Standalone and compiles JSX into a React Component.
 */

const BABEL_SRC =
  "https://unpkg.com/@babel/standalone@7.24.7/babel.min.js";

let babelLoadPromise = null;

export function loadBabel() {
  if (typeof window !== "undefined" && window.Babel) {
    return Promise.resolve(window.Babel);
  }

  if (babelLoadPromise) {
    return babelLoadPromise;
  }

  babelLoadPromise = new Promise((resolve, reject) => {
    const script = document.createElement("script");

    script.src = BABEL_SRC;
    script.async = true;

    script.onload = () => resolve(window.Babel);

    script.onerror = () =>
      reject(new Error("Failed to load Babel Standalone"));

    document.head.appendChild(script);
  });

  return babelLoadPromise;
}

/**
 * Defensive cleanup: LLM-generated code sometimes arrives wrapped in
 * markdown fences or containing import/export statements even when the
 * backend is supposed to strip them. `new Function(...)` is not a module
 * context, so `import`/`export` there is a SyntaxError, and stray
 * backticks silently swallow the real code into unused template
 * literals (which is what produced the `"" is not a function` error).
 * This makes the frontend robust even if the backend ever regresses.
 */
function sanitizeSource(sourceCode) {
  if (!sourceCode) return sourceCode;

  let code = sourceCode.trim();

  // Strip ```jsx / ```javascript / ``` fences
  code = code.replace(/^```[a-zA-Z]*\s*\n?/, "");
  code = code.replace(/\n?```\s*$/, "");
  code = code.trim();

  // Drop import statements (React & hooks come from scope)
  code = code.replace(/^\s*import\s+.*?;?\s*$/gm, "");

  // Strip `export default` / `export` but keep the declaration itself
  code = code.replace(/^\s*export\s+default\s+/gm, "");
  code = code.replace(/^\s*export\s+/gm, "");

  return code.trim();
}

export function compileComponent(sourceCode, Babel, scope = {}) {
  const cleaned = sanitizeSource(sourceCode);

  console.log("========== RAW JSX ==========");
  console.log(cleaned);

  const transformed = Babel.transform(cleaned, {
    presets: ["react"],
    filename: "dynamic-component.jsx",
  }).code;

  console.log("========== TRANSFORMED ==========");
  console.log(transformed);

  const scopeKeys = Object.keys(scope);
  const scopeValues = Object.values(scope);

  const wrappedCode = `
${transformed}

if (typeof Component === "undefined") {
    throw new Error("Component was not created after Babel transform.");
}

return Component;
`;

  try {
    const factory = new Function(
      ...scopeKeys,
      wrappedCode
    );

    return factory(...scopeValues);
  } catch (err) {
    console.error("========== COMPILE ERROR ==========");
    console.error(err);
    throw err;
  }
}