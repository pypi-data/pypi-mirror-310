import os
import sys
from ..objects import Service
from MainShortcuts2 import ms
SERVICES_DIR = "%s/var/service" % os.environ["PREFIX"]
WRAPPER_PATH = os.path.dirname(os.path.dirname(__file__)) + "/wrapper.py"


def write(svc: Service, reload: bool = False, *, filename: str = None, path: str = None):
  """Записать файл сервиса в папку сервисов или по указанному пути"""
  if path is None:
    if filename is None:
      if svc.name is None:
        raise ValueError("The service has no name. Indicate the file name to recording the service")
      filename = svc.name
    path = SERVICES_DIR + "/" + filename
  ms.dir.create(path + "/log")
  ms.path.link(os.environ["PREFIX"] + "/share/termux-services/svlogger", path + "/log/run")
  code = "#!%s\nimport os" % sys.executable
  if svc.always_restart:
    if svc.restart_sec:
      code += "\nfrom time import sleep"
    code += "\nwhile True:\n  os.system(%r)" % svc.cmd
    if svc.restart_sec:
      code += "\n  sleep(%i)" % svc.restart_sec
  else:
    code += "\nos.system(%r)" % svc.cmd
  ms.file.write(path + "/run", code)
  ms.proc.call("chmod", "+x", path + "/run", path + "/log/run")
  if reload:
    ms.proc.call("service-daemon", "restart")
  return path


def make_wrapper(name: str, args: list[str], *,
                 clear_env: bool = False,
                 cwd: str = None,
                 data_dir: str = None,
                 env: dict[str, str] = None,
                 exe: str = None,
                 reload: bool = False,
                 stderr: str = None,
                 stdin: str = None,
                 stdout: str = None,
                 **svc_kw) -> str:
  if data_dir is None:
    data_dir = SERVICES_DIR + "/%s/MainServiceAPI" % name
  ms.dir.create(data_dir)
  data = {"format": 1}
  data["args"] = list(args)
  data["clear_env"] = bool(clear_env)
  if not cwd is None:
    data["cwd"] = ms.path.path2str(cwd, True)
  if not env is None:
    data["env"] = dict(env)
  if not exe is None:
    data["exe"] = ms.path.path2str(exe, True)
  if not stderr is None:
    data["stderr"] = ms.path.path2str(stderr, True)
  if not stdin is None:
    data["stdin"] = ms.path.path2str(stdin, True)
  if not stdout is None:
    data["stdout"] = ms.path.path2str(stdout, True)
  filepath = "%s/wrapper.json" % data_dir
  ms.json.write(filepath, {"MainServiceAPI/wrapper": data})
  svc_kw["name"] = name
  svc_kw["cmd"] = [sys.executable, WRAPPER_PATH, filepath]
  return os.path.basename(write(Service(**svc_kw), reload=reload))
