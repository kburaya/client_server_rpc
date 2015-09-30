.SUFFIXES:
.SUFFIXES: .c .o
CLNT = rpc_client
SRVR = rpc_server
CFLAGS = -g -Wall

SRVR_OBJ = functions_svc_proc.o functions_svc.o
CLNT_OBJ = functions.o functions_clnt.o

.c.o:; gcc -c -o $@ $(CFLAGS) $<

default: $(CLNT) $(SRVR)

$(CLNT): $(CLNT_OBJ) functions.h
	gcc -o $(CLNT) $(CLNT_OBJ)

$(SRVR): $(SRVR_OBJ) functions.h
	gcc -o $(SRVR) $(SRVR_OBJ)

clean:
	rm *.o $(CLNT) $(SRVR)
	rm -i *~
	rm core