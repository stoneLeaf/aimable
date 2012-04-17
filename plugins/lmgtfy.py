"""Let Me Google That For You (LMGTFY) plugin.

This plugin forms LMGTFY links.

Command: lmgtfy
Regex: '<nick> lmgtfy <query>'
"""

from urllib import quote

from util import hook


base_url = "http://lmgtfy.com/?q="

@hook.command
def lmgtfy(inp, say=None):
    ('.lmgtfy <query> | <user> lmgtfy <query> -- returns a Let Me Google That '
     'For You link to <query> / highlighting <user>')

    say('%s%s' % (base_url, quote(inp.encode("utf-8"))))

@hook.regex(r'(?i)^([a-zA-Z0-9_<\-\[\]\\\^{}]{2,15})[,:]? lmgtfy +(.+)$')
def lmgtfyregex(match, say=None, conn=None):
    """Regex hook matching the pattern '<nick> lmgtfy <query>'."""
    if match.group(1) != conn.nick:
        say('%s: %s%s' % (match.group(1), base_url,
                          quote(match.group(2).rstrip().encode("utf-8"))))