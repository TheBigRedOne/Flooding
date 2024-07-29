# -*- mode: ruby -*-
# vi: set ft=ruby :

$INSTALL_BASE = <<EOF
  sudo apt-get update
  sudo apt-get upgrade -y
  sudo apt-get install -y vim git ubuntu-desktop build-essential pkg-config python3-minimal libboost-all-dev libssl-dev libsqlite3-dev libpcap-dev libsystemd-dev
  sudo pip3 install --upgrade pip

  # Clone and install ndn-cxx from source
  git clone https://github.com/named-data/ndn-cxx.git /home/vagrant/ndn-cxx
  cd /home/vagrant/ndn-cxx
  ./waf configure
  ./waf build
  sudo ./waf install
  sudo ldconfig

  #Clone and install mini-ndn
  git clone --branch v0.6.0 https://github.com/named-data/mini-ndn.git /home/vagrant/mini-ndn
  cd /home/vagrant/mini-ndn
  ./install.sh

  # Change ownership of the mini-ndn folder to vagrant user
  sudo chown -R vagrant:vagrant /home/vagrant/mini-ndn

  echo "export PATH=\$PATH:/usr/local/bin" >> /home/vagrant/.bashrc
EOF

$DOWNLOAD_FILES = <<EOF
  #Clone Flooding project
  git clone https://github.com/TheBigRedOne/Flooding.git /home/vagrant/mini-ndn/flooding
EOF

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.box_version = "202404.23.0"

  config.vm.network "private_network", type: "dhcp"

  config.vm.provider :virtualbox do |v|
    v.customize ["modifyvm", :id, "--cpus", "12"]
    v.customize ["modifyvm", :id, "--memory", "32768"]
    v.customize ["modifyvm", :id, "--vram", "256"]
    
  end

  config.vm.provision "shell", inline: $INSTALL_BASE, privileged: false
  config.vm.provision "shell", inline: $DOWNLOAD_FILES, privileged: false

  config.vm.provider "virtualbox" do |vb|
    vb.gui = true
  end
  
end
