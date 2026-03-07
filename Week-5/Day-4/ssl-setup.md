# SSL Setup with NGINX using Self-Signed Certificates

## Overview

This setup configures **HTTPS using a self-signed SSL certificate** inside an NGINX container running in Docker.
NGINX acts as a **reverse proxy** and routes requests to two backend Node.js services with **round-robin load balancing**.

The system also forces **HTTP → HTTPS redirection** for secure communication.

---

## Project Architecture

Client → NGINX Reverse Proxy → Backend Containers

* backend1 (Node.js – port 3000)
* backend2 (Node.js – port 3000)

NGINX handles:

* Reverse proxy
* Load balancing
* HTTPS termination

---

## Step 1: Create Certificates Folder

Inside the project directory:

```
mkdir certs
cd certs
```

---

## Step 2: Generate Self-Signed Certificate

Run the following command:

```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout localhost-key.pem \
-out localhost.pem
```

This creates:

```
localhost.pem
localhost-key.pem
```

These files are used by NGINX to enable HTTPS.

---

## Step 3: Configure Docker Compose

Mount the certificate folder inside the NGINX container.

Example:

```
nginx:
  image: nginx:latest
  container_name: nginx-proxy
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
    - ./certs:/etc/nginx/certs
```

---

## Step 4: Configure NGINX for HTTPS

Example configuration:

```
events {}

http {

  upstream backend_servers {
      server backend1:3000;
      server backend2:3000;
  }

  server {
      listen 80;
      return 301 https://$host$request_uri;
  }

  server {
      listen 443 ssl;

      ssl_certificate /etc/nginx/certs/localhost.pem;
      ssl_certificate_key /etc/nginx/certs/localhost-key.pem;

      location /api/ {
          proxy_pass http://backend_servers/;
      }

      location / {
          return 200 "HTTPS Reverse Proxy Working";
      }
  }
}
```

---

## Step 5: Start Containers

Run:

```
docker-compose down
docker-compose up -d --build
```

---

## Step 6: Verify HTTPS

Test with curl:

```
curl -k https://localhost
```

Expected output:

```
HTTPS Reverse Proxy Working
```

Test API routing:

```
curl -k https://localhost/api
```

---

## Browser Test

Open in browser:

```
https://localhost
```

Because the certificate is self-signed, the browser may show a warning.
Click **Advanced → Proceed to localhost**.

You should see the page loading over **HTTPS**.

---

## Features Implemented

* Docker multi-container setup
* NGINX reverse proxy
* Round-robin load balancing
* Self-signed SSL certificates
* HTTPS termination
* HTTP → HTTPS redirect

---

## Output

✔ HTTPS enabled in NGINX
✔ Secure communication via SSL
✔ Reverse proxy routing to backend services
