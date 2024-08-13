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
        # Add hosts: producer, consumer
        producer = self.addHost('producer')
        consumer = self.addHost('consumer')

        # Connnect the consumer and producer
        self.addLink(consumer, producer, delay='10ms')

if __name__ == '__main__':
    setLogLevel('info')

    Minindn.cleanUp()
    Minindn.verifyDependencies()

    # Use the custom topology
    ndn = Minindn(topo=SimpleTopo())
    ndn.start()

    info('Starting NFD on nodes\n')
    nfds = AppManager(ndn, ndn.net.hosts, Nfd)
    info('Starting NLSR on nodes\n')
    nlsrs = AppManager(ndn, ndn.net.hosts, Nlsr)
    sleep(30)  # Wait for NLSR to start

    # Deploy the producer and consumer
    producer = ndn.net['producer']
    consumer = ndn.net['consumer']

    # Start the producer and consumer
    producer.cmd("/home/vagrant/mini-ndn/flooding/producer &> /home/vagrant/mini-ndn/flooding/producer.log &")
    consumer.cmd("/home/vagrant/mini-ndn/flooding/consumer &> /home/vagrant/mini-ndn/flooding/consumer.log &")

    MiniNDNCLI(ndn.net)
    ndn.stop()
  
