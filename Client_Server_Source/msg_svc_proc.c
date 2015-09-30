/* 
* Implementation of remote function
*/
#include <unistd.h>

#include <sys/types.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <arpa/inet.h>


#include <stdio.h>
#include "msg.h"
#include <syslog.h>
#include <stdlib.h>
#include <rpc/pmap_clnt.h>
#include <string.h>
#include <memory.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <syslog.h>

int *
printmessage_1_svc(msg, req)
	char **msg;	
	struct svc_req *req;		/* details of call */
{
	static int result;			/* must be static! */
	openlog("rpc_client_server", 0, LOG_USER);

	int fd;
 	struct ifreq ifr;
	fd = socket(AF_INET, SOCK_DGRAM, 0);

	ifr.ifr_addr.sa_family = AF_INET;
 	strncpy(ifr.ifr_name, "eth0", IFNAMSIZ-1);
	ioctl(fd, SIOCGIFADDR, &ifr);
	close(fd);

	syslog(LOG_INFO, "service_1 on ip %s answered", inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr));

	//syslog(LOG_INFO, "%s", "rpc client is in the remote procedure call");
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
	//syslog(LOG_INFO, "%s", "rpc remote procedure call succeed");
	result = 1;
	return (&result);
}