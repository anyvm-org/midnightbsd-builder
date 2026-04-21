#some tasks run in the VM as soon as the vm is up


echo '=================== start ===='


service ntpd enable

service ntpd start

kldload fusefs 2>/dev/null || true


echo "Applying fastest boot optimizations..."

# Optimize loader.conf. APPEND — the resp's post-install may have already
# written `vfs.root.mountfrom` (for builds like 3.2.4 / 2.2.8 where we
# partition manually with mnbsd-* types that gptboot can't auto-discover).
# A `>` redirect here would wipe that and land the next reboot at a
# mountroot prompt.
cat <<EOF >>/boot/loader.conf
autoboot_delay="0"
loader_logo="NO"
loader_menu_title="NO"

hw.hpet.enable=0
EOF

# Enable parallel RC
sysrc rc_parallel="YES"

# Required services
sysrc syslogd_enable="YES"
sysrc cron_enable="YES"


# Disable unnecessary services
sysrc growfs_enable="NO"
sysrc growfs_fstab_enable="NO"
sysrc kldxref_enable="NO"

sysrc mixer_enable="NO"
sysrc rctl_enable="NO"
sysrc virecover_enable="NO"
sysrc motd_enable="NO"
sysrc savecore_enable="NO"
sysrc utx_enable="NO"
sysrc bgfsck_enable="NO"
sysrc dmesg_enable="NO"


sysrc ipv6_network_interfaces="none"


echo 'ifconfig_em0="DHCP"' >> /etc/rc.conf
echo 'ifconfig_vtnet0="DHCP"' >> /etc/rc.conf

cat << 'EOF' >> /etc/rc.local
for iface in $(ifconfig -l); do
    if [ "$iface" != "lo0" ]; then
        dhclient $iface >/dev/null 2>&1
    fi
done
EOF
chmod +x /etc/rc.local


# Refresh mport index
mport index || true
mport update || true


echo "Done. Reboot to apply all optimizations."


