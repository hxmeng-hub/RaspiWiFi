import os
import re

def install_prereqs():
	os.system('clear')
	os.system('apt update')
	os.system('clear')
	os.system('apt install python3 python3-rpi.gpio python3-pip dnsmasq hostapd -y')
	os.system('clear')
	print("Installing Flask web server...")
	print()
	os.system('pip3 install flask pyopenssl')
	os.system('clear')

def copy_configs(wpa_enabled_choice):
	is_installed = os.path.exists("/etc/raspiwifi")
	if is_installed:
		print('raspiwifi is already installed, this will overwrite the installation.\n')
		os.system('rm -rf /usr/lib/raspiwifi/*')
		os.system('rm -rf /etc/raspiwifi/*')
		os.system('rm -rf /etc/cron.raspiwifi/*')
		os.system('rm -f /etc/wpa_supplicant/wpa_supplicant.conf')

	else:
		os.system('mkdir /etc/raspiwifi')
		os.system('mkdir /usr/lib/raspiwifi')
		os.system('mkdir /etc/cron.raspiwifi')

		os.system('mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.original')
		os.system('mv /etc/dnsmasq.conf /etc/dnsmasq.conf.original')
		os.system('mv /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.conf.original')
		os.system('mv /etc/dhcpcd.conf /etc/dhcpcd.conf.original')
		os.system('touch /etc/raspiwifi/host_mode')
	
	os.system('rm -f ./tmp/*')
	os.system('cp -a libs/* /usr/lib/raspiwifi/')
	# wpa_supplicant is updated later
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/dhcpcd.conf /etc/')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/dnsmasq.conf /etc/')

	if wpa_enabled_choice.lower() == "y":
		os.system('cp /usr/lib/raspiwifi/reset_device/static_files/hostapd.conf.wpa /etc/hostapd/hostapd.conf')
	else:
		os.system('cp /usr/lib/raspiwifi/reset_device/static_files/hostapd.conf.nowpa /etc/hostapd/hostapd.conf')
	
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/aphost_bootstrapper /etc/cron.raspiwifi')
	os.system('chmod +x /etc/cron.raspiwifi/aphost_bootstrapper')
	with open("/etc/crontab", "r+") as crontab:
		if "cron.raspiwifi" not in crontab.read():
			crontab.write("# RaspiWiFi Startup\n")
			crontab.write("@reboot root run-parts /etc/cron.raspiwifi/\n") 

	os.system('mv /usr/lib/raspiwifi/reset_device/static_files/raspiwifi.conf /etc/raspiwifi')
	

def update_main_config_file(entered_ssid, auto_config_choice, auto_config_delay, ssl_enabled_choice, server_port_choice, wpa_enabled_choice, wpa_entered_key):
	if entered_ssid != "":
		os.system('sed -i \'s/RaspiWiFi Setup/' + entered_ssid + '/\' /etc/raspiwifi/raspiwifi.conf')
	if wpa_enabled_choice.lower() == "y":
		os.system('sed -i \'s/wpa_enabled=0/wpa_enabled=1/\' /etc/raspiwifi/raspiwifi.conf')
		os.system('sed -i \'s/wpa_key=0/wpa_key=' + wpa_entered_key + '/\' /etc/raspiwifi/raspiwifi.conf')
	if auto_config_choice.lower() == "y":
		os.system('sed -i \'s/auto_config=0/auto_config=1/\' /etc/raspiwifi/raspiwifi.conf')
	if auto_config_delay != "":
		os.system('sed -i \'s/auto_config_delay=300/auto_config_delay=' + auto_config_delay + '/\' /etc/raspiwifi/raspiwifi.conf')
	if ssl_enabled_choice.lower() == "y":
		os.system('sed -i \'s/ssl_enabled=0/ssl_enabled=1/\' /etc/raspiwifi/raspiwifi.conf')
	if server_port_choice != "":
		os.system('sed -i \'s/server_port=12345/server_port=' + server_port_choice + '/\' /etc/raspiwifi/raspiwifi.conf')
