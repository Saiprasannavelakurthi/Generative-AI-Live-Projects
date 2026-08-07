/**
 * babelLoader.js
 *
 * Loads Babel Standalone dynamically and
 * compiles AI-generated React components.
 */

const BABEL_SRC =
  "https://unpkg.com/@babel/standalone@7.24.7/babel.min.js";

let babelPromise = null;

/**
 * Load Babel Standalone only once.
 */
export async function loadBabel() {
  if (typeof window !== "undefined" && window.Babel) {
    return window.Babel;
  }

  if (babelPromise) {
    return babelPromise;
  }

  babelPromise = new Promise((resolve, reject) => {
    const existing = document.querySelector(
      `script[src="${BABEL_SRC}"]`
    );

    if (existing) {
      existing.addEventListener("load", () => {
        if (window.Babel) {
          resolve(window.Babel);
        } else {
          reject(
            new Error("Babel failed to initialize.")
          );
        }
      });

      existing.addEventListener("error", () => {
        reject(
          new Error("Unable to load Babel.")
        );
      });

      return;
    }

    const script = document.createElement("script");

    script.src = BABEL_SRC;
    script.async = true;

    script.onload = () => {
      if (window.Babel) {
        resolve(window.Babel);
      } else {
        reject(
          new Error("Babel failed to initialize.")
        );
      }
    };

    script.onerror = () => {
      reject(
        new Error(
          "Failed to load Babel Standalone."
        )
      );
    };

    document.head.appendChild(script);
  });

  return babelPromise;
}

/**
 * Clean AI-generated code before compilation.
 */
function sanitizeSource(source = "") {
  let code = source.trim();

  // Remove Markdown code fences
  code = code.replace(/^```[a-zA-Z]*\n?/gm, "");
  code = code.replace(/```$/gm, "");

  // Remove imports
  code = code.replace(
    /^\s*import\s.+$/gm,
    ""
  );

  // Remove exports
  code = code.replace(
    /^\s*export\s+default\s+/gm,
    ""
);

code = code.replace(
    /^\s*export\s*\{.*\};?$/gm,
    ""
);

  return code.trim();
}

/**
 * Compile JSX into a React Component.
 */
export function compileComponent(
  sourceCode,
  Babel,
  scope = {}
) {
  if (!sourceCode) {
    throw new Error(
      "No source code provided."
    );
  }

  if (!Babel) {
    throw new Error(
      "Babel is not loaded."
    );
  }

  const cleanedCode =
    sanitizeSource(sourceCode);

    console.log("========== SOURCE ==========");
    console.log(cleanedCode);

  const transformed =
    Babel.transform(cleanedCode, {
      presets: ["react"],
      filename: "Component.jsx",
    }).code;
    console.log("========== TRANSFORMED ==========");
    console.log(transformed.code);

  const scopeKeys =
    Object.keys(scope);

  const scopeValues =
    Object.values(scope);

  const wrappedCode = `
${transformed}

if (typeof Component === "undefined") {
    throw new Error(
        "Generated code does not define a Component."
    );
}

return Component;
`;

  try {
    const factory = new Function(
      ...scopeKeys,
      wrappedCode
    );
    const Component = factory(...scopeValues);

    console.log("Compiled Component:", Component);

    return Component;

    return factory(...scopeValues);
  } catch (error) {
    console.error(
      "React component compilation failed:"
    );
    console.error(error);

    throw error;
  }
}