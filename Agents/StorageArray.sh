#!/bin/bash

sudo ./Agents/rpcbind_test.sh ns1 start
#sudo ./Agents/rpcbind_test.sh ns2 start

sudo ip netns exec ns1 ./Client_Server_Source/rpc_server srv_ns1 &
#sudo ip netns exec ns2 ./Client_Server_Source/rpc_server srv_ns2 &

sudo ./Client_Server_Source/rpc_client 192.168.16.135 "i'm at ns1"
#./Client_Server_Source/rpc_client 192.168.16.136 "i'm at ns2"

sudo ./Agents/rpcbind_test.sh ns1 stop
#sudo ./Agents/rpcbind_test.sh ns2 stop