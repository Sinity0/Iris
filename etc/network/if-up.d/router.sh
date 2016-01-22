iptables -F
iptables -X

iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A INPUT -i wlan0 -j ACCEPT
iptables -A OUTPUT -o wlan0 -j ACCEPT

iptables -A POSTROUTING -t nat -o eth0 -j MASQUERADE
iptables -A FORWARD -i wlan0 -j ACCEPT