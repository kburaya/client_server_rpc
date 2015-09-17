#!/bin/bash

Agents/rpcbind_test.sh ns1 start
Agents/rpcbind_test.sh ns2 start
ip netns exec ns1 Client_Server_Source/rpc_server srv_ns1
ip netns exec ns2 Client_Server_Source/rpc_server srv_ns2
Client_Server_Source/rpc_client 192.168.16.135 "i'm at ns1"
Client_Server_Source/rpc_client 192.168.16.135 "i'm at ns2"
Agents/rpcbind_test.sh ns1 stop
Agents/rpcbind_test.sh ns2 stop