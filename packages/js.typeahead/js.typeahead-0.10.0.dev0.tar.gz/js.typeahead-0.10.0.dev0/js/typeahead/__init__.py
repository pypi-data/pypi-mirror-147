from fanstatic import Library, Resource
from js.jquery import jquery

lib = Library("js.typeahead", "resources")
typeahead_css = Resource(
    lib,
    "css/typeahead.css",
    minified="css/typeahead.min.css",
)

typeahead_bootstrap_css = Resource(
    lib,
    "css/typeahead.js-bootstrap.css",
    depends=[typeahead_css],
)

typeahead_js = Resource(
    lib,
    "js/typeahead.js",
    minified="js/typeahead.min.js",
    depends=[jquery],
)
