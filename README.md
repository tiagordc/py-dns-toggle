
# DNS Toggle for Windows

This is a simple app that allows you to toggle between your default DNS and a custom DNS. 

It is useful for when you want to use a Pi-Hole or other DNS server, but don't want to have to change your DNS settings every time you want to use it.

## Run

```console

py -3.8 -m venv env
env\scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
pip list --outdated
py run.py "Network Bridge" "192.168.10.10"

```

## Credits

- [Icons by Anu Rocks](https://freeicons.io/profile/730)
