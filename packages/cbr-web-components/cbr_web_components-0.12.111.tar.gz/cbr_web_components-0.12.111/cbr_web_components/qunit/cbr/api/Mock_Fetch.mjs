export class Mock_Fetch {
    constructor() {
        this.responses = new Map()
    }

    static apply_mock(target_class) {                                    // Much simpler now - just patch and go
        target_class.prototype.fetch_url = function(...args) {
            return mock.fetch_url.apply(mock, args)
        }
        return mock
    }

    static restore_original(target_class, original) {                    // Optional restore if needed
        if (original) {
            target_class.prototype.fetch_url = original
        }
    }

    async fetch_url(url) {
        if (this.responses.has(url)) {
            const response = this.responses.get(url)
            return {
                ok     : response.status === 200           ,
                status : response.status || 200            ,
                json   : async () => response.data
            }
        }
        throw new Error(`No mock response set for URL: ${url}`)
    }

    set_response(url, data, status = 200) {
        this.responses.set(url, { data, status })
    }
}

export const mock = new Mock_Fetch()                                    // Single instance for convenience

export function set_mock_response(url, data, status = 200) {           // Helper function
    mock.set_response(url, data, status)
}