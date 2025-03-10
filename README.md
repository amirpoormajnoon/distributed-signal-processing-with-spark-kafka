# distributed-signal-processing-with-spark-kafka
A distributed signal processing system using Apache Kafka and Apache Spark for real-time financial data processing. It generates trading signals with techniques like moving averages, RSI, and EMA. Docker is used for containerization, ensuring scalability and efficient signal analysis

## Project Structure

This project is divided into several components that work together to process financial signals and generate trading signals in a distributed manner.

### 1. **Producer**

The **Producer** is responsible for collecting financial data from a source (in this case, Kraken WebSocket API) and sending it to Kafka topics. This component processes the data and streams it into Kafka, which can then be consumed by other services for further processing.

**Files:**
- `producer.py`: Contains the logic to connect to Kraken API and send data to Kafka.
- `Dockerfile`: Used to containerize the producer component.

### 2. **Receiver**

The **Receiver** listens to the Kafka topics where the financial data is published and processes the data further for analysis.

**Files:**
- `receiver.py`: Contains the logic for consuming data from Kafka topics.
- `Dockerfile`: Used to containerize the receiver component.

### 3. **Sender**

The **Sender** consumes the processed signals from Kafka and sends them to a specified external system via TCP/IP for further action (e.g., sending to an external broker or system for executing trades).

**Files:**
- `sender.py`: Contains the logic for receiving signals from Kafka and sending them via a socket.
- `Dockerfile`: Used to containerize the sender component.

### 4. **Signal Generator**

The **Signal Generator** uses Apache Spark to perform real-time data analysis, such as calculating moving averages, RSI, and EMA. It generates trading signals and sends them to a Kafka topic for further action.

**Files:**
- `signal_generator.py`: Contains the Spark logic for analyzing the data and generating trading signals.
- `Dockerfile`: Used to containerize the signal generation component.

### 5. **.gitignore**

The `.gitignore` file is used to specify which files and directories Git should ignore. This ensures that temporary files or files that are not relevant to the project (e.g., logs, compiled files) are not tracked in version control.

**Files:**
- `.gitignore`: Contains a list of files and directories to be excluded from Git tracking.

## Getting Started

To get started, you can clone this repository and build the necessary Docker containers.
