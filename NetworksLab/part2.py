from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import sys
import time


class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    "A LinuxRouter connecting three IP subnets"

    def build(self, **_opts):
        s1, s2 = [self.addSwitch(s) for s in ('s1', 's2')]
        h1, h2, h3, h4 = [self.addHost(h) for h in ('h1', 'h2', 'h3', 'h4')]
        self.addLink(s1, s2, intfName1='s1-eth-2', intfName2='s2-eth-2')
        self.addLink(h1, s1, intfName2='s1-eth-0')
        self.addLink(h2, s1, intfName2='s1-eth-1')
        self.addLink(h3, s2, intfName2='s2-eth-0')
        self.addLink(h4, s2, intfName2='s2-eth-1')


if __name__ == '__main__':
    args = sys.argv
    scheme = ''
    loss = 0
    config = ''
    flag = 0
    if len(args) < 3:
        flag = 1
        print("Please specify valid configuration")
    else:
        if len(args) % 2 == 0:
            flag = 1
            print("Please specify valid configuration")
        else:
            if len(args) >= 3:
                if args[1] == '--config':
                    if args[2] != 'b' and args[2] != 'c':
                        flag = 1
                        print("please specify valid configuration")
                    else:
                        config = str(args[2])
                else:
                    flag = 1
                    print("Please specify valid argument")
            if len(args) >= 5:
                if args[3] == '--scheme':
                    if args[4] != 'vegas' and args[4] != 'reno' and args[4] != 'cubic' and args[4] != 'bbr':
                        flag = 1
                        print("please specify valid congestion control scheme")
                    else:
                        scheme = str(args[4])
                else:
                    flag = 1
                    print("please specify valid argument")
            if len(args) == 7:
                if args[5] == '--loss':
                    loss = int(args[6])
                else:
                    flag = 1
                    print("please specify valid argument")
            elif len(args) > 7:
                flag = 1
                print("please specify valid argument")
    if flag == 0:
        # topo = NetworkTopo(config,scheme,loss)
        setLogLevel('info')
        topo = NetworkTopo()
        net = Mininet(topo=topo,
                      waitConnected=True)  # controller is used by s1-s3

        net.start()

        h1, h2, h3, h4 = net.getNodeByName('h1', 'h2', 'h3', 'h4')
        h4open = h4.popen(['iperf', '-s', '-p', '5001'])
        if config == 'c':
            if len(scheme) > 0:
                h1open = h1.popen('iperf -c {0} -p 5001 -t 10 -Z {1}'
                                  .format(h4.IP(), scheme), shell=True)
                h2open = h2.popen('iperf -c {0} -p 5001 -t 10 -Z {1}'
                                  .format(h4.IP(), scheme), shell=True)
                h3open = h3.popen('iperf -c {0} -p 5001 -t 10 -Z {1}'
                                  .format(h4.IP(), scheme), shell=True)
            else:
                h1open = h1.popen('iperf -c {0} -p 5001 -t 10 '
                                  .format(h4.IP()), shell=True)
                h2open = h2.popen('iperf -c {0} -p 5001 -t 10 '
                                  .format(h4.IP()), shell=True)
                h3open = h3.popen('iperf -c {0} -p 5001 -t 10'
                                  .format(h4.IP()), shell=True)
            h1open.wait()
            h2open.wait()
            h3open.wait()
        elif config == 'b':
            if len(scheme) > 0:
                h1open = h1.popen('iperf -c {0} -p 5001 -t 10 -Z {1}'
                                  .format(h4.IP(), scheme), shell=True)
            else:
                h1open = h1.popen('iperf -c {0} -p 5001 -t 10 '
                                  .format(h4.IP()), shell=True)
            h1open.wait()
        h4open.terminate()
        net.stop()

