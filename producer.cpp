#include <ndn-cxx/face.hpp>
#include <ndn-cxx/security/key-chain.hpp>
#include <iostream>
#include <chrono>
#include <thread>
#include <memory>  // Include for std::make_shared

class Producer {
public:
    Producer(const ndn::Name& prefix, int dataRate)
    : m_prefix(prefix), m_dataRate(dataRate), m_face()
    {
        m_face.setInterestFilter(m_prefix,
                                 [this](const auto& filter, const auto& interest) { this->onInterest(interest); },
                                 ndn::RegisterPrefixSuccessCallback(),
                                 [this](const ndn::Name& prefix, const std::string& reason) { this->onRegisterFailed(prefix, reason); });
    }

    void run() {
        try {
            m_face.processEvents();
        } catch (const std::exception& e) {
            std::cerr << "ERROR: " << e.what() << std::endl;
        }
    }

private:
    void onInterest(const ndn::Interest& interest) {
        // 创建一个与兴趣包名称相同的数据包
        auto data = std::make_shared<ndn::Data>(interest.getName());
        
        // 设置数据包的内容
        std::string content = "Hello, responding to " + interest.getName().toUri();
        data->setContent(std::string_view(content));
        
        // 签名数据包
        m_keyChain.sign(*data);
        
        // 发送数据包给消费者
        m_face.put(*data);

        // 控制发送速率
        std::this_thread::sleep_for(std::chrono::milliseconds(1000 / m_dataRate));
    }

    void onRegisterFailed(const ndn::Name& prefix, const std::string& reason) {
        std::cerr << "ERROR: Failed to register prefix '" << prefix << "' in local hub's daemon (" << reason << ")" << std::endl;
        m_face.shutdown();
    }

    ndn::Face m_face;
    ndn::KeyChain m_keyChain;
    ndn::Name m_prefix;
    int m_dataRate;  // Data rate in packets per second
};

int main(int argc, char* argv[]) {
    ndn::Name prefix("/example/producer");
    int dataRate = 25;  // Send 25 packets per second

    Producer producer(prefix, dataRate);
    std::cout << "Producer running for prefix " << prefix << std::endl;
    producer.run();

    return 0;
}
