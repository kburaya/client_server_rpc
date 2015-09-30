/* 
* Implementation of remote function
*/

#include <stdio.h>
#include "functions.h"
#include <syslog.h>

int *
printmsg_1_1_svc(msg, req)
	char **msg;	
	struct svc_req *req;		/* details of call */
{
	static int result;			/* must be static! */
	openlog("rpc_service_1", 0, LOG_USER);
	syslog(LOG_INFO, "%s", "rpc client is in the remote procedure call");
	FILE *file;
	file = fopen("/tmp/rpc_service_1.log", "a");
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

int *
printmsg_2_1_svc(msg, req)
	char **msg;	
	struct svc_req *req;		/* details of call */
{
	static int result;			/* must be static! */
	openlog("rpc_service_2", 0, LOG_USER);
	syslog(LOG_INFO, "%s", "rpc client is in the remote procedure call");
	FILE *file;
	file = fopen("/tmp/rpc_service_2.log", "a");
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

int *
printmsg_3_1_svc(msg, req)
	char **msg;	
	struct svc_req *req;		/* details of call */
{
	static int result;			/* must be static! */
	openlog("rpc_service_3", 0, LOG_USER);
	syslog(LOG_INFO, "%s", "rpc client is in the remote procedure call");
	FILE *file;
	file = fopen("/tmp/rpc_service_3.log", "a");
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