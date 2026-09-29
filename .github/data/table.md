

| Release | x86_64 |
|---------|---------|
| 4.0.8 | ✅ (rsync,scp,sshfs,nfs,tar) |
| 4.0.7 | ✅ (rsync,scp,sshfs,nfs,tar) |
| 4.0.6 | ✅ (rsync,scp,sshfs,nfs,tar) |
| 4.0.4 | ✅ (rsync,scp,sshfs,nfs,tar) |
| 3.2.4 | ✅ (rsync,scp,sshfs,nfs,tar) |
| 2.2.8 | ✅ (rsync,scp,sshfs,nfs,tar) |

How the images are built:

Each image is built automatically in the
[anyvm-org/midnightbsd-builder](https://github.com/anyvm-org/midnightbsd-builder)
repo's GitHub Actions: it downloads the official MidnightBSD installer
ISO, boots it in QEMU, answers the installer unattended, enables ssh,
pre-installs the packages listed in the conf, and exports the installed
disk as a compressed qcow2 image.

Upstream install media: the official MidnightBSD ISOs from
https://midnightbsd.org/ftp/MidnightBSD/releases/ (download page:
https://www.midnightbsd.org/download/).
