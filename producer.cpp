#include <ndn-cxx/face.hpp>
#include <ndn-cxx/security/key-chain.hpp>
#include <iostream>
#include <memory>

class Producer {
public:
    Producer(const ndn::Name& prefix)
    : m_prefix(prefix), m_face()
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
        std::cout << "Received Interest: " << interest.getName() << std::endl;

        auto data = std::make_shared<ndn::Data>(interest.getName());
        std::string content = "Hello, responding to " + interest.getName().toUri();
        data->setContent(content);  // 使用正确的 setContent 方法

        m_keyChain.sign(*data);
        m_face.put(*data);

        std::cout << "Sent Data: " << data->getName() << std::endl;
    }

    void onRegisterFailed(const ndn::Name& prefix, const std::string& reason) {
        std::cerr << "ERROR: Failed to register prefix '" << prefix << "' in local hub's daemon (" << reason << ")" << std::endl;
        m_face.shutdown();
    }

    ndn::Face m_face;
    ndn::KeyChain m_keyChain;
    ndn::Name m_prefix;
};

int main(int argc, char* argv[]) {
    ndn::Name prefix("/example/producer");

    Producer producer(prefix);
    std::cout << "Producer running for prefix " << prefix << std::endl;
    producer.run();

    return 0;
}
