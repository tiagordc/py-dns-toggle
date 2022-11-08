import sys, re, os
from PyQt5 import QtGui, QtWidgets, QtCore

adapter, dns_ip = sys.argv[-2:]
app = QtWidgets.QApplication([])
process = QtCore.QProcess()

def resource_path(*path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.normpath(os.path.dirname(__file__))
    return os.path.join(base_path, *path)

def get_dns():
    ''' Get the current DNS server for the given adapter '''
    process.start('netsh', ['interface', 'ipv4', 'show', 'config', f'name={adapter}'])
    process.waitForFinished()
    output = process.readAllStandardOutput().data().decode('utf-8')
    match = re.search(r"DNS.+?:\s+\b((?:[0-9]{1,3}\.){3}[0-9]{1,3})", output)
    return match.group(1) if match else None

dns_original = get_dns()
widget = QtWidgets.QSystemTrayIcon()
widget.setToolTip(f"DNS: {dns_original}")

if dns_ip == dns_original: 
    widget.setIcon(QtGui.QIcon(resource_path('img', 'on.svg')))
    dns_original = None # we don't have an original DNS, so we go back to DHCP
else:
    widget.setIcon(QtGui.QIcon(resource_path('img', 'off.svg')))

def toggle_dns():
    ''' Toggle the active DNS server between the original and the given one '''
    current = get_dns()
    if current == dns_ip: 
        if dns_original is None:
            process.start('netsh', ['interface', 'ipv4', 'set', 'dns', f'name={adapter}', 'source=dhcp'])
            widget.setToolTip(f"DNS: DHCP")
        else:
            process.start('netsh', ['interface', 'ipv4', 'set', 'dns', f'name={adapter}', 'static', dns_original ])
            widget.setToolTip(f"DNS: {dns_original}")
        widget.setIcon(QtGui.QIcon(resource_path('img', 'off.svg')))
    else:
        process.start('netsh', ['interface', 'ipv4', 'set', 'dns', f'name={adapter}', 'static', dns_ip ])
        widget.setToolTip(f"DNS: {dns_ip}")
        widget.setIcon(QtGui.QIcon(resource_path('img', 'on.svg')))

widget.activated.connect(toggle_dns)
widget.show()
sys.exit(app.exec_())
