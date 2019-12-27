from subprocess import run

USER = input('Qual usuário? ') or 'julio'
HOSTNAME = input('Qual o hostname? ') or 'juliocesar'
PASSWORD = input('Qual a senha? (default: admin)') or 'admin'
LANG = input('Qual a lang? (default: pt_BR) ') or 'pt_BR'
ENCODE = input('Qual o encode? (default: UTF-8)') or 'UTF-8'
TIME_ZONE = input(
    'Qual o timezone? (default: America/Fortaleza) ') or 'America/Fortaleza'

try:
    run(['sed', '-i', '/{LANG}/,+1 s/^#//', '/etc/locale.gen'], check=True)
    run(['locale-gen'], check=True)
    run(['echo', 'LANG={LANG}.{ENCODE}', '>', '/etc/locale.conf'], check=True)
    run(['export', 'LANG={LANG}.{ENCODE}'], check=True)

    run(['ln', '-sf', '/usr/share/zoneinfo/' +
         TIME_ZONE, '/etc/localtime'], check=True)

    run(['sed', '-i', '/multilib\\]/,+1 s/^#//', '/etc/pacman.conf'], check=True)
    run(['pacman', '-Sy'], check=True)
except Exception as ex:
    print(ex)
