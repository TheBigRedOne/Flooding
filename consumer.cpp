#include <ndn-cxx/face.hpp>
#include <ndn-cxx/util/scheduler.hpp>
#include <iostream>
#include <unordered_set>
#include <chrono>
#include <thread>
#include <boost/asio/io_context.hpp>

class Consumer {
public:
    Consumer(const ndn::Name& interestName, int maxInflightInterests, int requestIntervalMs)
    : m_interestName(interestName), m_face(m_ioContext), m_scheduler(m_ioContext), m_maxInflightInterests(maxInflightInterests), m_requestIntervalMs(requestIntervalMs)
    {
        sendInterests();
        m_scheduler.schedule(ndn::time::milliseconds(m_requestIntervalMs), [this] { this->periodicRequest(); });
    }

    void run() {
        try {
            m_ioContext.run();
        } catch (const std::exception& e) {
            std::cerr << "ERROR: " << e.what() << std::endl;
        }
    }

private:
    void periodicRequest() {
        sendInterests();
        m_scheduler.schedule(ndn::time::milliseconds(m_requestIntervalMs), [this] { this->periodicRequest(); });
    }

    void sendInterests() {
        while (m_inflightInterests.size() < m_maxInflightInterests) {
            ndn::Name nextInterestName = m_interestName;
            nextInterestName.appendSegment(m_nextSegment++);
            ndn::Interest interest(nextInterestName);
            interest.setInterestLifetime(ndn::time::milliseconds(1000));
            interest.setMustBeFresh(true);

            std::cout << "Sending Interest for: " << nextInterestName << std::endl;
            m_inflightInterests.insert(nextInterestName.toUri());
            m_face.expressInterest(interest,
                                   bind(&Consumer::onData, this, _1, _2),
                                   bind(&Consumer::onNack, this, _1, _2),
                                   bind(&Consumer::onTimeout, this, _1));
        }
    }

    void onData(const ndn::Interest& interest, const ndn::Data& data) {
        std::cout << "Received data: " << data.getName() << std::endl;
        m_inflightInterests.erase(interest.getName().toUri());
    }

    void onNack(const ndn::Interest& interest, const ndn::lp::Nack& nack) {
        std::cout << "Received NACK for: " << interest.getName() << " reason: " << nack.getReason() << std::endl;
        m_inflightInterests.erase(interest.getName().toUri());
    }

    void onTimeout(const ndn::Interest& interest) {
        std::cout << "Timeout for Interest: " << interest.getName() << std::endl;
        m_inflightInterests.erase(interest.getName().toUri());
    }

    boost::asio::io_context m_ioContext;
    ndn::Face m_face;
    ndn::Scheduler m_scheduler{m_ioContext};
    ndn::Name m_interestName;
    uint64_t m_nextSegment = 0;
    int m_maxInflightInterests;
    int m_requestIntervalMs;
    std::unordered_set<std::string> m_inflightInterests;
};

int main(int argc, char* argv[]) {
    ndn::Name interestName("/example/producer");
    int maxInflightInterests = 5;
    int requestIntervalMs = 5;

    Consumer consumer(interestName, maxInflightInterests, requestIntervalMs);
    std::cout << "Consumer running, requesting data from " << interestName << std::endl;
    consumer.run();

    return 0;
}
