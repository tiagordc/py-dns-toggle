import sys, re
from PyQt5 import QtGui, QtWidgets, QtCore

adapter, dns_ip = sys.argv[-2:]
app = QtWidgets.QApplication([])
process = QtCore.QProcess()

def get_dns():
    process.start('netsh', ['interface', 'ipv4', 'show', 'config', f'name={adapter}'])
    process.waitForFinished()
    output = process.readAllStandardOutput().data().decode('utf-8')
    match = re.search(r"DNS.+?:\s+\b((?:[0-9]{1,3}\.){3}[0-9]{1,3})", output)
    if match: return match.group(1)
    return None

dns_original = get_dns()
widget = QtWidgets.QSystemTrayIcon()
widget.setToolTip(f"DNS: {dns_original}")

def toggle_dns():
    current = get_dns()
    if current == dns_ip: 
        if dns_original is None:
            process.start('netsh', ['interface', 'ipv4', 'set', 'dns', f'name={adapter}', 'source=dhcp'])
            widget.setToolTip(f"DNS: DHCP")
        else:
            process.start('netsh', ['interface', 'ipv4', 'set', 'dns', f'name={adapter}', 'static', dns_original ])
            widget.setToolTip(f"DNS: {dns_original}")
        widget.setIcon(QtGui.QIcon('img/off.svg'))
    else:
        process.start('netsh', ['interface', 'ipv4', 'set', 'dns', f'name={adapter}', 'static', dns_ip ])
        widget.setToolTip(f"DNS: {dns_ip}")
        widget.setIcon(QtGui.QIcon('img/on.svg'))

if dns_ip == dns_original: 
    widget.setIcon(QtGui.QIcon('img/on.svg'))
    dns_original = None
else:
    widget.setIcon(QtGui.QIcon('img/off.svg'))

widget.activated.connect(toggle_dns)
widget.show()
sys.exit(app.exec_())
