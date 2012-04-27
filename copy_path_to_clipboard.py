import sublime, sublime_plugin
import os

class CopyPathToClipboard(sublime_plugin.TextCommand):
  def run(self, edit):
    line_number, column = self.view.rowcol(self.view.sel()[0].begin())
    line_number += 1
    path = self.view.file_name() + ":" + str(line_number)
    sublime.set_clipboard(path)
    sublime.status_message("Copied " + path)

