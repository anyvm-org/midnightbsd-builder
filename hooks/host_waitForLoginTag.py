# Wait for the guest to reach the login prompt after a fresh boot.
#
# Host-side hook: run by base-builder/build.py via exec() in this module's
# globals. start_and_wait() invokes us right after openConsole().
#
# Two-stage wait: first match VM_LOGIN_TAG (e.g. "MidnightBSD/amd64"), then
# look for the literal "logi" so we catch the actual login: prompt and not
# a banner that happens to embed the tag.

# Stage 1 is BEST EFFORT -- do not make it fatal. It legitimately times out in
# successful builds: 30 s is short, and CI tesseract regularly drops the leading
# capital (run 30265903005 green jobs 4.0.4/4.0.6 both logged
# "Timeout for text: idnightBSD/amd64" and went on to build fine).
waitForText(env("VM_LOGIN_TAG"), "30")

time.sleep(10)

# Stage 2 is the real gate, and it MUST be bounded and fatal.
#
# It used to be an unbounded waitForText("logi"): with no third argument
# waitForText polls forever. On 2026-07-27 the 3.2.4 install ISO panicked
# ("panic: vm_fault: fault on nofault entry") so nothing was ever installed;
# the disk then had no bootloader ("Boot failed: not a bootable disk", "No
# bootable device"), the login prompt could never appear, and this line spun
# "(no new screen text)" for 5 h 40 m until a human cancelled the job.
#
# Fatal is safe here (unlike stage 1): across that run's three green jobs
# "logi" was always found, within ~4 s of the stage-1 wait -- it never timed
# out in a build that worked.
#
# Why this must exit rather than just return: start_and_wait() treats the mere
# presence of a waitForLoginTag hook as success (`if run_hook(...): return 0`),
# so it applies neither VM_LOGIN_MAX_SECONDS nor its force-kill-and-reboot
# reroll to us. If we returned quietly after a failed wait the pipeline would
# march on against a VM that never booted.
if waitForText("logi", "300") != 0:
    log("FATAL: guest never reached a login prompt (no 'logi' on the console).")
    log("       The install most likely failed or the guest panicked -- check "
        "the screen dump above for 'panic:' or 'not a bootable disk'.")
    sys.exit(1)
