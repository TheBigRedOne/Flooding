# 主 Makefile

# 路径
VAGRANTFILE = Vagrantfile
APP_DIR = /home/vagrant/mini-ndn/flooding/Applications
RESULTS_DIR = results
EXTERNAL_RESULTS_DIR = results

# 启动 Vagrant 虚拟机
start-vagrant:
	vagrant up --provider virtualbox

# 编译 consumer 和 producer
compile-applications:
	vagrant ssh -c 'cd $(APP_DIR) && make all'

# 生成密钥
generate-keys:
	vagrant ssh -c 'cd /home/vagrant/mini-ndn/flooding && \
	ndnsec key-gen /example && \
	ndnsec cert-dump -i /example > example-trust-anchor.cert && \
	ndnsec key-gen /example/testApp && \
	ndnsec sign-req /example/testApp | ndnsec cert-gen -s /example -i example | ndnsec cert-install -'

# 运行实验脚本 test.py
run-test:
	vagrant ssh -c 'cd /home/vagrant/mini-ndn/flooding && sudo python3 test.py'

# 退出 Mini-NDN
quit-minindn: 
	vagrant ssh -c 'echo quit | minindn'

# 复制结果文件到外部目录
copy-results:
	mkdir -p $(EXTERNAL_RESULTS_DIR)
	vagrant ssh -c 'cp /home/vagrant/mini-ndn/flooding/consumer.log /vagrant/$(RESULTS_DIR)/'
	vagrant ssh -c 'cp /home/vagrant/mini-ndn/flooding/producer.log /vagrant/$(RESULTS_DIR)/'
	cp $(RESULTS_DIR)/*.log $(EXTERNAL_RESULTS_DIR)/

# 停止 Vagrant 虚拟机
stop-vagrant:
	vagrant halt

# 清理 Vagrant 虚拟机
clean-vagrant:
	vagrant destroy -f

# 运行所有步骤
all: start-vagrant compile-applications generate-keys run-test quit-minindn copy-results stop-vagrant
