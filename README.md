
# DNS Toggle for Windows

This is a simple app that allows you to toggle between your default DNS and a custom DNS from a tray icon.

It is useful for when you want to use a Pi-Hole or other DNS server, but don't want to have to change your DNS settings every time you want to use it.

## Run

```console

py -3.8 -m venv env
env\scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
pip list --outdated
py run.py "Bridge de Rede" "192.168.50.89"

pyinstaller --name DnsToggle --paths ".\env\Lib\site-packages\PyQt5\Qt\bin" --add-data='img/;img/' --clean --onefile --windowed --icon=app.ico run.py
DnsToggle.exe "Bridge de Rede" "192.168.50.89"
taskkill /im DnsToggle.exe /t /f

netsh interface ipv4 show config name="Bridge de Rede"

```

## Credits

- [Icons by Anu Rocks](https://freeicons.io/profile/730)
