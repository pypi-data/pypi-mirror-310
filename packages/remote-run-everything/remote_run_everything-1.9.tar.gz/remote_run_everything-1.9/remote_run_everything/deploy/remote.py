import os

import pysftp

from remote_run_everything.deploy.hist_pickle import Hist


class Remote:
    def __init__(self, conf):
        self.c = conf
        self.hist = Hist(self.c.local_root)

    def conn(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        return pysftp.Connection(self.c.host, username=self.c.user, port=self.c.port, password=self.c.pwd,
                                 cnopts=cnopts)

    def upload(self, data):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(self.c.host, username=self.c.user, port=self.c.port, password=self.c.pwd,
                               cnopts=cnopts) as shell:
            for i in data:
                will_up = self.hist.upload_record_or_not(self.c.host, i[0])
                if will_up:
                    print("upload file:", i[0])
                    remote_dir = os.path.dirname(i[1])
                    shell.makedirs(remote_dir, mode=777)
                    shell.put(i[0], i[1])

    def download(self, data):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(self.c.host, username=self.c.user, port=self.c.port, password=self.c.pwd,
                               cnopts=cnopts) as shell:
            for i in data:
                local_dir = os.path.dirname(i[0])
                os.makedirs(local_dir, exist_ok=True, mode=777)
                shell.get(i[1], i[0])

    def get_remote(self, dir):
        files = self._get_remote(dir, [])
        return files

    def _get_remote(self, root, res):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(self.c.host, username=self.c.user, port=self.c.port, password=self.c.pwd,
                               cnopts=cnopts) as shell:
            data = shell.listdir(root)
            for d in data:
                new = os.path.join(root, d).replace("\\", "/")
                if shell.isfile(new):
                    res.append(new)
                else:
                    self._get_remote(new, res)
        return res

    def cmd(self, cmds):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(self.c.host, username=self.c.user, port=self.c.port, password=self.c.pwd,
                               cnopts=cnopts) as shell:
            common_cmds = ["/usr/bin/bash -c", f"cd {self.c.remote_root}"]
            all = common_cmds + cmds
            cmd = ";".join(all)
            res = shell.execute(cmd)
            print("***********************")
            for i in res:
                print(i.decode("utf-8"))
