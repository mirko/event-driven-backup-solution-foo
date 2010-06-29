#!/usr/bin/python

# general settings

## dbus constants
#dbus_signals = {
#    # name: ('dbus-interface', 'signal_name', 'path', {properties})
#    'dbus_signal_nm_dhcp4': (
#        'org.freedesktop.NetworkManager.DHCP4Config',
#        'PropertiesChanged',
#        None,
#            {
#                'ip': 'Options.dhcp_server_identifier',
#            },
#        ),
#    'dbus_signal_nm_dhcp6': ('org.freedesktop.NetworkManager.DHCP6Config', 'PropertiesChanged'),
#}

dbus_signals = {
    # name: ('dbus-interface', 'signal_name', 'path', {properties})
    'dbus_signal_nm_dhcp4': (
        'org.freedesktop.NetworkManager.DHCP4Config',
        'PropertiesChanged',
    ),
    'dbus_signal_nm_dhcp6': (
        'org.freedesktop.NetworkManager.DHCP6Config',
        'PropertiesChanged',
    ),
}

## dbus methods
def dbus_event(x, sender=None):
    print 'foo'
    print x
    print sender

##### backup backends
bbs = [
    {
        'name': 'defect', # name of backup config (arbitrary)
        'host': 'foo', # if set, data will be backup upped on a remote host
        'path': '/bck', # path to back up
        'path_dest': '/storage/bck/',
        'priority': 10, # lower = higher priority, defines which backend to try first
        'keep': 3,
        'hardlink': True,
        'triggers': (
            {
                'signal': 'dbus_signal_nm_dhcp4',
                'Options.dhcp_server_identifier': '192.168.2.1',
            },
         ),
        'pre': [], # array of shell commands going to be exec'ed before backup starts
        'post': [], # array of shell commands goiing to be exec'ed after backup finished # TODO: only if backup was successful(?)
    }
]
#####

#config_type_checking(backup_backend):
#    struct = {
#        'name': (str)
#        'protocol': (str)
#        'host': (str, None)
#        'path': 

#TODO: when 'local' chosen, check whether path is mounted - otherwise throw a warning (backupping onto the same disk/partition doesn't make much sense)
#for k in range(0,i):
#    print k
#    print bb[k]

import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()

for backup_config in bbs:
    print 'starting backup < %s >'%(backup_config['name'])
    for trigger in backup_config['triggers']:
        print 'add dbus trigger for: < %s >'%str(dbus_signals[trigger['signal']])
        bus.add_signal_receiver(dbus_event, dbus_interface=dbus_signals[trigger['signal']][0], signal_name=dbus_signals[trigger['signal']][1])
loop = gobject.MainLoop()
loop.run()
