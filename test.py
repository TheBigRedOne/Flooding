from mininet.log import setLogLevel, info
from mininet.topo import Topo
from mininet.node import OVSSwitch
from minindn.minindn import Minindn
from minindn.util import MiniNDNCLI
from minindn.apps.app_manager import AppManager
from minindn.apps.nfd import Nfd
from minindn.apps.nlsr import Nlsr

class SimpleTopo(Topo):
    def build(self):
        # 添加三个主机: producer, consumer 和 forwarder
        producer = self.addHost('producer')
        consumer = self.addHost('consumer')
        forwarder = self.addSwitch('fowarder')

        # 连接 producer, forwarder 和 consumer
        self.addLink(producer, forwarder, delay='10ms')
        self.addLink(consumer, forwarder, delay='10ms')

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

    # 获取生产者、消费者和转发者节点
    producer = ndn.net.get('producer')
    consumer = ndn.net.get('consumer')
    forwarder = ndn.net.get('forwarder')

    # 启动 tcpdump 抓取 NDN 数据包
    producer.cmd('tcpdump -i any -w /home/mini-ndn/flooding/test-producer.pcap &')
    consumer.cmd('tcpdump -i any -w /home/mini-ndn/flooding/test-consumer.pcap &')
    forwarder.cmd('tcpdump -i fowarder-eth1 -w /home/mini-ndn/flooding/test-forwarder-producer.pcap &')
    forwarder.cmd('tcpdump -i forwarder-eth2 -w /home/mini-ndn/flooding/test-forwarder-consumer.pcap &')

    # 启动生产者和消费者应用程序
    producer.cmd('/home/mini-ndn/flooding/producer &')
    consumer.cmd('/home/mini-ndn/flooding/consumer &')

    # 等待 10 秒钟抓取数据包
    import time
    time.sleep(10)

    # 停止 tcpdump
    producer.cmd('pkill -f tcpdump')
    consumer.cmd('pkill -f tcpdump')
    forwarder.cmd('pkill -f tcpdump')

    MiniNDNCLI(ndn.net)

    ndn.stop()
