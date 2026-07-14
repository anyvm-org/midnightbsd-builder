

[![Build](https://github.com/anyvm-org/midnightbsd-builder/actions/workflows/build.yml/badge.svg)](https://github.com/anyvm-org/midnightbsd-builder/actions/workflows/build.yml)

Latest: v2.0.5


The image builder for `midnightbsd`


All the supported releases are here:



| Release | x86_64  |
|---------|---------|
| 4.0.6   |  ✅ (rsync,scp,sshfs,nfs)     |
| 4.0.4   |  ✅ (rsync,scp,sshfs,nfs)     |
| 3.2.4   |  ✅ (rsync,scp,sshfs,nfs)     |
| 2.2.8   |  ✅ (rsync,scp,sshfs,nfs)     |





How to build:

1. Use the [manual.yml](.github/workflows/manual.yml) to build manually.
   
    Run the workflow manually, you will get a view-only webconsole from the output of the workflow, just open the link in your web browser.
   
    You will also get an interactive VNC connection port from the output, you can connect to the vm by any vnc client.

2. Run the builder locally on your Ubuntu machine.

    Just clone the repo. and run:
    ```bash
    python3 build.py conf/midnightbsd-4.0.6.conf
    ```
   
