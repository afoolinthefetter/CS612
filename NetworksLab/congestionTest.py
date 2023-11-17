from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
import time
class NetworkTopo(Topo):
    "A simple network topology with two switches and four hosts"

    def build(self, **_opts):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')
        h3 = self.addHost('h3', ip='10.0.0.3')
        h4 = self.addHost('h4', ip='10.0.0.4')

        self.addLink(s1, s2, intfName1='s1-eth0', intfName2='s2-eth0')
        self.addLink(h1, s1, intfName2='s1-eth1')
        self.addLink(h2, s1, intfName2='s1-eth2')
        self.addLink(h3, s2, intfName2='s2-eth1')
        self.addLink(h4, s2, intfName2='s2-eth2')

if __name__ == '__main__':
    topo = NetworkTopo()
    net = Mininet(topo=topo, controller=None)
    net.start()

    # Add a small delay before attempting to ping
    time.sleep(2)

    # Now let's ping between hosts
    h1, h2, h3, h4 = net.get('h1', 'h2', 'h3', 'h4')

    # Ping h2 from h1
    result1 = h1.cmd('ping -c 3', h2.IP())
    print(f'Ping result from h1 to h2:\n{result1}')

    # Ping h3 from h4
    result2 = h4.cmd('ping -c 3', h3.IP())
    print(f'Ping result from h4 to h3:\n{result2}')

    # Stop the Mininet network
    net.stop()

