#!/bin/bash

ip netns exec ns1 ./Client_Server_Source/rpc_server srvns1 &
sleep 3
./Client_Server_Source/rpc_client 192.168.16.135 "agent1 to srvns1"

ip netns exec ns2 ./Client_Server_Source/rpc_server srvns2 &
sleep 3
./Client_Server_Source/rpc_client 192.168.16.136 "agent2 to srvns2"

ip netns exec ns1 ./Client_Server_Source/rpc_server srvns3 &
sleep 3
./Client_Server_Source/rpc_client 192.168.16.135 "agent1 to srvns3"

./Agents/nsconfig.sh ns1 stop
./Agents/nsconfig.sh ns2 stop