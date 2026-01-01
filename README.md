# Podman Recipe for TP-Link Omada Software Controller
rootless podman [quadlet][1] recipe
for the Omada Software Controller. Uses pure `systemd`
to orchestrate the containers.

Intended to be hosted locally on a Raspberry Pi. Utilizes mbentley's
[excellent Docker image][2]. For a previous version of
this repository targeted at a free tier class cloud server
for home-sized networks, see the `omada-v5` tag.

Includes [caddy-docker-proxy][7] to reverse proxy to the omada
web server and [sftpgo][5] for pushing backups from the controller
to an S3 compatible storage backend.

The Cloudflare ACME DNS API plugin is used for automatic
LetsEncrypt SSL cert generation.

## Installation
Contents of this repository are intended to live inside
`.config` in your home directory. You'll need to configure
the `caddy.env` file in [`.config/containers/systemd/omada/`][6]
for your `cloudflare` keys.

You'll also need the configure A, AAAA, or CNAME DNS records pointing
to your server to access the Omada and sftpgo web interfaces.

To enable and start services at login:

    systemctl --user start omada.service

If you make changes to any of the service files after
enabling, you need to reload the `systemd` daemon:

    systemctl --user daemon-reload

Useful command for troubleshooting changes to the service
files:

    /usr/libexec/podman/quadlet --user --dryrun

which causes podman to parse the service files and check
for errors.

[1]: https://www.redhat.com/en/blog/multi-container-application-podman-quadlet
[2]: https://github.com/mbentley/docker-omada-controller
[5]: https://hub.docker.com/r/drakkan/sftpgo
[6]: https://github.com/dave-atx/docker-omada-compose/blob/main/.config/containers/systemd/omada/caddy.env.example
[7]: https://github.com/lucaslorentz/caddy-docker-proxy