#!/bin/bash

#!/bin/bash

set -eux

### Create the ruggedpod user (sudoers)

adduser --disabled-password --gecos "" --shell /bin/bash ruggedpod
chpasswd <<EOF
ruggedpod:ruggedpod
EOF
adduser ruggedpod sudo

echo "ruggedpod ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/ruggedpod


### Enable startup logs redirect to serial console

chmod +w /boot/grub/grub.cfg
sed -i -e "s/\(.*\/boot\/vmlinuz\-.*\)/\1 console=tty0 console=ttyS0,{{ serial_baudrate }}n8/g" /boot/grub/grub.cfg
chmod -w /boot/grub/grub.cfg


### Replace VT102 by xterm for color support

cat > /etc/rc2.d/S99update-ttyS0 <<EOF
#!/bin/bash

sed -i "s/vt102/xterm-256color/" /etc/init/ttyS0.conf
service ttyS0 restart
rm -f /etc/rc2.d/S99update-ttyS0
EOF

chmod +x /etc/rc2.d/S99update-ttyS0


### Notify the management that the install is done

wget --header="X-Auth-Token: Lj9MN6TlSWb6j6EvoZIJJYmUHENs2Oxr" \
                 --method=DELETE {{ api_base_url }}/v2/blades/{{ blade_number }}/build
