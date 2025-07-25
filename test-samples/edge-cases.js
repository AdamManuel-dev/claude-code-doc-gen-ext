// Edge case test file

// Empty function
function emptyFunction() {}

// Function with existing partial JSDoc
/**
 * This already has a description
 */
function partiallyDocumented(a, b) {
    return a + b;
}

// Nested functions
function outerFunction() {
    function innerFunction() {
        return "nested";
    }
    return innerFunction();
}

// Function with destructured parameters
function destructuredParams({name, age, city = "Unknown"}) {
    return `${name} is ${age} from ${city}`;
}

// Function with rest parameters
function restParams(first, ...rest) {
    return [first, ...rest];
}

// Empty class
class EmptyClass {}

// Method that looks like control flow
class Parser {
    if(condition) {
        // This is actually a method named 'if'
        return condition;
    }
}

// Arrow function with no parentheses
const singleParam = x => x * 2;

// IIFE
(function() {
    console.log("IIFE");
})();

// Object method shorthand
const obj = {
    method() {
        return "shorthand";
    }
};