/*
 * Please do not edit this file.
 * It was generated using rpcgen.
 */

#include "functions.h"
#include <stdio.h>
#include <stdlib.h>
#include <rpc/pmap_clnt.h>
#include <string.h>
#include <memory.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <syslog.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>

#ifndef SIG_PF
#define SIG_PF void(*)(int)
#endif

static void
service_1_1(struct svc_req *rqstp, register SVCXPRT *transp)
{
	union {
		char *printmsg_1_1_arg;
	} argument;
	char *result;
	xdrproc_t _xdr_argument, _xdr_result;
	char *(*local)(char *, struct svc_req *);

	switch (rqstp->rq_proc) {
	case NULLPROC:
		(void) svc_sendreply (transp, (xdrproc_t) xdr_void, (char *)NULL);
		return;

	case PRINTMSG_1:
		_xdr_argument = (xdrproc_t) xdr_wrapstring;
		_xdr_result = (xdrproc_t) xdr_int;
		local = (char *(*)(char *, struct svc_req *)) printmsg_1_1_svc;
		break;

	default:
		svcerr_noproc (transp);
		return;
	}
	memset ((char *)&argument, 0, sizeof (argument));
	if (!svc_getargs (transp, (xdrproc_t) _xdr_argument, (caddr_t) &argument)) {
		svcerr_decode (transp);
		return;
	}
	result = (*local)((char *)&argument, rqstp);
	if (result != NULL && !svc_sendreply(transp, (xdrproc_t) _xdr_result, result)) {
		svcerr_systemerr (transp);
	}
	if (!svc_freeargs (transp, (xdrproc_t) _xdr_argument, (caddr_t) &argument)) {
		fprintf (stderr, "%s", "unable to free arguments");
		exit (1);
	}
	return;
}

static void
service_2_1(struct svc_req *rqstp, register SVCXPRT *transp)
{
	union {
		char *printmsg_2_1_arg;
	} argument;
	char *result;
	xdrproc_t _xdr_argument, _xdr_result;
	char *(*local)(char *, struct svc_req *);

	switch (rqstp->rq_proc) {
	case NULLPROC:
		(void) svc_sendreply (transp, (xdrproc_t) xdr_void, (char *)NULL);
		return;

	case PRINTMSG_2:
		_xdr_argument = (xdrproc_t) xdr_wrapstring;
		_xdr_result = (xdrproc_t) xdr_int;
		local = (char *(*)(char *, struct svc_req *)) printmsg_2_1_svc;
		break;

	default:
		svcerr_noproc (transp);
		return;
	}
	memset ((char *)&argument, 0, sizeof (argument));
	if (!svc_getargs (transp, (xdrproc_t) _xdr_argument, (caddr_t) &argument)) {
		svcerr_decode (transp);
		return;
	}
	result = (*local)((char *)&argument, rqstp);
	if (result != NULL && !svc_sendreply(transp, (xdrproc_t) _xdr_result, result)) {
		svcerr_systemerr (transp);
	}
	if (!svc_freeargs (transp, (xdrproc_t) _xdr_argument, (caddr_t) &argument)) {
		fprintf (stderr, "%s", "unable to free arguments");
		exit (1);
	}
	return;
}

static void
service_3_1(struct svc_req *rqstp, register SVCXPRT *transp)
{
	union {
		char *printmsg_3_1_arg;
	} argument;
	char *result;
	xdrproc_t _xdr_argument, _xdr_result;
	char *(*local)(char *, struct svc_req *);

	switch (rqstp->rq_proc) {
	case NULLPROC:
		(void) svc_sendreply (transp, (xdrproc_t) xdr_void, (char *)NULL);
		return;

	case PRINTMSG_3:
		_xdr_argument = (xdrproc_t) xdr_wrapstring;
		_xdr_result = (xdrproc_t) xdr_int;
		local = (char *(*)(char *, struct svc_req *)) printmsg_3_1_svc;
		break;

	default:
		svcerr_noproc (transp);
		return;
	}
	memset ((char *)&argument, 0, sizeof (argument));
	if (!svc_getargs (transp, (xdrproc_t) _xdr_argument, (caddr_t) &argument)) {
		svcerr_decode (transp);
		return;
	}
	result = (*local)((char *)&argument, rqstp);
	if (result != NULL && !svc_sendreply(transp, (xdrproc_t) _xdr_result, result)) {
		svcerr_systemerr (transp);
	}
	if (!svc_freeargs (transp, (xdrproc_t) _xdr_argument, (caddr_t) &argument)) {
		fprintf (stderr, "%s", "unable to free arguments");
		exit (1);
	}
	return;
}

//register only one service!
//service name should be in argv
int
main (int argc, char **argv)
{
	register SVCXPRT *transp;
	if(argc != 4) {
		fprintf(stderr, "usage: %s [server name] [service number - 1/2/3] [protocol - udp/tcp/all]\n", argv[0]);
		exit(1);
	}
	char *server;
	char *service;
	char *protocol;


	server = argv[1];
	service = argv[2];
	protocol = argv[3];

	openlog("rpc_client_server", 0, LOG_USER);
	syslog(LOG_INFO, "server [%s] started with service [%s] with protocol [%s]", server, service, protocol);



	if(strcmp(service, "service_1") == 0) {
		pmap_unset (SERVICE_1, PRINTMSG_1);
		syslog(LOG_INFO, "service [%s] mapped", service);
	}
	else if(strcmp(service, "service_2") == 0) {
		pmap_unset (SERVICE_2, PRINTMSG_2);
		syslog(LOG_INFO, "service [%s] mapped", service);
	}
	else if(strcmp(service, "service_3") == 0) {
		pmap_unset (SERVICE_3, PRINTMSG_3);
		syslog(LOG_INFO, "service [%s] mapped", service);
	}

	if((strcmp(protocol, "udp") == 0) || (strcmp(protocol, "all") == 0)) {
		transp = svcudp_create(RPC_ANYSOCK);
		if (transp == NULL) {
			fprintf (stderr, "%s", "cannot create udp service.");
			exit(1);
		}
		if (strcmp(service, "service_1") == 0) {
			if(!svc_register(transp, SERVICE_1, PRINTMSG_1, service_1_1, IPPROTO_UDP)) {
				syslog(LOG_INFO, "Try to regicter service [%s] on UDP", service);
				fprintf (stderr, "%s", "unable to register (SERVICE_1, PRINTMSG_1, udp).");
				exit(1);
			}
		}
		if (strcmp(service, "service_2") == 0) {
			if(!svc_register(transp, SERVICE_2, PRINTMSG_2, service_2_1, IPPROTO_UDP)) {
				syslog(LOG_INFO, "Try to regicter service [%s] on UDP", service);
				fprintf (stderr, "%s", "unable to register (SERVICE_2, PRINTMSG_2, udp).");
				exit(1);
			}
		}
		if (strcmp(service, "service_3") == 0) {
			if(!svc_register(transp, SERVICE_3, PRINTMSG_3, service_3_1, IPPROTO_UDP)) {
				syslog(LOG_INFO, "Try to regicter service [%s] on UDP", service);
				fprintf (stderr, "%s", "unable to register (SERVICE_3, PRINTMSG_3, udp).");
				exit(1);
			}
		}
	}

	if((strcmp(protocol, "tcp") == 0) || (strcmp(protocol, "all") == 0))  {
		transp = svctcp_create(RPC_ANYSOCK, 0, 0);
		if (transp == NULL) {
			fprintf (stderr, "%s", "cannot create tcp service.");
			exit(1);
		}
		if ((strcmp(service, "service_1") == 0)) {
			if(!svc_register(transp, SERVICE_1, PRINTMSG_1, service_1_1, IPPROTO_TCP)) {
				fprintf (stderr, "%s", "unable to register (SERVICE_1, PRINTMSG_1, tcp).");
				exit(1);
			}
		}
		if (strcmp(service, "service_2") == 0) {
			if(!svc_register(transp, SERVICE_2, PRINTMSG_2, service_2_1, IPPROTO_TCP)) {
				fprintf (stderr, "%s", "unable to register (SERVICE_2, PRINTMSG_2, tcp).");
				exit(1);
			}
		}
		if ((strcmp(service, "service_3") == 0)) {
			if(!svc_register(transp, SERVICE_3, PRINTMSG_3, service_3_1, IPPROTO_TCP)) {
				fprintf (stderr, "%s", "unable to register (SERVICE_3, PRINTMSG_3, tcp).");
				exit(1);
			}
		}
	}


	pid_t pid, sid;
	pid = fork();
    if (pid < 0) {
        exit(EXIT_FAILURE);
    }

   	else if (pid > 0) {
        exit(EXIT_SUCCESS);
    }
    else {
    	svc_run ();
		fprintf (stderr, "%s", "svc_run returned");
		exit (1);
	}
	/* NOTREACHED */
}
