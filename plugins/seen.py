"""Seen plugin.

This plugin records and retrieves when and where nicks were last seen chatting.

Command: seen
"""

import time

from util import hook


def db_init(db):
    db.execute("CREATE TABLE IF NOT EXISTS last_seen"
               "(indexnick PRIMARY KEY, nick, chan, time, line REAL)")
    db.commit()

def db_query(db, indexnick):
    return db.execute("SELECT nick, chan, time, line FROM last_seen "
                      "WHERE indexnick = ?", (indexnick,)).fetchone()

def db_record(db, indexnick, nick, chan, time, line):
    db.execute("REPLACE INTO last_seen(indexnick, nick, chan, time, line) "
               "values(?, ?, ?, ?, ?)", (indexnick, nick, chan, time, line))
    db.commit()


time_units = (("year", 60 * 60 * 24 * 365), ("month", 60 * 60 * 24 * 30),
              ("day", 60 * 60 * 24), ("hour", 60 * 60), ("minute", 60),
              ("second", 1))

def time_since(then, now):
    offset = int(now) - int(then)
    b = []
    for i, (name, duration) in enumerate(time_units):
        unit, offset = divmod(offset, duration)
        if unit:
            b.append("%d %s%s" % (unit, name, ("s" if unit > 1 else "")))
        if len(b) == 2:
            break
    return ", ".join(b)


@hook.singlethread
@hook.event("PRIVMSG")
def watch_nicks(inp, input=None, db=None):
    # Don't record private messages
    if input.chan[:1] == "#":
        db_init(db)
        db_record(db, input.user.lower(), input.user,
                  input.chan, time.time(), input.msg)

@hook.command
def seen(inp, input=None, db=None, conn=None):
    """.seen <nick> -- Indicates when and where <nick> was last seen."""

    if inp.find(" ") != -1:
        return "You must provide a valid nick."

    indexnick = inp.lower()
    if conn.nick.lower() == indexnick:
        return "I'm right here."
    if input.nick.lower() == indexnick:
        return "You're right here."

    db_init(db)
    query = db_query(db, indexnick)
    if query is not None:
        who = "%s was" % query[0]
        where = query[1]
        when = "%s ago" % time_since(query[2], time.time())
        what = query[3].replace("\x01ACTION", "me *").strip()
        return "%s last seen %s in %s saying: %s" % (who, when, where, what)
    else:
        return "I've never seen %s chat." % inp
