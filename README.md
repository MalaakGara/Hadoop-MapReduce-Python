# Hadoop-MapReduce-Python
### Total Sales by Store

A practical implementation of Hadoop MapReduce using Python and Hadoop Streaming to calculate the total sales for each store from a large purchases dataset.

## Project Overview

This project was developed as part of a Big Data practical assignment. Its purpose is to process a large collection of purchase transactions and calculate the total amount spent at each store.

The application uses the MapReduce programming model. Python scripts handle the Mapper and Reducer operations, while Apache Hadoop manages distributed processing and storage through HDFS.

The project was executed on a Hadoop cluster running in Docker.

## Technologies

- **Apache Hadoop 2.7.2** – Distributed data processing
- **Hadoop Streaming** – Running Python scripts as MapReduce tasks
- **Python 3** – Mapper and Reducer implementation
- **Docker** – Hadoop cluster environment
- **HDFS** – Input and output storage
- **Git and GitHub** – Source code management

## Dataset

The dataset contains purchase transactions with six fields:

| Field | Description |
|---|---|
| Date | Transaction date |
| Time | Transaction time |
| Store | Store name |
| Product | Purchased product |
| Cost | Transaction amount |
| Payment | Payment method |

The dataset used for the Hadoop execution contains approximately 4.1 million records and occupies around 211 MB.

The full dataset is not included in this repository because of its size.

## How It Works

The application follows four main stages:

1. **Map:** Read each transaction and extract the store name and purchase amount.
2. **Shuffle and Sort:** Hadoop groups and sorts the intermediate records by store.
3. **Reduce:** Add the purchase amounts belonging to the same store.
4. **Output:** Write one total sales value per store to HDFS.

### Example

**Mapper input:**

```text
2025-01-01  10:30  San Jose    Product A  120.50  Cash
2025-01-01  11:15  Fort Worth  Product B   75.25  Card
2025-01-01  12:00  San Jose    Product C   40.00  Card
```

**Mapper output:**

```text
San Jose    120.50
Fort Worth   75.25
San Jose     40.00
```

**Reducer output:**

```text
Fort Worth    75.25
San Jose     160.50
```

## Project Structure

```text
Hadoop-MapReduce-Python/
│
├── data/
│   └── .gitkeep
│
├── docker/
│   └── docker-commands.md
│
├── docs/
│   ├── screenshots/
│   └── report.md
│
├── results/
│   ├── local_output.txt
│   ├── hadoop_output.txt
│   └── .gitkeep
│
├── src/
│   ├── mapper.py
│   └── reducer.py
│
├── tests/
│   ├── purchases_sample.txt
│   └── test_local.sh
│
├── .gitignore
└── README.md
```

## Running the Project

### 1. Requirements

To run the project locally, you need:

- Python 3
- Git

To execute the complete Hadoop job, you also need:

- Docker
- A running Hadoop cluster
- The input dataset available in HDFS

### 2. Clone the Repository

```bash
git clone https://github.com/MalaakGara/Hadoop-MapReduce-Python.git
cd Hadoop-MapReduce-Python
```

### 3. Run the Local Test

The Mapper and Reducer can first be tested without Hadoop using the sample dataset.

On Windows CMD:

```cmd
type tests\purchases_sample.txt | python src\mapper.py | sort | python src\reducer.py
```

On Linux or Git Bash:

```bash
python3 src/mapper.py < tests/purchases_sample.txt | sort | python3 src/reducer.py
```

The expected output is:

```text
Fort Worth    647.08
San Jose      515.76
```

To save the local result:

```cmd
type tests\purchases_sample.txt | python src\mapper.py | sort | python src\reducer.py > results\local_output.txt
```

### 4. Run the Hadoop Job

The Hadoop environment used for this project consists of three Docker containers:

- `hadoop-master`
- `hadoop-slave1`
- `hadoop-slave2`

Start the existing containers from Windows CMD:

```cmd
docker start hadoop-master
docker start hadoop-slave1
docker start hadoop-slave2
```

Copy the Python scripts to the master container:

```cmd
docker cp src\mapper.py hadoop-master:/root/mapper.py
docker cp src\reducer.py hadoop-master:/root/reducer.py
```

Enter the master container:

```cmd
docker exec -it hadoop-master bash
```

Inside the container, define the Streaming JAR:

```bash
STREAMING_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar"
```

Remove the previous output directory if it exists:

```bash
hadoop fs -rm -r -f output_sales_by_store
```

Execute the MapReduce job:

```bash
hadoop jar "$STREAMING_JAR" \
-files /root/mapper.py,/root/reducer.py \
-mapper "python3 mapper.py" \
-reducer "python3 reducer.py" \
-input input/purchases.txt \
-output output_sales_by_store \
-numReduceTasks 1
```

The input file must already be available in HDFS at `input/purchases.txt`.

### 5. Retrieve the Results

Display the results:

```bash
hadoop fs -cat output_sales_by_store/part-00000
```

Count the output records:

```bash
hadoop fs -cat output_sales_by_store/part-00000 | wc -l
```

To save the output on the local computer, inside the master container:

```bash
hadoop fs -get output_sales_by_store/part-00000 /root/hadoop_output.txt
exit
```

Then, in Windows CMD:

```cmd
docker cp hadoop-master:/root/hadoop_output.txt results\hadoop_output.txt
```

## Results

The Hadoop job completed successfully on the full dataset.

The following values were obtained from the Hadoop execution report:

| Metric | Result |
|---|---:|
| Input records | 4,138,476 |
| Map output records | 4,138,476 |
| Map tasks | 2 |
| Reduce tasks | 1 |
| Reduce input groups | 103 |
| Reduce output records | 103 |
| Failed shuffles | 0 |
| Output file size | 2,204 bytes |

The final output contains 103 records, with one calculated sales total for each store.

The results are available in `results/hadoop_output.txt`.

## Monitoring the Hadoop Cluster

The Hadoop environment provides two web interfaces:

| Interface | Address | Description |
|---|---|---|
| YARN ResourceManager | http://localhost:8088 | View and monitor Hadoop applications |
| HDFS NameNode | http://localhost:50070 | Inspect HDFS and its storage information |

These interfaces can be accessed while the Hadoop containers are running.

## Repository Contents

- `src/` – Python Mapper and Reducer scripts.
- `tests/` – Sample dataset and local testing script.
- `data/` – Dataset directory.
- `docker/` – Docker and Hadoop execution commands.
- `results/` – Local and Hadoop output files.
- `docs/` – Project report and execution screenshots.

## Authors

**Project:** Hadoop MapReduce with Python  
**Application:** Total Sales by Store

Developed as part of a Big Data practical assignment at the Faculty of Sciences of Tunis, University of Tunis El Manar.

