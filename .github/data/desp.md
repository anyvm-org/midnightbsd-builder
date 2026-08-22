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
