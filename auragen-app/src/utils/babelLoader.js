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

export function compileComponent(sourceCode, Babel, scope = {}) {
  console.log("========== RAW JSX ==========");
  console.log(sourceCode);

  const transformed = Babel.transform(sourceCode, {
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