# MidnightBSD unattended install via `bsdinstall script`.
#
# Confirmed on 4.0.4: once the script argument is passed intact (avoid the
# quoting traps the old bash hook fell into where `inputKeys` eval'd its
# input and a bare `string bsdinstall script /tmp/ic` landed in `string()`
# with just $1=bsdinstall -- which then drops into the interactive TUI),
# bsdinstall reads PARTITIONS/DISTRIBUTIONS and the post-install `#!/bin/sh`
# block from the installerconfig and powers off on its own. No keymap /
# hostname / network / timezone dialogs to drive.
#
# Host-side hook: run by base-builder/build.py via exec() in this module's
# globals, so functions like waitForText / inputKeys / string / enter / sleep
# (Python's time.sleep) are available as bare names.

# ISO auto-boots -> Welcome dialog; Keymap Selection auto-clears on this ISO
# without user input.
waitForText(osname, "MidnightBSD Installer", "300")
time.sleep(5)

# Welcome menu: Install / Shell / Live CD -- Tab moves Install->Shell, Enter selects.
inputKeys("tab; sleep 1; enter")

# Live shell prompt.
time.sleep(10)

# Bring up the network (virtio NIC == vtnet0).
string(osname, "dhclient vtnet0")
enter(osname)
time.sleep(15)

# Pull the installerconfig from the host-side web server.
string(osname, "fetch -o /tmp/ic http://192.168.122.1:8000/%s" % env("VM_OPTS"))
enter(osname)
time.sleep(10)

# Kick off the unattended install; the resp ends with `poweroff` and the
# build pipeline's main loop polls isRunning.
string(osname, "bsdinstall script /tmp/ic")
enter(osname)
