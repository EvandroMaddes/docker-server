# Architecture

This repository stores all configuration files needed to run my personal home server.\
From the software point of view, it is a docker-based environment. All containers are managed
using [docker compose](https://docs.docker.com/compose) and relative yaml files.

| Container                               | Description                                                                                                                                                                | Source                                                                          | Env variable                                                           |
|-----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|------------------------------------------------------------------------|
| [Traefik](https://traefik.io/traefik/)  | Reverse proxy and load balancer                                                                                                                                            | [traefik container](https://hub.docker.com/_/traefik)                           | <ul><li>`TRAEFIK_INTERNAL_IP`</li></ul>                                |
| Whoami                                  | Tiny Go webserver that prints os information and HTTP request to output                                                                                                    | [whoami continer](https://registry.hub.docker.com/r/traefik/whoami)             | <ul><li>`WHOAMI_INTERNAL_IP`</li><li>`WHOAMI_PORT`</li></ul>           |
| [FileBrowser](https://filebrowser.org/) | File Browser is a create-your-own-cloud-kind of software where you can install it on a server, direct it to a path and then access your files through a nice web interface | [filebrowser container](https://registry.hub.docker.com/r/hurlenko/filebrowser) | <ul><li>`FILEBROWSER_INTERNAL_IP`</li><li>`FILEBROWSER_PORT`</li></ul> |

The server is hosted on [Raspberry Pi 4](https://www.raspberrypi.com/documentation/).

Routing is managed by Traefik, all request are autheticated using
traefik [auth middleware](https://doc.traefik.io/traefik/middlewares/http/basicauth/).
Users are listed in file `usersfile.txt`
under [`traefik/config`](/volumes/traefik/config) directory.
Others containers are not directly accessible from internet.

# Repository Structure

All used containers are listed in
the [`docker-compose.yml`](docker-compose.yml) file.\
Firstly a docker network is created (`${BASE_INTERNAL_IP}/24`), all containers will run inside it.\
For each container there is a directory with relative files (data and configuration). They are stored
inside [`volumes`](/volumes) directory.\
In the [`utils`](utils) directory there are scripts used for
developing or debugging purposes.

# Required network configuration

### Open ports on your router

Although it is trivial to specify it, you have to open the ports on your router in order to allow network traffic from
internet to your server and viceversa.
> How to open ports on your router depends on router vendor. Nothing that a Google search can't resolve :wink:

In my case, I opened port 443 and port 80 to allow https and http traffic to Traefik container. Also port 8080 is opened
to access the Traefik dashboard.
Traefik is responsible to route the requests to the relative container and this is specified in
the [`config/config.yml`](volumes/traefik/config/config.yml)
file (rule section, one for each container).
> Remember to open ports that are actually used by your Traefik container!

### Register records on your DNS provider

Of course, you have to register a new record on your DNS provider in order to associate your domain name to your
**public** ip address, your ip address can be retrieved from this [site](https://whatismyipaddress.com/).
If you use wildcard domains, remember to register also these records on your provider as _**CNAME** record_ pointing to
your main domain, this allows Traefik to execute the relative rule.

# Environmental variables

All variable are stored in a `.env` file at the same level
of [`docker-compose.yml`](docker-compose.yml) file.

- `DOMAIN_NAME`: name of hosted domain
- `USER_MAIL`: personal mail used to register the domain

Since Traefik uses ACME provider (Let's Encrypt) for automatic certificate generation, it required user information.
In my case the domain is purchased from name.com, required information are username, token and server.
> In case you choose another domain provider required information are listed on
> Trafik [documentation](https://doc.traefik.io/traefik/https/acme/#providers)

- `NAMECOM_USERNAME_PROD`: username
- `NAMECOM_API_TOKEN_PROD`: token
- `NAMECOM_SERVER_PROD`: server endpoint, i.e. _api.name.com_

Static ip is assigned to docker network. The specified ip is internal to the docker network.

- `BASE_INTERNAL_IP`: ip

- `TRAEFIK_INTERNAL_IP`: traefik ip

- `WHOAMI_INTERNAL_IP`: whoami ip
- `WHOAMI_PORT`: port assigned to whoami container

- `FILEBROWSER_INTERNAL_IP`: filebrowser ip
- `FILEBROWSER_PORT`: port assigned to filebrowser container

# Getting Started

To run this docker-based server and expose it to the internet follow these steps:

1. Clone the repo
   ```bash
   git clone https://github.com/EvandroMaddes/docker-server.git
   ```
2. Set all environment variables, and sotre them in `.env` file
3. Register DNS records on your DNS provider
4. Open ports on your router
5. Create docker network and launch the containers

```bash
 docker compose up -d
```

If all is good, on your command line you see:

```bash
[+] Running 3/3
✔ Container filebrowser            Started                                                                                                                                                                                    0.0s
✔ Container whoami-sensor-service  Started                                                                                                                                                                                    0.0s
✔ Container traefik                Started
```

Type on your domain name on your browser, it redirects to Traefik dashboard.
In my case it is:`https://${DOMAIN_NAME}`\
To access FileBrowser, connect to the endpoint specified in
the  [`config/config.yml`](volumes/traefik/config/config.yml)
file.
In my case it is:`https://filebrowser.${DOMAIN_NAME}`

## Debug tools

Most time-consuming activity is the network setting and Traefik configuration. I found very helpful the Traefik
documentation and Let's Debug.

- [`letsdebug.net`](https://letsdebug.net/): Let's Debug is a diagnostic tool/website to help figure out why you might
  not
  be able to issue a
  certificate for Let's Encrypt™.

> On the codes, I've left different comments explaining sections purposes and different available choices 

