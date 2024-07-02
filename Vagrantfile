# -*- mode: ruby -*-
# vi: set ft=ruby :

$INSTALL_BASE = <<EOF
  sudo apt-get update
  sudo apt-get upgrade -y
  sudo apt-get install -y vim git build-essential python3-pip

  git clone https://github.com/named-data/mini-ndn.git /home/vagrant/mini-ndn
  cd /home/vagrant/mini-ndn
  sudo ./install.sh

  sudo pip3 install --upgrade pip
  sudo pip3 install minindn

  echo "export PATH=\$PATH:/usr/local/bin" >> /home/vagrant/.bashrc
EOF

$DOWNLOAD_FILES = <<EOF
  mkdir -p /home/vagrant/mini-ndn/flooding
  cd /home/vagrant/mini-ndn/flooding
  wget https://raw.githubusercontent.com/TheBigRedOne/Flooding/master/consumer.cpp
  wget https://raw.githubusercontent.com/TheBigRedOne/Flooding/master/producer.cpp
  wget https://raw.githubusercontent.com/TheBigRedOne/Flooding/master/compile.txt
  wget https://raw.githubusercontent.com/TheBigRedOne/Flooding/master/trust-schema.conf
  wget https://raw.githubusercontent.com/TheBigRedOne/Flooding/master/trust_anchor_generator.txt
  wget https://raw.githubusercontent.com/TheBigRedOne/Flooding/master/test.py
EOF

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.box_version = "202404.23.0"

  config.vm.network "private_network", type: "dhcp"

  config.vm.provider :virtualbox do |v|
    v.customize ["modifyvm", :id, "--memory", "32768"]
    v.customize ["modifyvm", :id, "--cpus", "12"]
  end

  config.vm.provision "shell", inline: $INSTALL_BASE, privileged: true

  config.vm.provision "shell", inline: $DOWNLOAD_FILES, privileged: false

  # 可选：运行特定的代码或脚本
  # config.vm.provision "shell", privileged: false, inline: <<-SHELL
  #   cd /home/vagrant/mini-ndn/flooding
  #   make
  #   ./run_experiment.sh
  # SHELL
end
