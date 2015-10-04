#default configs
#ns1 - 192.168.16.135
#ns2 - 192.168.16.136
#ns3 - 192.168.16.137


#run service_1 in each ns
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1 service_1 tcp
sleep 2
ip netns exec ns2 ./CLI_SERV_SOURCE/rpc_server srv_ns2 service_1 tcp
sleep 2
ip netns exec ns3 ./CLI_SERV_SOURCE/rpc_server srv_ns3 service_1 tcp
sleep 2


#test connection
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_1 "client from ns1 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.137 service_1 "client from ns3 - service_1"

#stop rpcbind in ns1
./Agents/nsconfig.sh ns1 stop
ip link del brns1

#test connection
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.137 service_1 "client from ns3 - service_1"

#add ns1
ip netns add ns1
python Agents/vethconf.py -ns ns1 192.168.16.135
./Agents/nsconfig.sh ns1 start

#run service_2 in ns1
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1 service_2 tcp
sleep 2

#test connection
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"

#run service_3 in ns1
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1 service_3 tcp
sleep 2
#test connection
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_3"


#stop rpcbind in ns2
./Agents/nsconfig.sh ns2 stop
ip link del brns2

#add ns2
ip netns add ns2
python Agents/vethconf.py -ns ns2 192.168.16.136
./Agents/nsconfig.sh ns2 start

#run service_1 in ns2
./CLI_SERV_SOURCE/rpc_server srv_ns2 service_1 tcp
sleep 2

#check all connections
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_3 "client from ns1 - service_3"

./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"

./CLI_SERV_SOURCE/rpc_client 192.168.16.137 service_1 "client from ns3 - service_1"


#end test
pkill rpc_server
./Agents/nsconfig.sh ns1 stop
./Agents/nsconfig.sh ns2 stop
./Agents/nsconfig.sh ns3 stop