import attr


@attr.s(repr=False)
class CSPObject:
    default_src = attr.ib(convert=frozenset, default=frozenset())

    # The following fall back to default_src
    child_src = attr.ib(convert=frozenset, default=frozenset())
    connect_src = attr.ib(convert=frozenset, default=frozenset())
    font_src = attr.ib(convert=frozenset, default=frozenset())
    img_src = attr.ib(convert=frozenset, default=frozenset())
    manifest_src = attr.ib(convert=frozenset, default=frozenset())
    media_src = attr.ib(convert=frozenset, default=frozenset())
    object_src = attr.ib(convert=frozenset, default=frozenset())
    script_src = attr.ib(convert=frozenset, default=frozenset())
    style_src = attr.ib(convert=frozenset, default=frozenset())

    # The following fall back to child_src (then default_src)
    frame_src = attr.ib(convert=frozenset, default=frozenset())
    worker_src = attr.ib(convert=frozenset, default=frozenset())

    # The following fail open (don't fall back to default_src)
    base_uri = attr.ib(convert=frozenset, default=frozenset())
    form_action = attr.ib(convert=frozenset, default=frozenset())
    frame_ancestors = attr.ib(convert=frozenset, default=frozenset())

    # The following are not source lists (and so cannot fall back to
    # default_src)
    block_all_mixed_content = attr.ib(convert=bool, default=False)
    plugin_types = attr.ib(convert=frozenset, default=frozenset())
    referrer = attr.ib(default=None)
    report_uri = attr.ib(default=None)
    require_sri_for = attr.ib(convert=frozenset, default=frozenset())
    sandbox = attr.ib(convert=bool, default=False)
    sandbox_allow = attr.ib(convert=frozenset, default=frozenset())
    upgrade_insecure_requests = attr.ib(convert=bool, default=False)

    def __repr__(self):
        rv = []
        for k, v in attr.asdict(self).items():
            if not v:
                continue

            if isinstance(v, bool):
                rv.append("{}=True".format(k))

            elif isinstance(v, frozenset):
                rv.append("{}={{{}}}".format(
                    k, ', '.join(repr(vi) for vi in v)))

            else:
                rv.append("{}={}".format(k, repr(v)))
        return 'CSPObject({})'.format(', '.join(rv))

    def __str__(self):
        rv = []
        for k, v in attr.asdict(self).items():
            key = k.replace('_', '-')

            if not v:
                continue

            if isinstance(v, bool):
                rv.append(key)

            elif isinstance(v, frozenset):
                rv.append("{} {}".format(key, ' '.join(v)))

            else:
                rv.append("{} {}".format(key, v))
        return '; '.join(rv)
