
# MidnightBSD unattended install via `bsdinstall script`.
#
# Confirmed on 4.0.4: once the script argument is passed intact (note the
# double quotes around multi-word payloads — `inputKeys` eval's its input, so
# a bare `string bsdinstall script /tmp/ic` lands in the `string` helper with
# $1=bsdinstall only, and `bsdinstall` with no args drops into the interactive
# TUI), bsdinstall reads PARTITIONS/DISTRIBUTIONS and the post-install
# `#!/bin/sh` block from the installerconfig and powers off on its own. No
# keymap/hostname/network/timezone/... dialogs to drive.

# ISO auto-boots → Welcome dialog; Keymap Selection auto-clears on this ISO
# without user input.
waitForText "MidnightBSD Installer" 300
sleep 5

# Welcome menu: Install / Shell / Live CD — Tab moves Install→Shell, Enter selects.
inputKeys "tab; sleep 1; enter"

# Live shell prompt.
sleep 10

# Bring up the network (virtio NIC == vtnet0).
inputKeys 'string "dhclient vtnet0"; enter'
sleep 15

# Pull the installerconfig from the host-side web server.
inputKeys "string \"fetch -o /tmp/ic http://192.168.122.1:8000/$VM_OPTS\"; enter"
sleep 10

# Kick off the unattended install; the resp ends with `poweroff` and
# build.sh's main loop polls isRunning.
inputKeys 'string "bsdinstall script /tmp/ic"; enter'
