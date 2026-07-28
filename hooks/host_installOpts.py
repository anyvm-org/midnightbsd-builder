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
#
# A timeout here is FATAL. Every keystroke below assumes the installer TUI is
# on screen; if it never appeared the guest is dead and we would type dhclient
# / fetch / bsdinstall into a panic message, "install" nothing, and only fail
# much later with a confusing "not a bootable disk". That is exactly what
# happened on 2026-07-27 (run 30265903005, 3.2.4): the ISO panicked with
# "panic: vm_fault: fault on nofault entry", this wait timed out, the hook
# carried on regardless, and the job then hung 5 h 40 m in the login wait.
# Safe to be strict: the three green jobs in that same run never timed out
# here -- only on the best-effort login-tag anchor.
if waitForText("MidnightBSD Installer", "300") != 0:
    log("FATAL: the MidnightBSD installer never appeared on the console.")
    log("       The install ISO most likely panicked -- check the screen dump "
        "above for 'panic:'. Aborting instead of typing into a dead screen.")
    sys.exit(1)
time.sleep(5)

# Welcome menu: Install / Shell / Live CD -- Tab moves Install->Shell, Enter selects.
inputKeys("tab; sleep 1; enter")

# Live shell prompt.
time.sleep(10)

# Bring up the network (virtio NIC == vtnet0).
string("dhclient vtnet0")
enter()
time.sleep(15)

# Pull the installerconfig from the host-side web server.
string("fetch -o /tmp/ic http://192.168.122.1:8000/%s" % env("VM_OPTS"))
enter()
time.sleep(10)

# Kick off the unattended install; the resp ends with `poweroff` and the
# build pipeline's main loop polls isRunning.
string("bsdinstall script /tmp/ic")
enter()
