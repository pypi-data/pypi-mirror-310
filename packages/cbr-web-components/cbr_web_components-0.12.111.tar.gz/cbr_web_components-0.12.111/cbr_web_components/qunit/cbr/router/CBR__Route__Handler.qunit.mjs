import CBR__Content__Loader from '../../../js/cbr/router/CBR__Content__Loader.mjs'
import CBR__Route__Handler from '../../../js/cbr/router/CBR__Route__Handler.mjs'
import CBR__Route__Content from '../../../js/cbr/router/CBR__Route__Content.mjs'
import Raw_Html           from '../../../js/core/Raw_Html.mjs'
import { Mock_Fetch,
         set_mock_response } from '../api/Mock_Fetch.mjs'

const { module, test, only } = QUnit

const MOCK_CONTENT = {
    html    : '<div>Test Content</div>'    ,
    metadata: {
        title   : 'Test Page'              ,
        subtitle: 'Test Description'
    }
}

module('CBR__Route__Handler', hooks => {
    let handler
    let mock_component
    let content_div
    let route_content

    hooks.beforeEach(() => {
        //Mock_Fetch.apply_mock(CBR__Route__Content)                                // Apply mock to Route Content
        Mock_Fetch.apply_mock(CBR__Content__Loader)

        // Setup mock responses for common paths
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/test-page.md'     , MOCK_CONTENT)
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/home/index.md'    , MOCK_CONTENT)
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/test/path.md'     , MOCK_CONTENT)

        // Setup DOM elements
        content_div = document.createElement('div')
        content_div.id = 'content'
        document.body.appendChild(content_div)

        // Setup mock component
        route_content = new CBR__Route__Content()
        mock_component = {
            query_selector: (selector) => document.querySelector(selector),
            routeContent  : route_content
        }

        handler = new CBR__Route__Handler(mock_component)
    })

    hooks.afterEach(() => {
        content_div.remove()
        window.history.pushState({}, '', '/')                                      // Reset URL
    })

    test('constructor initializes with correct defaults', assert => {
        // Assert
        assert.equal(handler.base_path    , '/'           , 'Sets default base_path'    )
        assert.equal(handler.default_page , 'home/index'  , 'Sets default page'         )
        assert.equal(handler.component    , mock_component , 'Sets component reference'  )
    })

    test ('handle_route processes path correctly', async assert => {
        // Arrange
        const test_path = 'test-page'

        // Act
        await handler.handle_route(test_path)

        // Assert
        assert.ok(1)

        assert.ok(content_div.innerHTML.includes(MOCK_CONTENT.html)               , 'Renders correct content'          )
        assert.ok(content_div.firstChild.classList.contains('nav-content')        , 'Adds nav-content class'          )
        assert.ok(content_div.firstChild.classList.contains('nav-test-page')      , 'Adds navigation class'           )
    })

    test('handle_route handles empty path', async assert => {
        // Act
        await handler.handle_route('/')

        // Assert
        assert.ok(content_div.innerHTML.includes(MOCK_CONTENT.html), 'Renders default page content')
    })

    test('handle_route handles fetch errors gracefully', async assert => {
        // Arrange
        const error_path = 'error-page'
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/error-page.md', null, 404)
        const expected_error = `\
<div class="nav-content nav-error-page">
    ... failed to load content ...
</div>
`

        // Act
        await handler.handle_route(error_path)

        // Assert
        assert.deepEqual(content_div.innerHTML,expected_error)
    })

    test('should_handle_link validates links correctly', assert => {
        // Arrange
        handler.base_path = '/en/site/'
        const base_url = window.location.origin + handler.base_path
        const test_cases = [{ href: `${base_url}test`        , expected: true  , desc: 'Valid internal link' },
                            { href: 'https://external.com'   , expected: false , desc: 'External link'       },
                            { href: 'javascript:void(0)'     , expected: false , desc: 'JavaScript link'     },
                            { href: `${base_url}`            , expected: true  , desc: 'Root path'           },
                            { href: '/relative/path'         , expected: false , desc: 'Relative path'       }]

        // Act & Assert
        test_cases.forEach(test_case => {
            const link = document.createElement('a')
            link.href = test_case.href
            assert.equal(handler.should_handle_link(link), test_case.expected, test_case.desc)
        })
    })

    test('handle_navigation_click processes internal links', async assert => {
        // Arrange
        const link = document.createElement('a')
        link.href  = window.location.origin + '/test-page'
        document.body.appendChild(link)

        // Create click event with path
        const click_event = new MouseEvent('click', {
            bubbles   : true              ,
            cancelable: true              ,
            composed  : true
        })

        // Mock composedPath to return path with link
        click_event.composedPath = () => [link, document.body, document]

        // Act
        await handler.handle_navigation_click(click_event)

        // Assert
        assert.ok(content_div.innerHTML.includes(MOCK_CONTENT.html), 'Navigation processed content')

        // Cleanup
        link.remove()
    })

    test('set_base_path updates path handling', async assert => {
        // Arrange
        const new_base = '/new-base/'
        handler.set_base_path(new_base)

        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/test-in-new-base.md',
                          MOCK_CONTENT)

        const link = document.createElement('a')
        link.href = window.location.origin + new_base + 'test-in-new-base'

        // Act
        await handler.process_link(link)

        // Assert
        assert.equal(handler.base_path, new_base                                  , 'Base path was updated'    )
        assert.ok(content_div.innerHTML.includes(MOCK_CONTENT.html)              , 'Content loads with new base path')
    })

    test('handle_route handles null content response', async assert => {
        // Arrange
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/null-page.md', null)
        const expected_error = `\
<div class="nav-content nav-null-page">
    ... failed to load content ...
</div>
`

        // Act
        await handler.handle_route('null-page')

        // Assert
        assert.deepEqual(content_div.innerHTML , expected_error)
    })

    test('handle_pop_state processes browser navigation', async assert => {
        // Arrange
        window.history.pushState({}, '', '/test/path')
        set_mock_response('/markdown/render/markdown-file-to-html-and-metadata?path=en/site/test/path.md',
                          MOCK_CONTENT)

        // Act
        await handler.handle_pop_state(new PopStateEvent('popstate'))

        // Assert
        assert.ok(content_div.innerHTML.includes(MOCK_CONTENT.html), 'Pop state loads correct content')
    })

    test('process_link handles web component loading', async assert => {
        // Arrange
        const link = document.createElement('a')
        const mock_module = { default: class TestComponent extends HTMLElement {
            static define() { customElements.define('webc-test-component', this) }
        }}

        link.href = window.location.origin + '/test-component'
        link.setAttribute('data-target-type'   , 'web_component'          )
        link.setAttribute('data-component'     , 'WebC__Test__Component'  )
        link.setAttribute('data-component-path', 'test/components/'       )

        // Mock the import_module method
        handler.import_module = async (path) => {
            assert.equal(path,
                        '/web_components/js/cbr/web-components/test/components/WebC__Test__Component.mjs',
                        'Loads correct module path')
            return mock_module
        }

        // Act
        await handler.process_link(link)

        // Assert
        const component = content_div.querySelector('webc-test-component')
        assert.ok(component, 'Component was created')
    })
})