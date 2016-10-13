# gadget-ekensberg-flight-radar
Tracking nearby flights around Ekensberg using SDR to collect ADS-B data and sending online. 

## Depends on 
1. rtl-sdr
1. dump1090
1. python3
1. Docker, Docker-compose

## Suggested hardware
Hardware needed is a SDR stick (e.g. RTL2832U from http://www.rtl-sdr.com/), an antenna (an antenna made for 1090 MHz is significantly better, i.e. you will receive more data, than just the standard tv antenna that ships with most sdr dongles) and a computer, tested with OS X and a raspberry pi 1 mod b.

# Get started

## Setup osx test environment
Install rtl-sdr using macports (http://www.macports.org/):

`sudo port install rtl-sdr`

Connect your SDR, e.g. R820T2 RTL2832U, and test rtl-sdr:

`rtl_test -t`

Install dump1090 (https://github.com/antirez/dump1090):

1. `git clone git@github.com:antirez/dump1090.git`
1. `cd dump1090`
1. `make`
1. `./dump1090 --interactive --net --aggressive`
1. Go to `http://localhost:8080` and find the data at `http://localhost:8080/data.json`

## Setup raspi test environment
Install rtl-sdr on your raspi:

1. `sudo apt-get install -y cmake pkg-config libusb-1.0`
1. `git clone git://git.osmocom.org/rtl-sdr.git`
1. `cd rtl-sdr/`
1. `mkdir build`
1. `cd build`
1. `cmake ../ -DINSTALL_UDEV_RULES=ON`
1. `make`
1. `sudo make install`
1. `sudo ldconfig`

Make sure no other drivers are loaded for your sdr dongle:

1. `sudo vi /etc/modprobe.d/raspi-blacklist.conf`
1. Add these lines and save:
```
blacklist dvb_usb_rtl28xxu
blacklist rtl2832
blacklist rtl2830
```
1. Reboot 
1. Connect your sdr dongle and test it with `rtl_test -t`
1. Install 1090 by following the same steps above.

## Setup data poster
1. `git clone <this repo>`
1. Make a copy of `.env.sample` as `.env` and fill in exports
1. `source .env`
1. `python -m poster.post_data.py`

## Setup raspi for Docker
Use a raspi 3 for more punch and built in wifi, probably works with earlier raspis to.

1. Get jessie lite from https://www.raspberrypi.org/downloads/raspbian/ and write to sd-card.
1. Follow e.g this guide http://blog.alexellis.io/getting-started-with-docker-on-raspberry-pi/
1. Install `docker-compose` following https://github.com/hypriot/arm-compose
1. Add wifi access using e.g. https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
1. Add your local ssh key:
    ```
    mkdir .ssh
    touch .ssh/authorized_keys
    sudo nano ~/.ssh/authorized_keys
    ```
1. Fix for local ssh config, so you can `ssh pi-name`:
    ```
    Host pi-name
     HostName pi-name.local
     User pi
     PreferredAuthentications publickey
    ```
1. Install byobu for easier terminal over ssh `sudo apt-get install byobu`.
1. Make sure no other drivers are used:
    ```
    sudo vi /etc/modprobe.d/raspi-blacklist.conf
    ```
1. Add these lines:
    ```
    blacklist dvb_usb_rtl28xxu
    blacklist rtl2832
    blacklist rtl2830
    ```
1. Get this repo `git clone <repo url>`
1. Make a copy `.env` of `.env.sample` and fill in. 
1. `docker-compose up`

# Todos
1. Describe example antenna
