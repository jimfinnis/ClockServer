/**
 * @file main.cpp
 * @brief  Brief description of file.
 *
 */

#include <iostream>
#include <exception>

#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <time.h>
#include <termios.h>
#include <sys/ioctl.h>
#include <sys/select.h>
#include <unistd.h>
#include <stdarg.h>
#include <time.h>


class connectexception : public std::exception {
    const char *msg;
public:
    connectexception(const char *s) : msg(s) {}
    
    virtual const char *what() const throw() {
        return msg;
    }
};


class Comms {
private:
    int fd;
public:
    Comms() : fd(-1)  {
        const char *dev = "/dev/ttyACM0";
        int br = B115200;
        try {
            // read/write, not controlling terminal
            fd = open(dev,O_RDWR,O_NOCTTY);
            if(fd==-1){
                throw connectexception("cannot open");
            }
            
            // drop DTR to reset the Arduino! Ugh.
            int st;
            ioctl(fd, TIOCMGET, &st);
            st &= ~TIOCM_DTR;
            ioctl(fd, TIOCMSET, &st);
            struct timespec qqq={0,10000000};
            nanosleep(&qqq,NULL);
            st |= TIOCM_DTR;
            ioctl(fd, TIOCMSET, &st);
            
            if(fcntl(fd,F_SETFL,0)<0){
                throw connectexception("cannot fcntl");
            }
            
            
            struct termios options;
            if(tcgetattr(fd,&options)<0){
                throw(connectexception("cannot get terminal options"));
            }
            
            if(cfsetispeed(&options, br) < 0 || cfsetospeed(&options, br) < 0) {
                throw connectexception("Cannot set baud");
            }
            if(tcsetattr(fd, TCSAFLUSH, &options) < 0){
                throw connectexception("Cannot set options");
            }
        }
        catch(std::exception &e){
            perror(e.what());
            if(fd>=0){
                close(fd);
                fd=-1;
            }
        }
    }
    
    ~Comms(){
        if(fd>=0){
            close(fd);
            fd=-1;
        }
    }        
    
    void send(const char *s){
        try {
            write(fd,s,strlen(s));
        } catch(std::exception &e){
            perror(e.what());
            if(fd>=0){
                close(fd);
                fd=-1;
            }
        }
    }
};


int main(int argc,char *argv[]){
    Comms c;
    
    int i=0;
    for(;;){
        char buf[120],tbuf[100];
        sleep(2);
        
        time_t t;
        time(&t);
        strftime(tbuf,sizeof(tbuf),":L*:w*%H:%M*:M*:g*%a %e %b",localtime(&t));
        sprintf(buf,"%s\n",tbuf);
        puts(buf);
        c.send(buf);
    }
}
    
