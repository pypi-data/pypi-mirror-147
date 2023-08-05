# nordvpn-polybar

A polybar extension for nordvpn users


# How to install

Install python module
```
pip install nordvpn-polybar
```


Add to polybar config
```
[module/vpn]
type = custom/script
label = Nordvpn
exec = python -m nordvpn_polybar.main "{status} {city} {transfer}"
interval = 1
format-underline = #2196f3
```
