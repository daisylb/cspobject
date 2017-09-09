from hypothesis import strategies as s

from .. import CSPObject

HOST_SOURCES = (
    "http://example.com",
    "http://example.net",
    "https://example.com",
    "https://example.net",
    "https://foo.example.com",
    "https://*.example.net",
    "example.org",
)

SCHEME_SOURCES = ("http:", "https:", "data:")

SPECIAL_SOURCES = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "'none'",
)

sources = s.sampled_from(HOST_SOURCES + SCHEME_SOURCES + SPECIAL_SOURCES)
source_list = s.frozensets(sources)
csp_object = s.builds(
    CSPObject,
    default_src=source_list,
    child_src=source_list,
    connect_src=source_list,
    font_src=source_list,
    img_src=source_list,
    manifest_src=source_list,
    media_src=source_list,
    object_src=source_list,
    script_src=source_list,
    style_src=source_list,
    frame_src=source_list,
    worker_src=source_list,
    base_uri=source_list,
    form_action=source_list,
    frame_ancestors=source_list,
    block_all_mixed_content=s.booleans(),
    upgrade_insecure_requests=s.booleans(),
    # TODO: implement strategies for the rest of the args
)
