# Vagrantfile路径
VAGRANTFILE = Vagrantfile

# Vagrant虚拟机启动
start-vagrant:
	vagrant up --provider virtualbox

# 编译consumer.cpp
compile-consumer: start-vagrant
	vagrant ssh -c 'cd /home/vagrant/mini-ndn/flooding && \
	g++ -std=c++17 -o consumer consumer.cpp $$(pkg-config --cflags --libs libndn-cxx)'

# 编译producer.cpp
compile-producer: start-vagrant
	vagrant ssh -c 'cd /home/vagrant/mini-ndn/flooding && \
	g++ -std=c++17 -o producer producer.cpp $$(pkg-config --cflags --libs libndn-cxx)'

# 运行trust_anchor_generator.txt中的命令
generate-keys: start-vagrant
	vagrant ssh -c "cd /home/vagrant/mini-ndn/flooding && \
	ndnsec key-gen /example && \
	ndnsec cert-dump -i /example > example-trust-anchor.cert && \
	ndnsec key-gen /example/testApp && \
	ndnsec sign-req /example/testApp | ndnsec cert-gen -s /example -i example | ndnsec cert-install -"

# 运行实验脚本test.py
run-test: compile-consumer compile-producer generate-keys
	vagrant ssh -c "cd /home/vagrant/mini-ndn/flooding && sudo python3 test.py"

# 复制结果文件
copy-results: run-test
	mkdir -p results
	vagrant ssh -c "cp /home/vagrant/mini-ndn/flooding/consumer.log /vagrant/results/"
	vagrant ssh -c "cp /home/vagrant/mini-ndn/flooding/producer.log /vagrant/results/"

# 关闭Vagrant虚拟机
stop-vagrant: copy-results
	vagrant halt

# 清理Vagrant虚拟机
#clean-vagrant:
#	vagrant destroy -f

# 运行所有步骤
all: stop-vagrant
