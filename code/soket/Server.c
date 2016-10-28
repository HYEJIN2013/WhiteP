#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <signal.h>
#include <unistd.h>
#include <fcntl.h>

int main(int argc, char **argv) {

    fd_set fds, readfds;
    int i, clientaddrlen, j;
    int rval;
    char buffer[256];
    char temp[256];
    char names[5][256] = {"NULL", "NULL", "NULL", "NULL", "NULL"};
    struct timeval timeout;
    int clientsock[5], rc, numsocks = 0, maxsocks = 5;

    //User probably didn't enter a port numer
    if(argc < 2){
        printf("Usage: %s port\n", argv[0]);
        exit(1);
    }

    int serversock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (serversock == -1) perror("Socket ERROR");

    struct sockaddr_in serveraddr, clientaddr;  
    bzero(&serveraddr, sizeof(struct sockaddr_in));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_addr.s_addr = INADDR_ANY;
    serveraddr.sin_port = htons(atoi(argv[1]));

    if (-1 == bind(serversock, (struct sockaddr *)&serveraddr, sizeof(struct sockaddr_in))) perror("Binding ERROR");
    
    if (-1 == listen(serversock, 5)) perror("Listening ERROR");

    FD_ZERO(&fds);
    FD_SET(serversock, &fds);

    int bits;
    bits = fcntl(socket, F_GETFL);
    bits = bits | O_NONBLOCK;
    fcntl(serversock, F_SETFL, bits);

    while(1){

        timeout.tv_sec = 1;
        timeout.tv_usec = 50000;

        readfds = fds;
        rc = select(FD_SETSIZE, &readfds, NULL, NULL, &timeout);

        //Oh NOOOOOO...AN ERROR!!!!!!
        if(rc < 0){
            perror("Select Error");
            break;
        }
        
        //Nothing is happeing, print something to show that process is running correctly
        if(rc == 0){
            printf(".");
            fflush(stdout);
        }

        else for(i=0; i<FD_SETSIZE; i++){
            if(FD_ISSET(i, &readfds)){ //receiving something
                if(i == serversock){
                    if(numsocks < maxsocks){ //Add a new client that is trying to connect if there is still space
                        clientsock[numsocks] = accept(serversock, (struct sockaddr *) &clientaddr, (socklen_t *) &clientaddrlen);
                        if(clientsock[numsocks] < 0) perror("Accept error");
                        FD_SET(clientsock[numsocks], &fds);
                        if((send(clientsock[numsocks], "Please enter a name:\n", 25, 0)) < 0) perror("Error sending stream message\n");
                        printf("\nNew Client %d\n", numsocks);
                        numsocks++;
                    } else{
                        printf("\nRan out of socket space\n");
                        break;
                      }
                    
                } else{
                    bzero(buffer, 256);
                    if((rval = read(i, buffer, 256)) < 0) perror("Error reading stream message\n");
                    buffer[strlen(buffer)-1] = '\0';
                    //The client wants to exit the chat
                    if(strcmp(buffer, "exit") == 0){
                        printf("\nexit command received for user %s\n", names[i-4]);
                        printf("The value of the socket is: %d\n", clientsock[i-4]);
                         if((send(clientsock[i-4], "exit", 256, 0)) < 0) perror("Error sending stream message\n"); 
                        FD_CLR(clientsock[i-4], &fds);                       
                        //IMPLEMENT THIS DUDE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    }
                    //Receiving a name for a newly made client
                    else {if(strcmp(names[i-4], "NULL") == 0){
                        strcpy(names[i-4], buffer);
                        //names[i-4][strlen(names[i-4])-1] = '\0';
                        strcpy(temp, "User name assigned as: ");
                        strcat(temp, names[i-4]);
                        if(send(clientsock[i-4], temp, 256, 0) < 0) perror("ERROR sending\n");
                    }
                    //Receiving a message to be transmitted from an existing client
                    else{
                        printf("\nTransmitting message for: %s\n", names[i-4]);
                        temp[0] = '\0';
                        strcat(temp, names[i-4]);
                        strcat(temp, ": ");
                        strcat(temp, buffer);
                        for(j=0; j<numsocks; j++){
                            printf("j is: %d\n", j);
                                if(j+4 != i)
                                    if((send(clientsock[j], temp, 256, 0)) < 0) perror("Error sending stream message\n");
                        }
                    }
                    }
                }
            }
        }
    }
 
    close(serversock);
    return 0;
}