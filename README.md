# gadget-ekensberg-flight-radar
Tracking nearby flights around Ekensberg using SDR to collect ADS-B data and sending online. 

## Depends on 
1. rtl-sdr
1. dump1090

# Setup osx test environment
Install rtl-sdr using macports (http://www.macports.org/):

`sudo port install rtl-sdr`

Connect your SDR, e.g. R820T2 RTL2832U, and test rtl-sdr:

`rtl_test -t`

Install dump1090 (https://github.com/antirez/dump1090):

`git clone git@github.com:antirez/dump1090.git`

`cd dump1090`

`make`

`./dump1090 --interactive --net --aggressive`


Go to `http://localhost:8080` and find the data at `http://localhost:8080/data.json`
