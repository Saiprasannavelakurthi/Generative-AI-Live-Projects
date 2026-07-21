const parser = require("@babel/parser");

const code = process.argv[2];

try {

    parser.parse(code,{
        sourceType:"module",
        plugins:["jsx"]
    });

    console.log(JSON.stringify({
        valid:true
    }));

}
catch(error){

    console.log(JSON.stringify({

        valid:false,
        message:error.message

    }));

}