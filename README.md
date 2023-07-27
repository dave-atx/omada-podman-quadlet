# docker-omada-compose
docker-compose / rootless podman-compose recipe
for the Omaha Software Controller.

Intended to be hosted on a free tier class cloud server 
for home-sized networks.

Includes Wireguard for a site to site VPN with the home
network, cloudflared for exposing the controller to the
internet behind zero trust authentication, and sftpgo
for pushing backups from the controller to an S3 compatible
storage backend.

