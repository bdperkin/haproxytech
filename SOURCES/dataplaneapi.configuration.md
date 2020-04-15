# HAProxy Data Plane API Configuration
This document covers configuration and basic usage of the HAProxy Data Plane API on Red Hat Enterprise Linux and Fedora distributions and is intended as a supplement to the [README.md](README.md) file.  The prerequisite for using this document is that HAProxy has already been configured and has been started.

## General Data Plane API configuration
The system configuration file can be found at **/etc/sysconfig/dataplaneapi**.  Please review this file, especially for the **PORT** and **USERLIST** values to make sure they will work in your environment.

## Configure dataplaneapi user
The Data Plane API requires basic authentication such that any user invoking methods must provide valid credentials.
Usernames and passwords are stored in the HAProxy configuration file inside a top-level **userlist** section.

 - Add the following to the HAProxy configuration file
   **/etc/haproxy/haproxy.cfg** where the **userlist** value matches the **USERLIST** value from **/etc/sysconfig/dataplaneapi**:

       userlist dataplaneapi
           user dataplaneapi insecure-password mypassword

 - Change the ***user*** and ***insecure-password*** values to those of your choice.  You may also add additional ***user*** lines.
 - It is suggested to use an encrypted password instead of an insecure plain text password.  To generate an encrypted password, install the **mkpasswd** package and then run the following command:


       $ mkpasswd -m sha-256 mypassword
       $5$2yEnDhzXwNRisHxR$NvzzvO85Sw1D0.cjeIu8ZXmzjx9ibGjFfFmbQhq.Su/
       
 - If using an encrypted password, copy the output from the last step and paste the value into the configuration file while also changing ***insecure-password*** to ***password***:

       userlist dataplaneapi
           user dataplaneapi password $5$2yEnDhzXwNRisHxR$NvzzvO85Sw1D0.cjeIu8ZXmzjx9ibGjFfFmbQhq.Su/

There is no need to restart HAProxy for changes to the **userlist** section.  The Data Plane API runs as its own process which allows it to write and reload the HAProxy configuration as needed.

## Configure HAProxy socket
The Data Plane API requires read and write access to the HAProxy socket to function.
Socket specification is stored in the HAProxy configuration file inside the top-level **global** section.

 - Add the following to the HAProxy configuration file
   **/etc/haproxy/haproxy.cfg**:


       global
           stats socket /var/run/haproxy.sock user haproxy group haproxy mode 660 level admin

Restart HAProxy so the socket can be created.

## Enable and start the Data Plane API service
 - To enable the **dataplaneapi** service unit, so that it starts on system boot, run the following command (also make sure the haproxy service is enabled):


       $ sudo systemctl enable dataplaneapi.service
       Created symlink /etc/systemd/system/multi-user.target.wants/dataplaneapi.service → /usr/lib/systemd/system/dataplaneapi.service.
       $ sudo systemctl is-enabled haproxy.service
       enabled

 - To start the **dataplaneapi** service unit run the following command (also make sure the haproxy service is active):


       $ sudo systemctl start dataplaneapi.service
       $ sudo systemctl is-active haproxy.service
       active



<!--stackedit_data:
eyJoaXN0b3J5IjpbMTQ4MjExNjE4NywtMTgyMDgxMDUzOSwxNT
kyNDQ1OTA2LDI1OTE4MjE2MCwxODAzODA3ODU2XX0=
-->