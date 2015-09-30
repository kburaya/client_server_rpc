#!/bin/bash

ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srvns1 service_1 &
sleep 3
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_1 "agent1 to service_1 from srvns1"
ip netns exec ns1 rpcinfo -s

ip netns exec ns2 ./CLI_SERV_SOURCE/rpc_server srvns2 service_2 &
sleep 3
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_2 "agent2 to service_2 from srvns2"
ip netns exec ns2 rpcinfo -s

ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srvns3 service_3 &
sleep 3
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_3 "agent3 to service_3 from srvns3"
ip netns exec ns1 rpcinfo -s

./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_1 "agent1 to service_1 from srvns1"

./Agents/nsconfig.sh ns1 stop
./Agents/nsconfig.sh ns2 stop