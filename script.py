from subprocess import run

USER = input('Qual usuário? ') or 'julio'
HOSTNAME = input('Qual o hostname? ') or 'juliocesar'
PASSWORD = input('Qual a senha? (default: admin)') or 'admin'
SDA = input('Qual o disco? (default: /dev/sda)') or '/dev/sda'

PART_BOOT = '/dev/sda1'
PART_BOOT_EFI = '/dev/sda2'
PART_TMP = '/dev/sda3'
PART_ROOT = '/dev/sda4'
PART_HOME = '/dev/sda5'

try:
    print('######### CONFIGURANDO TECLADO #########')
    # run(['loadkeys', 'br-abnt2'], check=True)
    print('######### TECLADO Ok #########')

    print('######### VERIFICANDO INTERNET #########')
    # run(['ping', '-c', '3', 'archlinux.org'], check=True)
    print('######### INTERNET OK #########')

    print('######### CONFIGURANDO DATA #########')
    # run(['timedatectl', 'set-ntp', 'true'], check=True)
    print('######### DATA OK #########')

    print('As partições deveram ser /dev/sda1 = BOOT, /dev/sda2 = BOOT EFI, /dev/sda3 = TMP, /dev/sda4 = ROOT, /dev/sda5 = HOME')
    r = (input('Entendido? (y/N)') or 'n').lower()
    if r != 'y' or r == 'n':
        run(['exit 0'], check=True)
    print('######### INICIANDO CFDISK #########')
    run(['cfdisk', SDA], check=True)
    print('######### CFDISK OK #########')

    print('######### FORMATANDO DISCO #########')
    run(['sleep', '2'])
    print('######### FORMATANDO BOOT #########')
    run(['mkfs.ext2', '-L', 'BOOT', PART_BOOT], check=True)
    run(['sleep', '2'])
    print('######### FORMATANDO BOOT EFI #########')
    run(['mkfs.fat', '-F32', PART_BOOT_EFI], check=True)
    run(['sleep', '2'])
    print('######### FORMATANDO TMP #########')
    run(['mkfs.btrfs', '-f', '-L', 'TMP', PART_TMP], check=True)
    run(['sleep', '2'])
    print('######### FORMATANDO ROOT #########')
    run(['mkfs.btrfs', '-f', '-L', 'ROOT', PART_ROOT], check=True)
    run(['sleep', '2'])
    print('######### FORMATANDO HOME #########')
    run(['mkfs.btrfs', '-f', '-L', 'HOME', PART_HOME], check=True)

    print('######### MONTANDO OS DISCOS #########')
    print('ROOT')
    run(['mount', PART_ROOT, '/mnt'], check=True)
    print('BOOT')
    run(['mount', PART_BOOT, '/mnt/boot'], check=True)
    print('BOOT EFI')
    run(['mkdir -p /mnt/boot/efi'], check=True)
    run(['mount', PART_BOOT_EFI, '/mnt/boot/efi'], check=True)
    print('HOME')
    run(['mkdir -p /mnt/home'], check=True)
    run(['mount', PART_HOME, '/mnt/home'], check=True)
    print('TMP')
    run(['mkdir -p /mnt/tmp'], check=True)
    run(['mount', PART_TMP, '/mnt/tmp'], check=True)

    run(['lsblk', '/dev/sda'], check=True)
    r = (input('Tudo certo? (y/N)') or 'n').lower()
    if r != 'y' or r == 'n':
        run(['exit 0'], check=True)

except Exception as e:
    print(e)

# print(input('Tudo certo? '))
