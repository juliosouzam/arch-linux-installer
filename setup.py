from subprocess import run
import crypt

USER = input('Qual usuário? ') or 'julio'
HOSTNAME = input('Qual o hostname? ') or 'juliocesar'
PASSWORD = crypt.crypt(
    input('Qual a senha do usuário ' + USER + '? (default: admin)') or 'admin')
LANG = input('Qual a lang? (default: pt_BR) ') or 'pt_BR'
ENCODE = input('Qual o encode? (default: UTF-8)') or 'UTF-8'
TIME_ZONE = input(
    'Qual o timezone? (default: America/Fortaleza) ') or 'America/Fortaleza'

try:
    run(['sed', '-i', '/' + LANG + '/,+1 s/^#//', '/etc/locale.gen'], check=True)
    run(['locale-gen'], check=True)
    run(['echo', 'LANG=' + LANG + '.' + ENCODE + '', '>', '/etc/locale.conf'], check=True)

    run(['ln', '-sf', '/usr/share/zoneinfo/' +
         TIME_ZONE, '/etc/localtime'], check=True)

    run(['sed', '-i', '/multilib\\]/,+1 s/^#//', '/etc/pacman.conf'], check=True)
    run(['pacman', '-Sy'], check=True)

    run(['echo ' + HOSTNAME, '>', '/etc/hostname'])

    run(['echo', '127.0.0.1\tlocalhost', '>', '/etc/hosts'], check=True)

    run(['sed', '-i', 's/nameserver/#nameserver/g', '/etc/resolv.conf'], check=True)
    run(['echo', 'nameserver\t8.8.8.8', '>>', '/etc/resolv.conf'], check=True)
    run(['echo', 'nameserver\t8.8.4.4', '>>', '/etc/resolv.conf'], check=True)

    run(['pacman', '-S', 'wpa_supplicant', 'dialog',
         'iw', 'networkmanager', 'sudo'], check=True)

    run(['systemctl', 'enable', 'NetworkManager'], check=True)
    run(['useradd', '-m', '-g', 'users', '-G', 'log,sys,wheel,rfkill,dbus',
         '-s', '/bin/bash', '-p', PASSWORD, USER], check=True)

    print('#### DEFINIR SENHA ROOT #####')
    run(['passwd'], check=True)

    run(['pacman', '-S', 'bash-completion'], check=True)

    run(['sed', '-i', '/%wheel ALL=(ALL) ALL/s/^#//', '/etc/sudoers'], check=True)

except Exception as ex:
    print(ex)
