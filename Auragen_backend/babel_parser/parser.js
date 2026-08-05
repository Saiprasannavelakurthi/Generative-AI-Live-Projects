const parser = require("@babel/parser");

let code = "";

process.stdin.setEncoding("utf8");

process.stdin.on("data", (chunk) => {
    code += chunk;
});

process.stdin.on("end", () => {
    try {
        parser.parse(code, {
            sourceType: "module",
            plugins:[
                "jsx",
                "typescript"
            ]
        });

        console.log(
            JSON.stringify({
                valid: true,
                message: "Babel validation passed."
            })
        );

    } catch (error) {

        console.log(
            JSON.stringify({
                valid: false,
                message: error.message
            })
        );
    }
});