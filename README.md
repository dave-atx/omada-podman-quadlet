# Podman Recipe for TP-Link Omada Software Controller
rootless podman [quadlet][1] recipe
for the Omada Software Controller. Uses pure `systemd`
to orchestrate the containers.

Intended to be hosted on a free tier class cloud server
for home-sized networks. Utilizes mbentley's
[excellent Docker image][2].

Includes [tailscale][3] for a site to site VPN with the home
network, [cloudflared][4] for exposing the controller to the
internet behind zero trust authentication, and [sftpgo][5]
for pushing backups from the controller to an S3 compatible
storage backend.

## Installation
Contents of this repository are intended to live inside
`.config` in your home directory. You'll need to configure
the `.env` file in [`.config/containers/systemd/omada/`][6]
for your `cloudflared` and `tailscale` keys.

To enable and start services at login:

    systemctl --user enable omada.target
    systemctl --user start omada.target

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
[3]: https://hub.docker.com/r/tailscale/tailscale
[4]: https://hub.docker.com/r/cloudflare/cloudflared
[5]: https://hub.docker.com/r/drakkan/sftpgo
[6]: https://github.com/dave-atx/docker-omada-compose/blob/main/.config/containers/systemd/omada/.env.example
