from fanstatic import Library, Resource
from js.jquery import jquery

lib = Library("js.typeahead", "resources")
typeahead_bundle_js = Resource(
    lib,
    "js/typeahead.bundle.js",
    minified="js/typeahead.bundle.min.js",
    depends=[jquery],
)

bloodhound_js = Resource(
    lib,
    "js/bloodhound.js",
    minified="js/bloodhound.min.js",
)

typeahead_js = typeahead_jquery_js = Resource(
    lib,
    "js/typeahead.jquery.js",
    minified="js/typeahead.jquery.min.js",
    depends=[jquery],
)
