import sublime, sublime_plugin
import os
import subprocess

SQLITE_BIN_PATH = '/usr/bin/sqlite3'

class SqliteCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    region_all = sublime.Region(0, self.view.size())
    self.view.erase(edit, region_all)

    sqlite_dump = subprocess.check_output([
      SQLITE_BIN_PATH,
      self.view.file_name(),
      '.dump'
    ])
    sqlite_dump = sqlite_dump.decode('ascii', 'ignore')

    self.view.insert(edit, 0, sqlite_dump)


class EventListener(sublime_plugin.EventListener):
  def on_load(self, view):
    if not os.path.isfile(SQLITE_BIN_PATH):
      print('sqlite3 not found at {}, exiting'.format(SQLITE_BIN_PATH))
      return

    ext = os.path.splitext(view.file_name())[1]
    if not ext == '.sqlite3':
      return

    view.run_command('sqlite')
