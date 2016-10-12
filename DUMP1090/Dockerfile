# derive from our baseimage
FROM rtlsdr-baseimage
 
MAINTAINER mik4el
 
WORKDIR /tmp
 
RUN git clone git://github.com/antirez/dump1090.git && \
 cd dump1090 && \
 make
 
WORKDIR /tmp/dump1090
 
ENTRYPOINT ["./dump1090"]
