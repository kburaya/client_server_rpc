/*
	REMOTE VERSION OF FUNCTION
 */
#include <stdio.h>
#include <syslog.h>
#include "msg.h"			/* msg.h generated by rpcgen */
 
main(argc, argv)
	int argc;
	char *argv[];
{
	CLIENT *clnt;
	int *result;
	char *server;
	char *message;
 
	if (argc != 3) {
		fprintf(stderr, "usage: %s host message\n", argv[0]);
		exit(1);
	}
 
	server = argv[1];
	message = argv[2];
	
	openlog("rpc_client_server", 0, LOG_USER);
	syslog(LOG_INFO, "connection to server %s", server);
	syslog(LOG_INFO, "client message is %s", message);


	clnt = clnt_create(server, MESSAGEPROG, PRINTMESSAGETOCONSOLE, "tcp");
	if (clnt == (CLIENT *)NULL) {
		syslog(LOG_INFO, "could't establish connection with server %s, aborting", server);
		clnt_pcreateerror(server);
		exit(1);
	}
	
	//remote procedure call
	result = printmessage_1(&message, clnt);
	if (result == (int *)NULL) {
		syslog(LOG_INFO, "an error occured while calling the server, aborting");
		clnt_perror(clnt, server);
		exit(1);
	}
	if (*result == 0) {
		fprintf(stderr,"%s: could not print your message\n",argv[0]);
		exit(1);
	}

 	syslog(LOG_INFO, "message successfully delivered to server %s", server);
	clnt_destroy( clnt );
	exit(0);
}