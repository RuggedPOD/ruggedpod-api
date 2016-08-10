#!/bin/bash

set -eux

### Create the '{{ username }}' user (sudoers)

adduser --disabled-password --gecos "" --shell /bin/bash {{ username }}
{% if password is defined %}
chpasswd <<EOF
{{ username }}:{{ password }}
EOF
{% endif %}
adduser {{ username }} sudo
echo "{{ username }} ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/{{ username }}

### Setup hostname '{{ hostname }}'
echo '{{ hostname }}' > /etc/hostname
sed -i -e "s/127\.0\.1\.1.*/127.0.1.1 {{ hostname }}/" /etc/hosts

{% if ssh_pub_key is defined %}
### Add SSH public key for user '{{ username }}'

mkdir -p /home/{{ username }}/.ssh
echo '{{ ssh_pub_key }}' > /home/{{ username }}/.ssh/authorized_keys
chown -R {{ username }}: /home/{{ username }}/.ssh
{% endif %}

### Enable startup logs redirection to serial console

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
