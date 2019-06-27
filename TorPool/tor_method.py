# coding: utf-8
import subprocess
import shutil
import sys
import os

class TorMethod(object):
    '''tor 代理伺服器製作
    :::參數說明:::
    torrc_dir: torrc要儲存的位置(必要)
    tordata_dir: torrc內DataDirectory的資訊(必要)
    __process: tor的process控制器, 可以使用TorMethod.get_process取得
    __torname: torrc檔案和資料夾的名稱, 可以使用TorMethod.get_toruuid取得
    __torrcfile: torrc檔案路徑, 可以使用TorMethod.get_torrcpath取得
    __tordatafile: torrc內DataDirectory的資訊, 可以使用TorMethod.get_torrcpath取得
    __socksport: Tor opens a SOCKS proxy on port [socksport]
    __controlport: The port on which Tor will listen for local connections from Tor
                   controller applications, as documented in control-spec.txt.
    '''
    def __init__(self, torrc_dir, tordata_dir, hashedcontrolpassword):
        from . import _TOR_EXE
        if sys.platform is 'win32':
            self.__tor_exe = _TOR_EXE
        else:
            self.__tor_exe = os.popen('which tor').read().rstrip('\n')
            if self.__tor_exe is '':
                error_msg = (
                    "\'Tor client\' is not installed. Please insatll tor client first!\n"
                    "\t  If Your system is debian or ubuntu, please execute \'sudo apt install tor -y\'.\n"
                    "\t  If Your system is macOS, please install homebrew and execute \'brew install tor -y\'.\n"
                )
                raise OSError(error_msg)
        self.torrc_dir = torrc_dir #
        self.tordata_dir = tordata_dir #
        self.hashedcontrolpassword = hashedcontrolpassword
        import uuid
        self.__process = None #
        self.__torname = str(uuid.uuid4()) #
        self.__torrcfile = os.path.join(self.torrc_dir, self.__torname + '.conf') #
        self.__tordatafile = os.path.join(self.tordata_dir, self.__torname)
        self.__socksport = None #
        self.__controlport = None #
        self.__hashed = self.__tor_hashpasswd()
        if os.path.exists(self.torrc_dir):
            shutil.rmtree(self.torrc_dir)
            os.makedirs(self.torrc_dir)
        if os.path.exists(self.tordata_dir):
            shutil.rmtree(self.tordata_dir)
            os.makedirs(self.tordata_dir)

    @property
    def get_status(self):
        if self.__process is None:
            pid = None
        else:
            pid = self.__process.pid
        return {
            'tor_exe': self.__tor_exe,
            'socksport': self.__socksport,
            'process': pid,
            'tor_uuid': self.__torname,
            'torrc_path': self.__torrcfile,
            'torrcdata_path': self.__tordatafile,
        }

    def __tor_hashpasswd(self):
        process = subprocess.Popen(self.__tor_exe + ' --hash-password ' + str(self.hashedcontrolpassword), shell=True, stdout=subprocess.PIPE)
        return str(process.stdout.readline().decode('utf-8')).rstrip('\n')

    def get_free_port(self):
        '''找閒置port'''
        from socket import socket
        port = None
        with socket() as s:
            s.bind(('',0))
            port = s.getsockname()[1]
            s.close()
        return port

    def make_torrc(self):
        '''寫出torrc'''
        if not os.path.exists(self.torrc_dir):
            os.makedirs(self.torrc_dir)
        if not os.path.exists(self.tordata_dir):
            os.makedirs(self.tordata_dir)
        with open(self.__torrcfile, 'w') as f:
            torrc = self.torrc()
            f.write(torrc)

    def torrc(self):
        '''torrc格式'''
        if self.__socksport is None:
            self.__socksport = self.get_free_port()
        if self.__controlport is None:
            self.__controlport = self.get_free_port()
        torrc_file = (
            'HashedControlPassword {hashedcontrolpassword}\n'
            'SocksPort {socksport}\n'
            'ControlPort {controlport}\n'
            'DataDirectory {tordatafile}\n'
        )
        return torrc_file.format(
            hashedcontrolpassword = self.__hashed,
            socksport = self.__socksport,
            controlport = self.__controlport,
            tordatafile = self.__tordatafile
        )

    def start_tor(self):
        '''啟動tor'''
        if self.__process is not None:
            self.__process.kill()
        else:
            process = subprocess.Popen(self.__tor_exe + ' -f ' + self.__torrcfile, shell=True)
            self.__process = process

    def restart_tor(self):
        '''若proxy被封鎖，殺掉程序重新執行tor'''
        self.__process.kill()
        self.start_tor()

    def kill_process(self):
        '''殺死利用套件啟動的tor程序'''
        self.__process.kill()
        shutil.rmtree(self.torrcfile)
        shutil.rmtree(self.tordatafile)
        self.__process = None

    def kill_all_tor(self):
        '''殺死系統所有存在的tor'''
        if sys.platform is 'win32':
            os.system('TASKKILL /F /IM tor.exe /T')
        else:
            os.system('killall -9 tor')
        self.pool = []