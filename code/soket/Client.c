#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <fcntl.h>

int main(int argc, char **argv) {

    int portno, sel, i, rc;
    fd_set writefds, readfds, backupwritefds, backupreadfds;
    char buffer[256];
    struct hostent *server;

    if(argc < 3){
        printf("Usage: %s hostname port\n", argv[0]);
        exit(1);
    }

    portno = atoi(argv[2]);
    server = gethostbyname(argv[1]);
    if(server == NULL){
        fprintf(stderr, "ERROR, no such host\n");
        exit(0);
    }

    struct sockaddr_in servaddr;
    struct timeval timeout;
    int sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);

    if (sock == -1) perror("Socket");

    bzero((void *) &servaddr, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(portno);
    bcopy((char *)server->h_addr, (char *)&servaddr.sin_addr.s_addr, server->h_length);

    if (-1 == connect(sock, (struct sockaddr *)&servaddr, sizeof(servaddr))){
        perror("Connect");
        exit(1);
    }
    //if (ioctlsocket(sock, FIONBIO, &nonblocking) != 0) perror("Blocking");

    printf("Connected to Server!\n");

    FD_ZERO(&backupreadfds);
    FD_ZERO(&readfds);
    FD_SET(sock, &readfds);
    FD_SET(0, &readfds);

    sel = 0;

    int bits;
    bits = fcntl(sock, F_GETFL);
    bits = bits | O_NONBLOCK;
    fcntl(sock, F_SETFL, bits);

    while(1){

        timeout.tv_sec = 1;
        timeout.tv_usec = 50000;

        backupreadfds = readfds;
        sel = select(FD_SETSIZE, &backupreadfds, NULL, NULL, &timeout);

        if(sel < 0){
            perror("Select Error");
            break;
        }

        if(sel > 0){
            if(FD_ISSET(sock, &backupreadfds)){
                if(recv(sock, buffer, 256, 0) < 0) perror("ERROR recv\n");
                if(strcmp(buffer, "exit") == 0){
                    printf("You are the weakest link, goodbye.\n");
                    break;
                }
                printf("--------> %s\n", buffer);    
            }
            if(FD_ISSET(0, &backupreadfds)){
                fgets(buffer, 256, stdin);
                buffer[255] = '\0';
                send(sock, buffer, 256, 0);
            }        
        }    
    }
    close(sock);
    return 0;
}