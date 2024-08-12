from time import sleep
from mininet.log import setLogLevel, info
from minindn.minindn import Minindn
from minindn.util import MiniNDNCLI
from minindn.apps.app_manager import AppManager
from minindn.apps.nfd import Nfd
from minindn.apps.nlsr import Nlsr
from mininet.topo import Topo

class CustomTopo(Topo):
    def build(self):
        # 添加核心交换机
        core = self.addHost('s1')

        # 添加汇聚交换机
        agg1 = self.addHost('s2')
        agg2 = self.addHost('s3')

        # 添加接入交换机
        acc1 = self.addHost('s4')
        acc2 = self.addHost('s5')
        acc3 = self.addHost('s6')
        acc4 = self.addHost('s7')
        acc5 = self.addHost('s8')
        acc6 = self.addHost('s9')

        # 添加主机: producer 和 consumer
        producer = self.addHost('producer')
        consumer = self.addHost('consumer')

        # 连接交换机，设置带宽和延迟
        self.addLink(core, agg1, bw=100, delay='10ms')
        self.addLink(core, agg2, bw=100, delay='10ms')
        
        self.addLink(agg1, acc1, bw=100, delay='5ms')
        self.addLink(agg1, acc2, bw=100, delay='5ms')
        self.addLink(agg1, acc3, bw=100, delay='5ms')
        
        self.addLink(agg2, acc4, bw=100, delay='5ms')
        self.addLink(agg2, acc5, bw=100, delay='5ms')
        self.addLink(agg2, acc6, bw=100, delay='5ms')

        # 连接主机到接入交换机
        self.addLink(consumer, acc1, bw=100, delay='2ms')
        self.addLink(producer, acc2, bw=100, delay='2ms')  # 初始连接到acc2

if __name__ == '__main__':
    setLogLevel('info')

    Minindn.cleanUp()
    Minindn.verifyDependencies()

    # 使用自定义拓扑
    ndn = Minindn(topo=CustomTopo())
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

    # 调度生产者切换连接
    #sleep(20)
    #info('Switching producer to acc3\n')
    #ndn.net.configLinkStatus('producer', 's5', 'down')
    #ndn.net.configLinkStatus('producer', 's6', 'up')

    #sleep(10)
    #info('Switching producer to acc4\n')
    #ndn.net.configLinkStatus('producer', 's6', 'down')
    #ndn.net.configLinkStatus('producer', 's7', 'up')

    MiniNDNCLI(ndn.net)
    ndn.stop()
