# Kali Docker Image


### < This will be overtaken by a dockerfile that will do these steps for you >

```
- Pull Kali Image
    --> docker pull kalilinux/kali-rolling

- Enter Image in Interactive Mode
    --> docker run -it kalilinux/kali-rolling /bin/sh

- Update Packages and then install kali-linux-headless packages
    --> apt update && apt -y install kali-linux-headless

- Update Packages and then install postgresql
    --> apt-get update && apt-get install postgresql

- Install postgresql
    --> apt-get install postgresql

- Start postgresql
    --> service postgresql start

- Install nano
    --> apt install nano

- From root directory navigate to postgresql directory:
    --> cd /etc/postgresql/16/main

- Nano the postgresql.conf file and modify the listen_address line to be: listen_addresses = '*'
    --> sudo nano postgresql.conf

- Nano the postgresql.conf file and modify the listen_address line to be: listen_addresses = '*'
    --> sudo nano postgresql.conf

- Add following line to the pg_hba.conf file:
host    all             all             127.0.0.1/32            trust
    --> sudo nano pg_hba.conf

- Restart Postgres
    --> /etc/init.d/postgresql restart

- Initialize Metasploit
    --> msfdb init

* msfconsole *

Happy Metasploiting you little demon!