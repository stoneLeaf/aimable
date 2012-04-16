import inspect
import json
import os


def save(conf):
    json.dump(conf, open('config', 'w'), sort_keys=True, indent=2)

if not os.path.exists('config'):
    open('config', 'w').write(inspect.cleandoc(
        r'''
        {
          "connections":
          {
            "local irc":
            {
              "server": "localhost",
              "nick": "aimable",
              "channels": ["#test"]
            }
          },
          "disabled_plugins": [],
          "disabled_commands": [],
          "acls": {},
          "api_keys": {},
          "censored_strings":
          [
            "DCC SEND",
            "1nj3ct",
            "thewrestlinggame",
            "startkeylogger",
            "hybux",
            "\\0",
            "\\x01",
            "!coz",
            "!tell /x"
          ]
        }''') + '\n')


def config():
    """Reload config from file if it has changed."""
    config_mtime = os.stat('config').st_mtime
    if bot._config_mtime != config_mtime:
        try:
            bot.config = json.load(open('config'))
            bot._config_mtime = config_mtime
        except ValueError, e:
            print 'ERROR: malformed config file', e


bot._config_mtime = 0
