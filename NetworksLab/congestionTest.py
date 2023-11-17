from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import sys
import time

class NetworkTopo(Topo):
    def build(self, **_opts):
        
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        h1 = self.addSwitch('h1')
        h2 = self.addSwitch('h2')
        h3 = self.addSwitch('h3')
        h4 = self.addSwitch('h4')
        
        self.addLink(s1, s2, intfName1='s1-eth0', intfName2='s2-eth0')
        self.addLink(h1, s1, intfName2='s1-eth1')
        self.addLink(h2, s1, intfName2='s1-eth2')
        self.addLink(h3, s2, intfName2='s2-eth1')
        self.addLink(h4, s2, intfName2='s2-eth2')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Your script description')

    parser.add_argument('--config', choices=['b', 'c'], required=True,
                        help='Specify config option: b or c')
    parser.add_argument('--scheme', choices=['reno', 'vegas', 'cubic', 'bbr', 'all'], required=False,
                        help='Specify scheme option: reno, vegas, cubic, bbr, or all')
    parser.add_argument('--loss', type=float, required=False,
                        help='Specify loss as a number')

    args = parser.parse_args()
    configValue = args.config
    schemeValue = args.scheme
    lossValue = args.loss
    

    schemeAsArg = ""
    if schemeValue:
        schemeAsArg = " -Z " + schemeValue

    #start h4 in server mode no matter what
    h1, h2, h3, h4 = net.getNodeByName('h1', 'h2', 'h3', 'h4')
    h4Server = h4.popen(['iperf', '-s'])

    
    if configValue == 'b':
        h1Client = h1.popen(f'iperf -c {h4.IP()}{schemeAsArg}', shell=True)
        h1Client.wait()
    else:
        h1Client = h1.popen(f'iperf -c {h4.IP()}{schemeAsArg}', shell=True)
        h2Client = h2.popen(f'iperf -c {h4.IP()}{schemeAsArg}', shell=True)
        h3Client = h3.popen(f'iperf -c {h4.IP()}{schemeAsArg}', shell=True)
        h1Client.wait()
        h2Client.wait()
        h3Client.wait()

    
    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)
    net.start()

    CLI(net)
    h4Server.terminate()
    net.stop()
