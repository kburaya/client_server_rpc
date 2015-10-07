#default configs
#ns1 - 192.168.16.135
#ns2 - 192.168.16.136
#ns3 - 192.168.16.137


echo "Start service1 in ns1,2,3"
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1 service_1 tcp
sleep 2
ip netns exec ns2 ./CLI_SERV_SOURCE/rpc_server srv_ns2 service_1 tcp
sleep 2
ip netns exec ns3 ./CLI_SERV_SOURCE/rpc_server srv_ns3 service_1 tcp
sleep 2


echo "Test connections: ns1 - service1, ns2 - service1, ns3 - service1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_1 "client from ns1 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.137 service_1 "client from ns3 - service_1"

echo "Stop ns1"
./Agents/nsconfig.sh ns1 stop
ip link del brns1

echo "Test connections: ns2 - service1, ns3 - service1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.137 service_1 "client from ns3 - service_1"

echo "Add ns1 + run rpcbind"
ip netns add ns1
python Agents/vethconf.py -ns ns1 192.168.16.135
./Agents/nsconfig.sh ns1 start

echo "Run service_2 in ns1"
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1 service_2 tcp
sleep 2

echo "Test connections: ns1 - service2, ns2 - service1, ns3 - service1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.137 service_1 "client from ns3 - service_1"

echo "Run service_3 in ns1"
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1 service_3 tcp
sleep 2

echo "Test connections: ns1 - service2, ns1 - service3, ns2 - service1, ns3 - service1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_3 "client from ns1 - service_3"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.137 service_1 "client from ns3 - service_1"


echo "Stop ns2"
./Agents/nsconfig.sh ns2 stop
ip link del brns2

echo "Test connections: ns1 - service2, ns1 - service3, ns3 - service1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_3 "client from ns1 - service_3"
./CLI_SERV_SOURCE/rpc_client 192.168.16.137 service_1 "client from ns3 - service_1"

echo "Add ns2 + run rpcbind"
ip netns add ns2
python Agents/vethconf.py -ns ns2 192.168.16.136
./Agents/nsconfig.sh ns2 start


echo "Run service_1 in ns2"
ip netns exec ns2 ./CLI_SERV_SOURCE/rpc_server srv_ns2 service_1 tcp
sleep 2

echo "Test connections: ns1 - service2, ns1 - service3, ns2 - service2, ns3 - service1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_3 "client from ns1 - service_3"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.137 service_1 "client from ns3 - service_1"

echo "End test"

pkill rpc_server
./Agents/nsconfig.sh ns1 stop
./Agents/nsconfig.sh ns2 stop
./Agents/nsconfig.sh ns3 stop
