.SUFFIXES:
.SUFFIXES: .c .o
CLNT = rpc_client
SRVR = rpc_server
CFLAGS = -g -Wall

SRVR_OBJ = msg_svc_proc.o msg_svc.o
CLNT_OBJ = msg.o msg_clnt.o

.c.o:; gcc -c -o $@ $(CFLAGS) $<

default: $(CLNT) $(SRVR)

$(CLNT): $(CLNT_OBJ) msg.h
	gcc -o $(CLNT) $(CLNT_OBJ)

$(SRVR): $(SRVR_OBJ) msg.h
	gcc -o $(SRVR) $(SRVR_OBJ)

clean:
	rm *.o $(CLNT) $(SRVR)
	rm -i *~
	rm core