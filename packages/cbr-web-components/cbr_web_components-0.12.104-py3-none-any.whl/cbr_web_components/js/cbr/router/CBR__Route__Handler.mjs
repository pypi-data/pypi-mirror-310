import Raw_Html from "../../core/Raw_Html.mjs";

export default class CBR__Route__Handler {

    base_path    = '/'
    default_page = 'home/index'

    constructor(component, base_path) {
        this.component = component
        this.add_event_listeners()
    }

    add_event_listeners() {
        window.addEventListener  ('popstate', this.handle_pop_state       .bind(this))        // Listen for popstate events (browser back/forward)
        document.addEventListener('click'   , this.handle_navigation_click.bind(this))        // Intercept navigation clicks
    }

    async handle_pop_state(event) {
        await this.handle_route(window.location.pathname)
    }

    async handle_navigation_click(event) {
        const path = event.composedPath();
        const link = path.find(el => el.tagName === 'A');

        if (link && link.href.startsWith(window.location.origin)) {
            if (link.href.includes('/web/') || link.href.includes('/athena/index#' )) {           // don't intercept links to other pages
                return
            }
            event.preventDefault()
            const path = link.href.replace(window.location.origin, '')
            await this.navigate(path)
        }
    }

    async handle_route(path) {
        const contentEl = this.component.query_selector('#content')
        if (!contentEl) return

        const placeholder = contentEl
        const routePath   = path.replace(this.base_path, '').replace(/^\/+/, '') || this.default_page      // Get the route path without the base path

        const pathSegments = routePath.split('/').filter(segment => segment)                        // Create navigation classes from the path segments
        const navClasses   = pathSegments.map((segment, index) => {
            const subPath  = pathSegments.slice(0, index + 1).join('-')                                     // Build cumulative path for each level
            return `nav-${subPath}`
        })

        const div_classes = `nav-content ${navClasses.join(' ')}`
        const wrapperDiv  = new Raw_Html({class: div_classes })                                              // Create wrapper div with all navigation classes


        try {
            const content         = await this.component.routeContent.fetch_content(routePath)
            wrapperDiv.raw_html   = content
            placeholder.innerHTML = wrapperDiv.html()
        } catch (error) {
            console.error('Error loading content:', error)
            wrapperDiv.value = '<div class="content-error">Error loading content. Please try again.</div>'          // todo: refactor to use Div
            placeholder.innerHTML = wrapperDiv.html()
        }
    }

    async navigate(path) {
        window.history.pushState({}, '', path)
        await this.handle_route(path)
    }

    set_base_path(base_path) {
        this.base_path = base_path
    }
}