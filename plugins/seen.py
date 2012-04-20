"""Seen plugin.

This plugin records and retrieves when and where nicks were last seen chatting.

Command: seen

"""

import time

from util import hook


def db_init(db):
    db.execute("CREATE TABLE IF NOT EXISTS seen(lowernick, chan, nick, "
               "time REAL, message, PRIMARY KEY(lowernick, chan))")
    db.commit()

def db_fetch(db, lowernick, chan):
    return db.execute("SELECT nick, time, message FROM seen WHERE "
                      "lowernick = ? AND chan = ?", (lowernick, chan)
                      ).fetchone()

def db_insert(db, lowernick, chan, nick, time, message):
    db.execute("REPLACE INTO seen(lowernick, chan, nick, time, message) "
               "values(?, ?, ?, ?, ?)", (lowernick, chan, nick, time, message))
    db.commit()


time_units = (("year", 60 * 60 * 24 * 365), ("month", 60 * 60 * 24 * 30),
              ("day", 60 * 60 * 24), ("hour", 60 * 60), ("minute", 60),
              ("second", 1))

def time_since(then, now):
    """Determines and formats the time interval between then and now."""
    offset = int(now) - int(then) if int(now) > int(then) else 0
    b = []
    for i, (name, duration) in enumerate(time_units):
        unit, offset = divmod(offset, duration)
        if unit or (offset == 0 and duration == 1):
            b.append("%d %s%s" % (unit, name, ("s" if unit > 1 else "")))
        if len(b) == 2:
            break
    return ", ".join(b)


@hook.singlethread
@hook.event("PRIVMSG")
def watch_nicks(inp, input=None, db=None):
    """Records nick, chan, time and text of every PRIVMSG."""
    # Only record messages sent to chans
    if input.chan[:1] in ("#", "&", "+", "!"):
        db_init(db)
        db_insert(db, input.nick.lower(), input.chan,
                  input.nick, time.time(), input.msg)

@hook.command
def seen(inp, input=None, db=None, conn=None):
    """.seen <nick> -- Indicates when and where <nick> was last seen."""
    if inp.find(" ") != -1:
        return "You must provide a valid nick."

    lowernick = inp.lower()
    if conn.nick.lower() == lowernick:
        return "I'm right here."
    if input.nick.lower() == lowernick:
        return "You're right here."

    db_init(db)
    query = db_fetch(db, lowernick, input.chan)
    if query is not None:
        who = "%s was" % query[0]
        where = input.chan
        when = "%s ago" % time_since(query[1], time.time())
        what = query[2].replace("\x01ACTION", "me *").strip()
        return "%s last seen %s in %s saying: %s" % (who, when, where, what)
    else:
        return "I've never seen %s chat in %s." % (inp, input.chan)
