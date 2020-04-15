# HAProxy Data Plane API Configuration
This document covers configuration and basic usage of the HAProxy Data Plane API on Red Hat Enterprise Linux and Fedora distributions and is intended as a supplement to the [README.md](README.md) file.  The prerequisite for using this document is that HAProxy has already been configured and has been started.

## Configure dataplaneapi user
The Data Plane API requires basic authentication such that any user invoking methods must provide valid credentials.
Usernames and passwords are stored in the HAProxy configuration file inside a top-level **userlist** section.

<!--stackedit_data:
eyJoaXN0b3J5IjpbMTA1NDY4OTIyOCwxNTkyNDQ1OTA2LDI1OT
E4MjE2MCwxODAzODA3ODU2XX0=
-->