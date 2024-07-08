const yaml = require('js-yaml');
const fs = require('fs');

function loadYaml(filePath) {
    const fileContent = fs.readFileSync(filePath, 'utf8');
    return yaml.load(fileContent);
}

function findCircularRefs(schema, path = [], visited = new Set()) {
    if (schema && schema['$ref']) {
        // && visited.has(schema)
        console.log(`Circular reference detected at: ${path.join(' -> ')}`);
        return;
    }
    // console.log(schema);
    visited.add(schema);

    if (typeof schema === 'object' && schema !== null) {
        for (const key in schema) {
            findCircularRefs(schema[key], [...path, key], visited);
        }
    } else if (Array.isArray(schema)) {
        schema.forEach((item, idx) => {
            findCircularRefs(item, [...path, idx.toString()], visited);
        });
    }
}

// step 1
var hasRef = false;
function findNoRefs(schema, path = [], visited = new Set(), cnt = 0) {
    if (schema && schema['$ref']) {
        hasRef = true;
        return;
    }
    visited.add(schema);

    if (typeof schema === 'object' && schema !== null) {
        for (const key in schema) {
            if (hasRef) break;
            findNoRefs(schema[key], [...path, key], visited);
        }
    } else if (Array.isArray(schema)) {
        schema.forEach((item, idx) => {
            if (hasRef) return;
            findNoRefs(item, [...path, idx.toString()], visited);
        });
    }
}

// Load your YAML schema
const schema = loadYaml('source.yaml');

// Check for circular references
// findCircularRefs(schema);

components = schema['components'];
schemas = components['schemas'];
console.log(Object.keys(schemas).length);

var cntNoRef = 0;

var noRefs = new Set();

for (const key in schemas) {
    hasRef = false;
    findNoRefs(schemas[key]);
    if (hasRef) {
        schemas[key]['hasRef'] = true;
    } else {
        console.log(`1- Reference not detected at: ${key}`);
        schemas[key]['hasRef'] = false;
        noRefs.add(key);
        cntNoRef++;
    }
}

console.log(cntNoRef);

var noCircular = true;
var cntCircular = 0;
function findNoRefs2(isConsole, schema, path = [], visited = new Set(), cnt = 0) {
    if (schema && schema['$ref']) {
        let ref = schema['$ref'];
        let refSplit = ref.split('/');
        if (noRefs.has(refSplit[refSplit.length - 1])) {

        } else {
            noCircular = false;
            cntCircular++;
            // if (isConsole) 
            console.log(`0- Circular reference detected at: ${path.join(' -> ')} - ${refSplit[refSplit.length - 1]}`);
        }
        return;
    }
    // console.log(schema);
    visited.add(schema);

    if (typeof schema === 'object' && schema !== null) {
        for (const key in schema) {
            findNoRefs2(isConsole, schema[key], [...path, key], visited);
        }
    } else if (Array.isArray(schema)) {
        schema.forEach((item, idx) => {
            findNoRefs2(isConsole, item, [...path, idx.toString()], visited);
        });
    }
}

// step 2

var currentCnt = 0;

do {
    currentCnt = 0;
    cntCircular = 0;
    for (const key in schemas) {
        noCircular = true;
        if (schemas[key]['hasRef']) {
            findNoRefs2(false, schemas[key], [key]);
            if (noCircular) {
                console.log(`2- Reference with terminal at: ${key}`);
                cntNoRef++;
                currentCnt++;
                noRefs.add(key);
                schemas[key]['hasRef'] = false;
            }
        }
    }
    if (currentCnt !== 0) {
        console.log(`No ref count: ${cntNoRef}`);
        console.log(`Circular count: ${cntCircular}`);
    }
} while (currentCnt > 0);


// // step 3
// cntCircular = 0;
// for (const key in schemas) {
//     noCircular = true;
//     if (schemas[key]['hasRef']) {
//         findNoRefs2(true, schemas[key], [key]);
//         if (noCircular) {
//             console.log(`3- Reference with terminal at: ${key}`);
//             cntNoRef++;
//             noRefs.add(key);
//             schemas[key]['hasRef'] = false;
//         }
//     }
// }

// console.log(`No ref count: ${cntNoRef}`);
// console.log(`Circular count: ${cntCircular}`);






// step 4

for (const key in schemas) {
    noCircular = true;
    if (schemas[key]['hasRef']) {
        console.log(key);
    }
}