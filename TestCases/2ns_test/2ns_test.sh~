#default configs
#ns1 - 192.168.16.135
#ns2 - 192.168.16.136

#run service_1 in each ns
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1 service_1 tcp
sleep 2
ip netns exec ns2 ./CLI_SERV_SOURCE/rpc_server srv_ns2 service_1 tcp
sleep 2

#test connection
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_1 "client from ns1 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"

#run service_2 in each ns
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1 service_2 tcp
sleep 2
ip netns exec ns2 ./CLI_SERV_SOURCE/rpc_server srv_ns2 service_2 tcp
sleep 2

#test connection
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_1 "client from ns1 - service_2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_2"

#stop
./Agents/nsconfig.sh ns1 stop
./Agents/nsconfig.sh ns2 stop