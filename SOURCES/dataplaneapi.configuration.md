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
 - It is suggested to use an encrypted password instead of an insecure plain text password.  Supported algorithms are: MD5, SHA-256, and SHA-512.  To generate a SHA-256 encrypted password, install the **mkpasswd** package and then run the following command:


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
 - To enable the **dataplaneapi** service unit, so that it starts on system boot, run the following command (also make sure the **haproxy** service is enabled):


       $ sudo systemctl enable dataplaneapi.service
       Created symlink /etc/systemd/system/multi-user.target.wants/dataplaneapi.service → /usr/lib/systemd/system/dataplaneapi.service.
       $ sudo systemctl is-enabled haproxy.service
       enabled

 - To start the **dataplaneapi** service unit run the following command (also make sure the **haproxy** service is active):


       $ sudo systemctl start dataplaneapi.service
       $ sudo systemctl is-active haproxy.service
       active

## Test that the Data Plane API is running properly
Basic testing can be performed by using the **curl** command found in the **curl** package.  It is also suggested to install the **python3-libs** package so that the **json.tool** can be used to validate and pretty-print the JSON responses.
The "root" of the API is at **/v1**.  The most basic test that can be performed is to get that path:

    $ curl -H "Content-Type: application/json" -X GET -S -s -u dataplaneapi:mypassword "http://localhost:5555/v1/" | python3 -m json.tool
    [
        {
            "description": "Return Data Plane API OpenAPI specification",
            "title": "Data Plane API Specification",
            "url": "/specification"
        },
        {
            "description": "Returns a list of API managed services endpoints.",
            "title": "Return list of service endpoints",
            "url": "/services"
        },
        {
            "description": "Return API, hardware and OS information",
            "title": "Return API, hardware and OS information",
            "url": "/info"
        }
    ]

Next, call the **/services/haproxy/info** method, which returns process information:

    $ curl -H "Content-Type: application/json" -X GET -S -s -u dataplaneapi:mypassword "http://localhost:5555/v1/services/haproxy/info" | python3 -m json.tool
    {
        "haproxy": {
            "pid": 1622051,
            "processes": 1,
            "release_date": "2019-12-21",
            "uptime": 16985,
            "version": "2.0.12"
        }
    }

When fetching data with GET requests you do not need any additional URL parameters.  For example, to get the HAProxy configuration file in plain text, use the **/services/haproxy/configuration/raw** method:

    $ curl -H "Content-Type: application/json" -X GET -S -s -u dataplaneapi:mypassword "http://localhost:5555/v1/services/haproxy/configuration/raw" | python3 -m json.tool | sed -e 's/\\n/\n/g'
    {
        "data": "global
        daemon
        maxconn 256
        stats socket /var/run/haproxy.sock user haproxy group haproxy mode 660 level admin
    
    defaults
        mode http
        timeout connect 5000ms
        timeout client 50000ms
        timeout server 50000ms
    
    userlist dataplaneapi
        user dataplaneapi insecure-password mypassword
    
    listen http-in
        bind *:8000
        server server1 127.0.0.1:80 maxconn 32
    
    "
    }

## Example use case
Here is how a backend can be created with servers that a frontend binds to.
First, initialize a transaction:

    $ curl -H "Content-Type: application/json" -X POST -S -s -u dataplaneapi:mypassword "http://localhost:5555/v1/services/haproxy/transactions?version=1" | python3 -m json.tool
    {
        "_version": 1,
        "id": "78dd7054-c83c-4408-bf68-ddc1c0289054",
        "status": "in_progress"
    }


Make note of the transaction ID above (78dd7054-c83c-4408-bf68-ddc1c0289054 in this case).  Subsequent calls during this transaction will include the **transaction_id** parameter in the URL. To view all transactions, use the following command:

    $ curl -H "Content-Type: application/json" -X GET -S -s -u dataplaneapi:mypassword "http://localhost:5555/v1/services/haproxy/transactions" | python3 -m json.tool
    [
        {
            "_version": 1,
            "id": "78dd7054-c83c-4408-bf68-ddc1c0289054",
            "status": "in_progress"
        }
    ]

Second, add a backend:

    $ curl -d '{"name": "test_backend", "mode":"http", "balance": {"algorithm":"roundrobin"}, "httpchk": {"method": "HEAD", "uri": "/check", "version": "HTTP/1.1"}}' -H "Content-Type: application/json" -X POST -S -s -u dataplaneapi:mypassword "http://localhost:5555/v1/services/haproxy/configuration/backends?transaction_id=78dd7054-c83c-4408-bf68-ddc1c0289054" | python3 -m json.tool
    {
        "balance": {
            "algorithm": "roundrobin",
            "arguments": null
        },
        "httpchk": {
            "method": "HEAD",
            "uri": "/check",
            "version": "HTTP/1.1"
        },
        "mode": "http",
        "name": "test_backend"
    }

Third, add servers to the backend:

    $ curl -d '{"name": "server1", "address": "127.0.0.1", "port": 8080, "check": "enabled", "maxconn": 30, "weight": 100}' -H "Content-Type: application/json" -X POST -S -s -u dataplaneapi:mypassword "http://localhost:5555/v1/services/haproxy/configuration/servers?backend=test_backend&transaction_id=78dd7054-c83c-4408-bf68-ddc1c0289054" | python3 -m json.tool
    {
        "address": "127.0.0.1",
        "check": "enabled",
        "maxconn": 30,
        "name": "server1",
        "port": 8080,
        "weight": 100
    }
    $ curl -d '{"name": "server2", "address": "127.0.0.2", "port": 8080, "check": "enabled", "maxconn": 30, "weight": 100}' -H "Content-Type: application/json" -X POST -S -s -u dataplaneapi:mypassword "http://localhost:5555/v1/services/haproxy/configuration/servers?backend=test_backend&transaction_id=78dd7054-c83c-4408-bf68-ddc1c0289054" | python3 -m json.tool
    {
        "address": "127.0.0.2",
        "check": "enabled",
        "maxconn": 30,
        "name": "server2",
        "port": 8080,
        "weight": 100
    }
    $ curl -d '{"name": "server3", "address": "127.0.0.3", "port": 8080, "check": "enabled", "maxconn": 30, "weight": 100}' -H "Content-Type: application/json" -X POST -S -s -u dataplaneapi:mypassword "http://localhost:5555/v1/services/haproxy/configuration/servers?backend=test_backend&transaction_id=78dd7054-c83c-4408-bf68-ddc1c0289054" | python3 -m json.tool
    {
        "address": "127.0.0.3",
        "check": "enabled",
        "maxconn": 30,
        "name": "server3",
        "port": 8080,
        "weight": 100
    }

Fourth, add the frontend:

    $ curl -d '{"name": "test_frontend", "mode": "http", "default_backend": "test_backend", "maxconn": 2000}' -H "Content-Type: application/json" -X POST -S -s -u dataplaneapi:mypassword "http://localhost:5555/v1/services/haproxy/configuration/frontends?transaction_id=78dd7054-c83c-4408-bf68-ddc1c0289054" | python3 -m json.tool
    {
        "default_backend": "test_backend",
        "maxconn": 2000,
        "mode": "http",
        "name": "test_frontend"
    }

Fifth, add a bind line to the frontend:

    $ curl -d '{"name": "http", "address": "*", "port": 9433}' -H "Content-Type: application/json" -X POST -S -s -u dataplaneapi:mypassword "http://localhost:5555/v1/services/haproxy/configuration/binds?frontend=test_frontend&transaction_id=78dd7054-c83c-4408-bf68-ddc1c0289054" | python3 -m json.tool
    {
        "address": "*",
        "name": "http",
        "port": 9433
    }

Finally, 
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTQwMDE5NzY0MywtNzI2NjYwODgwLC0xNT
AxNTYxOTg2LDcwOTU2NTExNywxOTk3NDU5MjQ2LC0xMzYwNjc3
MzUxLC0yMDYwODU4MjU5LC0xODEyMDgxMjU4LC0xMDMzNzc3Mj
I5LDEzNzc0NDA2NiwtMTIwNzExNjA3Myw3MzMyMTU5ODQsLTEy
NzYxOTI2NTgsMjAyNTM2NDE3MywxODUzMDU3NjI3LC0xODIwOD
EwNTM5LDE1OTI0NDU5MDYsMjU5MTgyMTYwLDE4MDM4MDc4NTZd
fQ==
-->