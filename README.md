# distributed-signal-processing-with-spark-kafka
A distributed signal processing system using Apache Kafka and Apache Spark for real-time financial data processing. It generates trading signals with techniques like moving averages, RSI, and EMA. Docker is used for containerization, ensuring scalability and efficient signal analysis

## Project Structure

This project is divided into several components that work together to process financial signals and generate trading signals in a distributed manner.

### 1. **Producer**

The **Producer** is responsible for collecting financial data from a source (in this case, Kraken WebSocket API) and sending it to Kafka topics. This component processes the data and streams it into Kafka, which can then be consumed by Signal Generator services for further processing.

**Files:**
- `producer.py`: Contains the logic to connect to Kraken API and send data to Kafka.
- `Dockerfile`: Used to containerize the producer component.

### 2. **Signal Generator**

The **Signal Generator** component reads the data from a Kafka topic, where the **Producer** has already pushed the real-time financial data from the exchange. The **Signal Generator** processes this incoming data and performs various technical analyses to generate trading signals.


- **Real-time Data Processing**: Using **Apache Spark**, the component processes this data in real-time. Key financial indicators like **Moving Averages (MA)**, **Exponential Moving Averages (EMA)**, and **Relative Strength Index (RSI)** are calculated to evaluate market conditions.
  
  - **Moving Averages (MA)**: Short-term and long-term moving averages are computed to detect price trends.
  - **Exponential Moving Average (EMA)**: A weighted moving average that reacts more quickly to recent price changes.
  - **Relative Strength Index (RSI)**: A momentum indicator used to assess if a market is overbought or oversold.


**Files:**
- `signal_generator.py`: Contains the logic for reading data from Kafka, performing the analysis (MA, EMA, RSI), and generating trading signals.
- `Dockerfile`: Used to containerize the Signal Generator, ensuring consistent deployment across different environments.


### 3. **Sender**

The **Sender** consumes the processed signals from Kafka and sends them to a specified external system via TCP/IP for further action (e.g., sending to an external broker or system for executing trades).

**Files:**
- `sender.py`: Contains the logic for receiving signals from Kafka and sending them via a socket.
- `Dockerfile`: Used to containerize the sender component.

### 4. **Receiver**

The **Receiver** listens to the **Sender Service** and showing the analysised data .

**Files:**
- `receiver.py`: Contains the logic for consuming data from Kafka topics.
- `Dockerfile`: Used to containerize the receiver component.

### 5. **.gitignore**

The `.gitignore` file is used to specify which files and directories Git should ignore. This ensures that temporary files or files that are not relevant to the project (e.g., logs, compiled files) are not tracked in version control.

**Files:**
- `.gitignore`: Contains a list of files and directories to be excluded from Git tracking.

## Getting Started

To get started, clone this repository and install **PySpark**, **Kafka**, and **Docker** on your system. After that, build the container for each service and run them to start the real-time signal processing pipeline.
