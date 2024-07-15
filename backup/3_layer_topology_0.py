from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import time
import threading

class TreeTopo(Topo):
    def build(self):
        # Add core switch
        core = self.addSwitch('core1')

        # Add aggregation switches
        agg1 = self.addSwitch('agg1')
        agg2 = self.addSwitch('agg2')

        # Add access switches
        acc1 = self.addSwitch('acc1')
        acc2 = self.addSwitch('acc2')
        acc3 = self.addSwitch('acc3')
        acc4 = self.addSwitch('acc4')
        acc5 = self.addSwitch('acc5')
        acc6 = self.addSwitch('acc6')

        # Add links core to aggregation switches
        self.addLink(core, agg1, cls=TCLink, bw=1000, delay='10ms')
        self.addLink(core, agg2, cls=TCLink, bw=1000, delay='10ms')

        # Add links aggregation to access switches
        self.addLink(agg1, acc1, cls=TCLink, bw=1000, delay='5ms')
        self.addLink(agg1, acc2, cls=TCLink, bw=1000, delay='5ms')
        self.addLink(agg1, acc3, cls=TCLink, bw=1000, delay='5ms')
        self.addLink(agg2, acc4, cls=TCLink, bw=1000, delay='5ms')
        self.addLink(agg2, acc5, cls=TCLink, bw=1000, delay='5ms')
        self.addLink(agg2, acc6, cls=TCLink, bw=1000, delay='5ms')

        # Add hosts
        consumer = self.addHost('consumer')
        producer = self.addHost('producer')

        # Add links access switches to hosts
        self.addLink(consumer, acc1, cls=TCLink, bw=100, delay='2ms')
        self.addLink(producer, acc2, cls=TCLink, bw=100, delay='2ms')

def dynamic_change(net):
    # Wait for a specific time before making changes (e.g., 5 seconds)
    time.sleep(5)
    producer = net.get('producer')
    
    # Disconnect producer from acc2
    net.configLinkStatus('producer', 'acc2', 'down')
    # Connect producer to acc3
    net.addLink(producer, net.get('acc3'), cls=TCLink, bw=100, delay='2ms')
    producer.cmd('ifconfig producer-eth1 up')
    producer.cmd('nfdc register /ndn/producer tcp4://acc3')

    # Wait for another 5 seconds (10 seconds in total) before making next change
    time.sleep(5)
    # Disconnect producer from acc3
    net.configLinkStatus('producer', 'acc3', 'down')
    # Connect producer to acc4
    net.addLink(producer, net.get('acc4'), cls=TCLink, bw=100, delay='2ms')
    producer.cmd('ifconfig producer-eth2 up')
    producer.cmd('nfdc register /ndn/producer tcp4://acc4')

def run():
    topo = TreeTopo()
    net = Mininet(topo=topo, controller=Controller, link=TCLink, switch=OVSSwitch)

    net.start()

    # Ensure no existing NFD processes are running on the nodes
    for host in net.hosts:
        host.cmd('sudo pkill nfd')

    # Start NFD on all nodes
    for host in net.hosts:
        host.cmd('nfd-start &')

    # Wait for NFD to start properly
    time.sleep(2)

    # Set up NFD routing
    consumer = net.get('consumer')
    producer = net.get('producer')

    # Initial setup
    producer.cmd('nfdc register /ndn/producer tcp4://acc2')
    consumer.cmd('nfdc register /ndn/consumer tcp4://acc1')

    # Run producer and consumer executables
    producer.cmd('/home/m26a1pershing/NDN/mini-ndn/examples/flooding/producer &> /tmp/producer.log &')
    consumer.cmd('/home/m26a1pershing/NDN/mini-ndn/examples/flooding/consumer &> /tmp/consumer.log &')

    # Schedule the dynamic change in topology
    threading.Thread(target=dynamic_change, args=(net,)).start()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
