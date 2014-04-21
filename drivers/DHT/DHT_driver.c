//  How to access GPIO registers from C-code on the Raspberry-Pi
//  Example program
//  15-January-2012
//  Dom and Gert
//


// Access from ARM Running Linux

#define BCM2708_PERI_BASE        0x20000000
#define GPIO_BASE                (BCM2708_PERI_BASE + 0x200000) /* GPIO controller */

#include "common.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <dirent.h>
#include <fcntl.h>
#include <assert.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <bcm2835.h>
#include <unistd.h>

#define MAXTIMINGS 100

#define DHT11 11
#define DHT22 22
#define AM2302 22

int bits[250], data[100];
int bitidx = 0;

DHTResult readDHT(int type, int pin) {
 int counter = 0;
 int laststate = HIGH;
 int j=0;
 int i=0;
 // Set GPIO pin to output
 bcm2835_gpio_fsel(pin, BCM2835_GPIO_FSEL_OUTP);
 bcm2835_gpio_write(pin, HIGH);
 usleep(100);
 bcm2835_gpio_write(pin, LOW);
 usleep(20000);
 bcm2835_gpio_fsel(pin, BCM2835_GPIO_FSEL_INPT);

 data[0] = data[1] = data[2] = data[3] = data[4] = 0;
 // read data!

 for (i=0; i< MAXTIMINGS; i++) {
    counter = 0;
    while ( bcm2835_gpio_lev(pin) == laststate) {
       counter++;
       nanosleep(1);           // overclocking might change this?
       if (counter == 100)
         break;
    }
    laststate = bcm2835_gpio_lev(pin);
    if (counter == 100) break;
    bits[bitidx++] = counter;

    if ((i>3) && (i%2 == 0)) {
     // shove each bit into the storage bytes
     data[j/8] <<= 1;
     if (counter > 16)
       data[j/8] |= 1;
     j++;
    }
 }


       DHTResult r;
 if ((j >= 39) && (data[4] == ((data[0] + data[1] + data[2] + data[3]) & 0xFF)) ) {
    if (type == DHT11) {
	r.temp = data[2];
	r.hum = data[0];
    }
    if (type == DHT22) {
       float f, h;
       h = data[0] * 256 + data[1];
       printf ("%s\n",h);
       h /= 10;

       f = (data[2] & 0x7F)* 256 + data[3];
       f /= 10.0;
       if (data[2] & 0x80)  f *= -1;
       r.temp = f;
       r.hum = h;
    }
}
else {
       r.temp = -1.;
       r.hum = -1.;
}
       return r;
}
