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

echo "Test connections: ns1 - service1, ns2 - servive"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_1 "client from ns1 - service_1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"

#stop rpcbind in ns 1 and delete ns1
echo "Stop rpcbind in ns1 and delete ns1"
./Agents/nsconfig.sh ns1 stop
ip link del brns1

echo "Test connections: ns2 - service1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"

echo "Start rpcbin in ns1"
ip netns add ns1
python Agents/vethconf.py -ns ns1 192.168.16.135
./Agents/nsconfig.sh ns1 start

echo "Start service2 in ns1"
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1 service_2 $1
sleep 2

echo "Test connections: ns1 - service2, ns2 - service1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"

echo "Run service3 in ns1"
ip netns exec ns1 ./CLI_SERV_SOURCE/rpc_server srv_ns1 service_3 $1
sleep 2

echo "Test connections: ns1 - service2, ns1 - service3, ns2 - service1"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_3 "client from ns1 - service_3"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_1 "client from ns2 - service_1"

echo "Stop rpcbind in ns2 and delete ns2"
./Agents/nsconfig.sh ns2 stop
ip link del brns2

echo "Test connections: ns1 - service2, ns2 - service3"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_3"

echo "Start rpcbind in ns2"
ip netns add ns2
python Agents/vethconf.py -ns ns2 192.168.16.136
./Agents/nsconfig.sh ns2 start

echo "Run service2 in ns2"
ip netns exec ns2 ./CLI_SERV_SOURCE/rpc_server srv_ns2 service_2 $1 

echo "Test connections: ns1 - service2, ns1 - service3, ns2 - service2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_2 "client from ns1 - service_2"
./CLI_SERV_SOURCE/rpc_client 192.168.16.135 service_3 "client from ns1 - service_3"
./CLI_SERV_SOURCE/rpc_client 192.168.16.136 service_2 "client from ns2 - service_2"

#stop
echo "End test, stop everything"
./Agents/nsconfig.sh ns1 stop
./Agents/nsconfig.sh ns2 stop

echo "Delete configuration"
ip link del brns1
ip link del brns2