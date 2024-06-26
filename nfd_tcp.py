import json
import os

from minindn.apps.application import Application
from minindn.util import copyExistentFile
from minindn.minindn import Minindn

class Nfd(Application):
    def __init__(self, node, logLevel='INFO', csSize=65536,
                 csPolicy='lru', csUnsolicitedPolicy='drop-all'):
        Application.__init__(self, node)
        self.logLevel = node.params['params'].get('nfd-log-level', logLevel)

        self.confFile = '{}/nfd.conf'.format(self.homeDir)
        self.logFile = 'nfd.log'
        self.ndnFolder = '{}/.ndn'.format(self.homeDir)
        self.clientConf = '{}/client.conf'.format(self.ndnFolder)

        possibleConfPaths = ['/usr/local/etc/ndn/nfd.conf', '/usr/local/etc/ndn/nfd.conf.sample',
                             '/etc/ndn/nfd.conf', '/etc/ndn/nfd.conf.sample']
        copyExistentFile(node, possibleConfPaths, self.confFile)

        conf_file = json.loads(node.cmd("infoconv info2json < {}".format(self.confFile)))

        if "log" not in conf_file:
            conf_file["log"] = {}

        conf_file["log"]["default_level"] = self.logLevel

        if "unix" in conf_file["face_system"]:
            del conf_file["face_system"]["unix"]

        os.makedirs(self.ndnFolder, exist_ok=True)
        with open(self.clientConf, "w") as client_conf_file:
            client_conf_file.write("transport=tcp4://127.0.0.1:6363\n")

        conf_file["tables"]["cs_max_packets"] = csSize
        conf_file["tables"]["cs_policy"] = csPolicy
        conf_file["tables"]["cs_unsolicited_policy"] = csUnsolicitedPolicy

        with open("{}/temp_nfd_conf.json".format(self.homeDir), "w") as temp_file:
            json.dump(conf_file, temp_file)

        node.cmd("infoconv json2info < {}/temp_nfd_conf.json > {}".format(self.homeDir, self.confFile))

        os.remove("{}/temp_nfd_conf.json".format(self.homeDir))

        if not Minindn.ndnSecurityDisabled:
            node.cmd('ndnsec-key-gen /localhost/operator | ndnsec-cert-install -')

    def start(self):
        Application.start(self, 'nfd --config {}'.format(self.confFile), logfile=self.logFile)
        Minindn.sleep(0.5)
