from time import sleep
from mininet.log import setLogLevel, info
from minindn.minindn import Minindn
from minindn.util import MiniNDNCLI
from minindn.apps.app_manager import AppManager
from minindn.apps.nfd import Nfd
from minindn.apps.nlsr import Nlsr
from mininet.topo import Topo

class SimpleTopo(Topo):
    def build(self):
        # 添加主机: producer, consumer
        producer = self.addHost('producer')
        consumer = self.addHost('consumer')

        # 连接 consumer 和 producer
        self.addLink(consumer, producer, delay='10ms')

if __name__ == '__main__':
    setLogLevel('info')

    Minindn.cleanUp()
    Minindn.verifyDependencies()

    # 使用自定义的拓扑
    ndn = Minindn(topo=SimpleTopo())
    ndn.start()

    info('Starting NFD on nodes\n')
    nfds = AppManager(ndn, ndn.net.hosts, Nfd)
    info('Starting NLSR on nodes\n')
    nlsrs = AppManager(ndn, ndn.net.hosts, Nlsr)
    sleep(30)  # 等待NLSR启动并稳定

    # 获取生产者和消费者
    producer = ndn.net['producer']
    consumer = ndn.net['consumer']

    # 启动生产者和消费者应用程序
    producer.cmd("/home/vagrant/mini-ndn/flooding/producer &> /home/vagrant/mini-ndn/flooding/producer.log &")
    consumer.cmd("/home/vagrant/mini-ndn/flooding/consumer &> /home/vagrant/mini-ndn/flooding/consumer.log &")

    MiniNDNCLI(ndn.net)
    ndn.stop()
