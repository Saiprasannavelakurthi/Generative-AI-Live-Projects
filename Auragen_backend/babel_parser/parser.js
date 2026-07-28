const parser = require("@babel/parser");

let code = "";

process.stdin.setEncoding("utf8");

process.stdin.on("data", (chunk) => {
    code += chunk;
});

process.stdin.on("end", () => {

    try {

        if (!code.trim()) {
            console.log(JSON.stringify({
                valid: false,
                message: "Empty code received."
            }));

            return;
        }

        parser.parse(code, {
            sourceType: "module",
            plugins: [
                "jsx"
            ]
        });

        console.log(JSON.stringify({
            valid: true,
            message: "Valid JSX syntax."
        }));

    } catch (error) {

        console.log(JSON.stringify({
            valid: false,
            message: error.message
        }));
    }
});