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

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTgzOTg0NjY3MCwtMTgyMDgxMDUzOSwxNT
kyNDQ1OTA2LDI1OTE4MjE2MCwxODAzODA3ODU2XX0=
-->