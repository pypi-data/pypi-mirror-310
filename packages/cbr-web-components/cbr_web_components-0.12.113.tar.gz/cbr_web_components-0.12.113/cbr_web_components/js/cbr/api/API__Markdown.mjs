import API__Invoke from '../../data/API__Invoke.mjs'
import {CBR__Paths} from "../CBR__Paths.mjs";

export default class API__Markdown {

    constructor() {
        this.api_invoke = new API__Invoke()
    }

    // API endpoints
    static url__markdown_render = '/markdown/render/markdown-file-to-html-and-metadata'

    async get_markdown_content(content_path) {
        try {
            const response = await this.api_invoke.invoke_api(`${CBR__Paths.API__MARKDOWN_RENDER}?path=${content_path}`, 'GET')
            return {
                html     : response?.html       ,    // Rendered HTML content
                metadata : response?.metadata   ,    // Metadata from markdown
                success  : true                      // API call status         // todo: add better support error detection which in some cases is provided inside the metadata
            }
        } catch (error) {
            //console.error('Error loading markdown content:', error)
            return {
                html     : '<p>Error loading content</p>'              ,    // Fallback content
                metadata : { title: 'Error'              }             ,    // Fallback metadata
                success  : false                                           // Error status
            }
        }
    }
}