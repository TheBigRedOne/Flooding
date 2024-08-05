# Applications/Makefile

# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++17 $(shell pkg-config --cflags --libs libndn-cxx)

# Targets
CONSUMER = consumer
PRODUCER = producer

# Source files
CONSUMER_SRC = consumer.cpp
PRODUCER_SRC = producer.cpp

# Build consumer
$(CONSUMER): $(CONSUMER_SRC)
	$(CXX) $(CXXFLAGS) -o $(CONSUMER) $(CONSUMER_SRC)

# Build producer
$(PRODUCER): $(PRODUCER_SRC)
	$(CXX) $(CXXFLAGS) -o $(PRODUCER) $(PRODUCER_SRC)

# Phony targets
.PHONY: all clean

# Build all
all: $(CONSUMER) $(PRODUCER)

# Clean build artifacts
clean:
	rm -f $(CONSUMER) $(PRODUCER)
