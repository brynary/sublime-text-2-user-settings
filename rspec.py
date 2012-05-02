import sublime
import sublime_plugin
import os, errno
import re

def get_twin_path(path):
  spec_file = path.find("/spec/") >= 0

  if spec_file:
    if path.find("/lib/") > 0:
      return path.replace("/spec/lib/","/lib/").replace("_spec.rb", ".rb")
    else:
      return path.replace("/spec/","/app/").replace("_spec.rb", ".rb")
  else:
    if path.find("/lib/") > 0:
      return path.replace("/lib/", "/spec/lib/").replace(".rb", "_spec.rb")
    else:
      return path.replace("/app/", "/spec/").replace(".rb", "_spec.rb")

class OpenRspecFileCommand(sublime_plugin.WindowCommand):
  def run(self, option):
    self.views = []
    window = self.window
    current_file_path = self.window.active_view().file_name()

    spec_file = current_file_path.find("/spec/") > 0
    twin_path = get_twin_path(current_file_path)
    path_parts = twin_path.split("/")
    dirname = "/".join(path_parts[0:-1])
    basename = path_parts[-1]

    if not os.path.exists(twin_path) and sublime.ok_cancel_dialog(basename + " was not found. Create it?"):
      self.mkdir_p(dirname)
      twin_file = open(twin_path, "w")

      constant_name = self.camelize(basename.replace(".rb", "").replace("_spec", ""))

      if spec_file:
        twin_file.write("class " + constant_name + "\nend")
      else:
        twin_file.write("require \"spec_helper\"\n\ndescribe " + constant_name + " do\nend")
      twin_file.close()

    if os.path.exists(twin_path):
      view = window.open_file(twin_path)
      view.run_command("revert")
    else:
      sublime.status_message("Not found: " + twin_path)


  def mkdir_p(self, path):
      try:
          os.makedirs(path)
      except OSError as exc: # Python >2.5
          if exc.errno == errno.EEXIST:
              pass
          else: raise

  def camelize(self, string):
      return re.sub(r"(?:^|_)(.)", lambda x: x.group(0)[-1].upper(), string)
      import sublime
      import sublime_plugin
      import os, errno
      import re

class RunTests(sublime_plugin.TextCommand):
  def run(self, edit, single):
    path = self.view.file_name()

    if path.find("/spec/") < 0:
      twin_path = get_twin_path(path)
      if os.path.exists(twin_path):
        path = twin_path
      else:
        return sublime.error_message("You're not in a spec, bro.")

    root_path = re.sub("\/spec\/.*", "", path)

    if single:
      line_number, column = self.view.rowcol(self.view.sel()[0].begin())
      line_number += 1
      path += ":" + str(line_number)

    cmd = 'osascript '
    cmd += '"/Users/bhelmkamp/Library/Application Support/Sublime Text 2/Packages/User/run_command.applescript"'
    cmd += ' "cd ' + root_path + ' && time ruby ' + path + '"'
    cmd += ' "Ruby Tests"'
    os.system(cmd)
