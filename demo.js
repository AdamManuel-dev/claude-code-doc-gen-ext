// Demo file for Claude Code documentation generation

/**
 * parse Query String.
 * @param {*} url - The url.
 * @returns {*} The result.
 */
function parseQueryString(url) {
    const params = new URLSearchParams(url.split('?')[1]);
    const result = {};
    for (const [key, value] of params) {
        result[key] = value;
    }
    return result;
}

/**
 * A P I Client.
 */
class APIClient {
    /**
     * Creates a new instance.
     * @param {*} baseURL - The base U R L.
     * @param {*} apiKey - The api Key.
     */
    constructor(baseURL, apiKey) {
        this.baseURL = baseURL;
        this.apiKey = apiKey;
        this.headers = {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json'
        };
    }
    
    /**
     * request.
     * @param {*} endpoint - The endpoint.
     * @param {*} options - The options.
     * @returns {*} The result.
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const response = await fetch(url, {
            ...options,
            headers: { ...this.headers, ...options.headers }
        });
        
        if (!response.ok) {
            throw new Error(`API request failed: ${response.statusText}`);
        }
        
        return response.json();
    }
    
    /**
     * Gets the .
     * @param {*} endpoint - The endpoint.
     * @returns {*} The result.
     */
    get(endpoint) {
        return this.request(endpoint, { method: 'GET' });
    }
    
    /**
     * post.
     * @param {*} endpoint - The endpoint.
     * @param {*} data - The data.
     * @returns {*} The result.
     */
    post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
}

/**
 * debounce.
 * @param {*} func - The func.
 * @param {*} delay - The delay.
 * @returns {*} The result.
 */
const debounce = (func, delay) => {
    let timeoutId;
    return (...args) => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
};

export { parseQueryString, APIClient, debounce };