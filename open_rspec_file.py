import sublime
import sublime_plugin
import os, errno
import re

class OpenRspecFileCommand(sublime_plugin.WindowCommand):
  def run(self, option):
    self.views = []
    window = self.window
    current_file_path = self.window.active_view().file_name()

    spec_file = current_file_path.find("/spec/") > 0

    if spec_file:
      if current_file_path.find("/lib/") > 0:
        twin_path = current_file_path.replace("/spec/lib/","/lib/").replace("_spec.rb", ".rb")
      else:
        twin_path = current_file_path.replace("/spec/","/app/").replace("_spec.rb", ".rb")
    else:
      if current_file_path.find("/lib/") > 0:
        twin_path = current_file_path.replace("/lib/", "/spec/lib/").replace(".rb", "_spec.rb")
      else:
        twin_path = current_file_path.replace("/app/", "/spec/").replace(".rb", "_spec.rb")

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
