/* 
* Implementation of remote function
*/

#include <stdio.h>
#include "msg.h"
#include <syslog.h>

int *
printmessage_1_svc(msg, req)
	char **msg;	
	struct svc_req *req;		/* details of call */
{
	static int result;			/* must be static! */
	openlog("rpc_client_server", 0, LOG_USER);
	syslog(LOG_INFO, "%s", "rpc client is in the remote procedure call");
	FILE *file;
	file = fopen("/tmp/rpc_client_server.log", "a");
	if (file == (FILE *)NULL) {
		syslog(LOG_INFO, "%s", "can't open file in the remote procedure call, aborting");
		result = 0;
		return (&result);
	}
	fputs("rpc client message delivered, success\n", file);
	fprintf(file, "%s\n", *msg);
	fclose(file);
	syslog(LOG_INFO, "%s", "rpc remote procedure call succeed");
	result = 1;
	return (&result);
}