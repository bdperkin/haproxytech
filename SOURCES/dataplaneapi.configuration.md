# HAProxy Data Plane API Configuration
This document covers configuration and basic usage of the HAProxy Data Plane API on Red Hat Enterprise Linux and Fedora distributions and is intended as a supplement to the [README.md](README.md) file.  The prerequisite for using this document is that HAProxy has already been configured and has been started.

## General Data Plane API configuration
The system configuration file can be found at **/etc/sysconfig/dataplaneapi**.  Please review this file, especially for the PORT, USERLIST
## Configure dataplaneapi user
The Data Plane API requires basic authentication such that any user invoking methods must provide valid credentials.
Usernames and passwords are stored in the HAProxy configuration file inside a top-level **userlist** section.

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTAzNjY2MTkzLDE1OTI0NDU5MDYsMjU5MT
gyMTYwLDE4MDM4MDc4NTZdfQ==
-->