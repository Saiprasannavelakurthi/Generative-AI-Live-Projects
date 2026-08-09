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
 * Subsequent calls return the cached promise.
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
 * Removes Markdown fences, import, and export statements.
 */
function sanitizeSource(source = "") {
  let code = source.trim();

  // Remove Markdown code fences
  code = code.replace(/^```[a-zA-Z]*\n?/gm, "");
  code = code.replace(/```$/gm, "");

  // Remove import statements (not allowed in sandboxed components)
  code = code.replace(
    /^\s*import\s.+$/gm,
    ""
  );

  // Remove export default
  code = code.replace(
    /^\s*export\s+default\s+/gm,
    ""
  );

  // Remove named exports
  code = code.replace(
    /^\s*export\s*\{.*\};?$/gm,
    ""
  );

  // Fix spaced variable typos e.g. Form Data -> formData
  code = code.replace(/\bForm\s+Data\b/gi, "formData");

  // Transform unsafe form data .includes() calls into safe operations e.g. (formData['x'] || '').includes(...)
  code = code.replace(/(formData(?:\[[^\]]+\]|\.[a-zA-Z0-9_$]+))\.includes\(/gi, "($1 || '').includes(");
  code = code.replace(/(FormaData(?:\[[^\]]+\]|\.[a-zA-Z0-9_$]+))\.includes\(/gi, "($1 || '').includes(");

  // Transform chained .split() array access to optional chaining to prevent split of undefined
  code = code.replace(/\.split\(([^)]+)\)\[(\d+)\]\.split\(/g, "?.split($1)?.[$2]?.split(");
  code = code.replace(/\.split\(([^)]+)\)\[(\d+)\]/g, "?.split($1)?.[$2]");

  // Truncate repetitive infinite SVG path strings to prevent string unterminated errors
  code = code.replace(/d="([^"]{120,})"/g, 'd="M12 4v16m8-8H4"');

  // Remove incomplete formData bracket-key string expressions cut mid-way
  code = code.replace(/formData\['[^']*\.\.\.[^']*'\]/g, "\"\"");

  return code.trim();
}

/**
 * Compile JSX source code into a React Component function.
 *
 * Flow:
 *   AI JSX source
 *     → sanitizeSource()      strip markdown/imports/exports
 *     → Babel.transform()     JSX → plain JavaScript
 *     → new Function()        create factory with injected scope
 *     → factory(scopeValues)  execute and return Component
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

  // Transform JSX to plain JavaScript
  const transformed =
    Babel.transform(cleanedCode, {
      presets: ["react"],
      filename: "Component.jsx",
    }).code;

  const scopeKeys =
    Object.keys(scope);

  const scopeValues =
    Object.values(scope);

  // Wrap with a Component existence check then return it
  const wrappedCode = `
${transformed}

let TargetComponent = typeof Component !== "undefined" ? Component : null;

if (!TargetComponent) {
    const knownNames = [
        "LoginUI", "DashboardComponent", "FormComponent", "MyComponent", 
        "App", "Form", "Login", "Dashboard", "LoanForm", "ProfilePage", 
        "ContactForm", "RegisterForm", "UIComponent"
    ];
    for (const name of knownNames) {
        try {
            if (typeof eval(name) === "function") {
                TargetComponent = eval(name);
                break;
            }
        } catch (e) {}
    }
}

if (!TargetComponent || typeof TargetComponent !== "function") {
    throw new Error("Generated code did not define a valid Component function.");
}

return TargetComponent;
`;

  try {
    const factory = new Function(
      ...scopeKeys,
      wrappedCode
    );

    const Component = factory(...scopeValues);

    return Component;

  } catch (error) {
    console.error(
      "[AuraGen] React component compilation failed:",
      error
    );

    throw error;
  }
}