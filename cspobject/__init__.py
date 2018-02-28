import attr


def _to_frozenset(value):
    """Convert cspobject arguments into frozensets."""

    if isinstance(value, str):
        return frozenset(value.split())
    return frozenset(value)


def _sandbox_convert(value):
    """Normalise values for the 'sandbox' argument."""

    # False indicates the sandbox attribute is not present.
    # True indicates that it is present, but has no exceptions.
    if isinstance(value, bool):
        return value

    # If the user passes a falsy value that isn't False, they probably
    # passed an empty iterable, which means they probably expect the
    # same behaviour as True (i.e. 'sandbox' with no exceptions).
    # In this case return True.
    if not value and value is not False:
        return True

    # If there's a list of exceptions, return it as a frozen set.
    return _to_frozenset(value)


@attr.s(repr=False)
class CSPObject:
    default_src = attr.ib(convert=_to_frozenset, default=frozenset())

    # The following fall back to default_src
    child_src = attr.ib(convert=_to_frozenset, default=frozenset())
    connect_src = attr.ib(convert=_to_frozenset, default=frozenset())
    font_src = attr.ib(convert=_to_frozenset, default=frozenset())
    img_src = attr.ib(convert=_to_frozenset, default=frozenset())
    manifest_src = attr.ib(convert=_to_frozenset, default=frozenset())
    media_src = attr.ib(convert=_to_frozenset, default=frozenset())
    object_src = attr.ib(convert=_to_frozenset, default=frozenset())
    script_src = attr.ib(convert=_to_frozenset, default=frozenset())
    style_src = attr.ib(convert=_to_frozenset, default=frozenset())

    # The following fall back to child_src (then default_src)
    frame_src = attr.ib(convert=_to_frozenset, default=frozenset())
    worker_src = attr.ib(convert=_to_frozenset, default=frozenset())

    # The following fail open (don't fall back to default_src)
    base_uri = attr.ib(convert=_to_frozenset, default=frozenset())
    form_action = attr.ib(convert=_to_frozenset, default=frozenset())
    frame_ancestors = attr.ib(convert=_to_frozenset, default=frozenset())

    # The following are not source lists (and so cannot fall back to
    # default_src)
    block_all_mixed_content = attr.ib(convert=bool, default=False)
    plugin_types = attr.ib(convert=_to_frozenset, default=frozenset())
    referrer = attr.ib(default=None)
    report_uri = attr.ib(default=None)
    require_sri_for = attr.ib(convert=_to_frozenset, default=frozenset())
    # Sandbox can either be
    sandbox = attr.ib(convert=_sandbox_convert, default=False)
    upgrade_insecure_requests = attr.ib(convert=bool, default=False)

    @classmethod
    def parse(cls, policy):
        if not policy:
            return CSPObject()

        kwargs = {}
        for directive_str in policy.split(';'):
            directive, *args = directive_str.split()
            arg = directive.replace('-', '_')
            if directive in (
                'block-all-mixed-content',
                'upgrade-insecure-requests',
            ):
                kwargs[arg] = True
            else:
                kwargs[arg] = args
        print('kwargs=%r' % kwargs)
        return cls(**kwargs)

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

    def _fallback_union(self, other, the_attr, child_src=False):
        self_v = getattr(self, the_attr)
        other_v = getattr(other, the_attr)
        if not (self_v or other_v):
            return frozenset()
        self_fb = self_v or (child_src and self.child_src) or self.default_src
        other_fb = other_v or (
            child_src and other.child_src) or other.default_src
        return self_fb.union(other_fb)

    def __or__(self, other):
        if not isinstance(other, CSPObject):
            raise TypeError("Expected CSPObject, got {}".format(type(other)))

        if self.referrer and other.referrer:
            raise ValueError("Cannot union two CSPObjects that both have the "
                             "(deprecated) referrer directive set")
        if self.report_uri and other.report_uri and self.report_uri != other.report_uri:
            raise ValueError("Cannot union two CSPObjects that both have the "
                             "report-uri directive set to different values")

        if not self.sandbox or not other.sandbox:
            sandbox = False
        else:
            our_sb = frozenset() if self.sandbox is True else self.sandbox
            their_sb = frozenset() if other.sandbox is True else other.sandbox
            sandbox = our_sb.union(their_sb)

        return CSPObject(
            default_src=self.default_src.union(other.default_src),
            child_src=self._fallback_union(other, 'child_src'),
            connect_src=self._fallback_union(other, 'connect_src'),
            font_src=self._fallback_union(other, 'font_src'),
            img_src=self._fallback_union(other, 'img_src'),
            manifest_src=self._fallback_union(other, 'manifest_src'),
            media_src=self._fallback_union(other, 'media_src'),
            object_src=self._fallback_union(other, 'object_src'),
            script_src=self._fallback_union(other, 'script_src'),
            style_src=self._fallback_union(other, 'style_src'),
            frame_src=self._fallback_union(other, 'frame_src', child_src=True),
            worker_src=self._fallback_union(
                other, 'worker_src', child_src=True),
            base_uri=self.base_uri.union(other.base_uri),
            form_action=self.form_action.union(other.form_action),
            frame_ancestors=self.frame_ancestors.union(other.frame_ancestors),
            block_all_mixed_content=self.block_all_mixed_content and other.block_all_mixed_content,
            plugin_types=self.plugin_types.union(other.plugin_types),
            referrer=self.referrer or other.referrer,
            sandbox=sandbox,
            upgrade_insecure_requests=self.upgrade_insecure_requests and other.upgrade_insecure_requests,
        )

    @classmethod
    def union(cls, *policies):
        if not policies:
            return CSPObject()
        output = policies[0]
        if isinstance(output, str):
            output = cls.parse(output)
        if not isinstance(output, CSPObject):
            raise TypeError("Expected CSPObject, got {}".format(type(output)))
        for policy in policies[1:]:
            if isinstance(policy, str):
                policy = cls.parse(policy)
            if not isinstance(policy, CSPObject):
                raise TypeError(
                    "Expected CSPObject, got {}".format(type(policy)))
            output |= policy
        return output
