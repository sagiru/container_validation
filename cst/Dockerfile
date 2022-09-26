FROM httpd:2.4.53

ENV VERSION=2.4.53

LABEL kostenstelle=zuTeuer0815

RUN mkdir /etc/apache2/ && \
    ln -s /usr/local/apache2/conf/httpd.conf /etc/apache2/

RUN chown www-data /usr/local/apache2/logs

RUN sed -i 's/^Listen 80$/Listen 8080\n/g' /usr/local/apache2/conf/httpd.conf

EXPOSE 8080

USER www-data
