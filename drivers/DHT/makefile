all: readDHT.a pyDHT.cpp
	g++ -shared -o pyDHT.so -l:readDHT.a -lbcm2835 -lrt -lboost_python -lpython2.7 -I/usr/include/python2.7/ pyDHT.cpp

readDHT.a: DHT_driver.c
	gcc -c -o readDHT.a DHT_driver.c

clean:
	rm -f pyDHT.so readDHT.a 
