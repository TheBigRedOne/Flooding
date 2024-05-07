#include <ndn-cxx/face.hpp>
#include <iostream>
#include <chrono>
#include <thread>

class Consumer {
public:
    Consumer(const ndn::Name& interestName)
    : m_interestName(interestName), m_face()
    {
        // 创建 Interest 对象
        ndn::Interest interest(interestName);
        interest.setInterestLifetime(ndn::time::milliseconds(1000));  // 设置兴趣包的生存时间为1000毫秒
        interest.setMustBeFresh(true);  // 设置兴趣包要求返回最新的数据

        m_face.expressInterest(interest,
                               bind(&Consumer::onData, this, _1, _2),
                               bind(&Consumer::onNack, this, _1, _2),
                               bind(&Consumer::onTimeout, this, _1));
        std::cout << "Interest sent for: " << interestName << std::endl;
    }

    void run() {
        try {
            m_face.processEvents();
        } catch (const std::exception& e) {
            std::cerr << "ERROR: " << e.what() << std::endl;
        }
    }

private:
    void onData(const ndn::Interest&, const ndn::Data& data) {
        std::cout << "Received data: " << data << std::endl;
    }

    void onNack(const ndn::Interest&, const ndn::lp::Nack& nack) {
        std::cout << "Received NACK: " << nack.getReason() << std::endl;
    }

    void onTimeout(const ndn::Interest& interest) {
        std::cout << "Timeout for interest: " << interest.getName() << std::endl;
    }

    ndn::Face m_face;
    ndn::Name m_interestName;
};

int main(int argc, char* argv[]) {
    ndn::Name interestName("/example/producer");  // 与生产者程序的前缀相对应
    Consumer consumer(interestName);
    std::cout << "Consumer running, requesting data from " << interestName << std::endl;
    consumer.run();

    return 0;
}
