# Setting up proxy using Nginx
## How to install
### 1. Clone this repo
### 2. Install Docker

```console
# Set up the repository
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

# Install Docker Engine
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose
```
## How to Run
```console
sudo docker-compose up -d
```
## How to test HTTP (Without other destination servers)

### Set up two mock flask servers with docker
These section are two mock flask servers in the docker-compose.yml file:
```yaml
app1:
    build: .
    container_name: app1
    ports:
      - "5000:5000"
app2:
    build: .
    container_name: app2
    ports:
      - "5001:5000"
```

### Modify the nginx.conf file for the proxy settings
Add the server_name/IP_address and port number to the upstream box. For example:
```conf
upstream app{
        server app1:5000;
        server app2:5000;
    }
```
You can change the IP and port to any IP address you want the proxy to forward to.
Run:
```console
sudo docker-compose up -d
```
### HTTPS
Comment and uncomment corresponding sections in the docker-compose.yml file and the nginx.conf file to enable https.

#### Certificates
For https, make sure you have .crt and .key files for the SSL and put them in cert folder. You can generate the .crt and .key from ZeroSSL(https://zerossl.com/) for free. Download the cert file. There should be 3 files, which are certificate.crt , ca_bundle.crt and private.key .

You need to combine certificate.crt and ca_bundle.crt in order to make the SSL complete. For the combination, run:
```console
cat certificate.crt ca_bundle.crt > chained.crt
```
You may use online SSL checker (https://www.sslshopper.com/ssl-checker.html) to check if the SSL of the domain name validate.

Note: If you do not have the domain name, you cannot obtain SSL certificate. You may need a self-signed certificate for testing. Now we are using self-signed certificates for demo.

#### nginx.conf
If there is no other problem, write chained.crt and priavte.key into the nginx.conf like below
```conf
ssl_certificate /etc/nginx/cert/chained.crt;
ssl_certificate_key /etc/nginx/cert/private.key;
```
Run:
```console
sudo docker-compose up -d
```
You can access https://<your domain name> to test the proxy.


