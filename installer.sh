#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "See yah, you're not root."
  exit 1
fi

SDA = '/dev/sda'
PART_BOOT = '/dev/sda1'
PART_BOOT_EFI = '/dev/sda2'
PART_ROOT = '/dev/sda3'
PART_HOME = '/dev/sda4'

loadkeys br-abnt2

ping -c 3 archlinux.org

timedatectl set-ntp true

cfdisk SDA

mkfs.ext2 -L BOOT PART_BOOT

mkfs.fat -F32 PART_BOOT_EFI

mkfs.btrfs -f -L ROOT PART_ROOT

mkfs.btrfs -f -L HOME PART_HOME

mount PART_ROOT /mnt

mkdir -p /mnt/boot

mount PART_BOOT /mnt/boot

mkdir -p /mnt/boot/efi

mount PART_BOOT_EFI /mnt/boot/efi

mkdir -p /mnt/home
mount PART_HOME /mnt/home

lsblk SDA

echo 'Are okay? (Y/n)'
read ok

if [ -n "$ok" ] && [ "$ok" != "Y" ] && [ "$ok" != "y" ]; then
  echo 'See yah!'
  exit 0
fi

pacstrap -i /mnt base base-devel linux-zen linux-firmware vim sudo grub efibootmgr btrfs-progs

genfstab -U /mnt >/mnt/etc/fstab

arch_chroot "sed -i '/pt_BR/,+1 s/^#//' '/etc/locale.gen'"

arch_chroot "locale-gen"

arch_chroot "echo LANG='pt_BR'.'UTF-8' > /etc/locale.conf"

arch_chroot "echo LANG='pt_BR'.'UTF-8' > /etc/locale.conf"

arch_chroot "sed -i '/multilib\\]/,+1 s/^#//' '/etc/pacman.conf'"

arch_chroot "pacman -Syy"

arch_chroot "echo juliocesar > /etc/hostname"

arch_chroot "echo '127.0.0.1\tlocalhost' > /etc/hosts"

arch_chroot "pacman -S xorg-server xorg-xinit xf86-video-intel mesa plasma konsole dolphin networkmanager --noconfirm"

arch_chroot "systemctl enable NetworkManager sddm"

arch_chroot "useradd -m -g users -G 'log,sys,wheel,rfkill,dbus' -s /bin/bash julio"

arch_chroot "passwd"

arch_chroot "sed -i '/%wheel ALL=(ALL) ALL/s/^#//' /etc/sudoers"

arch_chroot "mkinitcpio -P"

arch_chroot "grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=grub --recheck"

arch_chroot "grub-mkconfig -o /boot/grub/grub.cfg"

arch_chroot() {
  arch-chroot /mnt /bin/bash -c "${1}"
}
