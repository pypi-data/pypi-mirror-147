# Toori

Simple Python/C++ library for tunneling network traffic over http(s).

## iro

Server module. 

Relies on [`Scapy`](https://scapy.net/) and [`Socket.IO`](https://socket.io/).

### Usage

#### HTTP

```
iro -p 80 -f tcp and src port 443
```

#### HTTPS

```
iro -p 443 -f tcp and src port 443 -c <ssl cert path> -k <ssl key path>
```

## toori

Client module. Only available on Windows. 

Relies on [`WinDivert`](https://github.com/basil00/Divert) and [`Socket.IO`](https://socket.io/).

WinDivert requires Administrator privileges.

### Usage

```
toori -a <server address> -p 80 -f tcp && tcp.DstPort == 443 -t polling
```
