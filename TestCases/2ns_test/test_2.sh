#default configs
#ns1 - 192.168.16.135
#ns2 - 192.168.16.136
#success test

python Agents/StorageArray.py -c Configs/StorageArray_2ns.xml


echo "Run service1 in NS 1, 2"
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1 service_1 $1
sleep 2
ip netns exec ns2 ./CLI_SERV_SOURCE/rpc_server srv_ns2 service_1 $1
sleep 2

echo "Test connections: ns1 - service1, ns2 - service1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_1 "client from ns1 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"

echo "Run service2 in NS 1"
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1_1 service_2 $1
sleep 2

echo "Test connections: ns1 - service1, ns2 - service1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_1 "client from ns1 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"
echo "Test connections: ns1 - service2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"


echo "Run service3 in NS 1"
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1_2 service_3 $1
sleep 2


echo "Test connections: ns1 - service1, ns2 - service1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_1 "client from ns1 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"
echo "Test connections: ns1 - service2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"
echo "Test connections: ns1 - service3"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"


#stop
echo "End test, stop everything"
./Agents/nsconfig.sh ns1 stop
./Agents/nsconfig.sh ns2 stop

echo "Delete configuration"
ip link del brns1
ip link del brns2