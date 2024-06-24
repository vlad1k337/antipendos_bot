#!/usr/bin/env bash

check_systemd() {
	if ! which systemctl &> /dev/null; then
		echo "USE SYSTEMD STUPID"
		exit
	fi
}

check_docker() {
	if [[ -d /nix || -d /etc/nixos ]]; then
		echo "STOP USE nix(OS)"
		exit
	elif which docker-compose &> /dev/null; then
		return
	else
		echo "Install docker and restart script"
		exit
	fi
}

run_docker() {
	if systemctl list-units | grep docker.s &> /dev/null; then
		echo
		echo "Runing docker compose..."
		$SUP docker compose up --watch
	else
		echo "Start docker"
		$SUP systemctl enable --now docker.socket
	fi
	
}

superuser() {
	if which sudo &> /dev/null; then
		echo sudo
	elif which doas &> /dev/null; then
		echo doas
	elif [ $EUID -ne 0 ]; then
		echo 
	else
		echo "run script with superuser premissions"
		exit
	fi
}

echo -e "\e[31mW\e[33me\e[32ml\e[34mc\e[35mo\e[36mm\e[31me \e[33mt\e[32mo \e[34mA\e[35mn\e[36mt\e[31mi\e[33mP\e[32me\e[34mn\e[35md\e[36mo\e[31ms \e[33mi\e[32mn\e[34ms\e[35mt\e[36ma\e[31ml\e[33ml\e[32me\e[34mr\e[35m!\n\e[36mF\e[31mo\e[33ml\e[32ml\e[34mo\e[35mw \e[36mt\e[31mh\e[33me \e[32mi\e[34mn\e[35ms\e[36mt\e[31mr\e[33mu\e[32mc\e[34mt\e[35mi\e[36mo\e[31mn\e[33ms \e[32mt\e[34mo \e[35ms\e[36mt\e[31ma\e[33mr\e[32mt \e[34mA\e[35mn\e[36mt\e[31mi\e[33mP\e[32me\e[34mn\e[35md\e[36mo\e[31ms\e[33ms\e[0m"

if [ ! -s token.env ]; then
	echo -en "\nEnter your bot token..."
	read -r wtf
	echo "$wtf" > token.env
fi

check_systemd
check_docker
SUP=$(superuser)
run_docker
