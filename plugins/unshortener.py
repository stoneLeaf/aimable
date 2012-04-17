"""URL unshortener plugin

This plugin returns the real URLs behind shortened URLs.

Supported services: tinyurl.com, bit.ly, t.co, dlvr.it, goo.gl, is.gd, ow.ly

"""

from util import hook, http


@hook.regex(r'(?i)https?://(?:www\.)?tinyurl.com/[a-z0-9\-]+')
@hook.regex(r'(?i)https?://(?:www\.)?(?:bit.ly|j.mp)/[a-z0-9]+')
@hook.regex(r'(?i)https?://(?:www\.)?t.co/[a-z0-9]+')
@hook.regex(r'(?i)https?://(?:www\.)?dlvr.it/[a-z0-9]+')
@hook.regex(r'(?i)https?://(?:www\.)?goo.gl/(?:fb/)?[a-z0-9]+')
@hook.regex(r'(?i)https?://(?:www\.)?is.gd/[a-z0-9]+')
@hook.regex(r'(?i)https?://(?:www\.)?ow.ly/[a-z0-9]+')
def unshorten(match, say=None):
    try:
        return http.open(match.group(), get_method="HEAD").url.strip()
    except http.URLError:
        pass