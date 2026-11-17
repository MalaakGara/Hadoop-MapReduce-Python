# Docker Commands – Hadoop MapReduce Project

This document contains the Docker and Hadoop commands required to execute the MapReduce application.

## 1. Check Docker

Open Windows CMD and execute:

```cmd
docker --version
docker ps -a
```

The Hadoop environment uses three containers:

- `hadoop-master`
- `hadoop-slave1`
- `hadoop-slave2`

## 2. Start the Hadoop containers

If the containers have already been created, execute:

```cmd
docker start hadoop-master
docker start hadoop-slave1
docker start hadoop-slave2
```

Check that they are running:

```cmd
docker ps
```

## 3. Enter the master container

```cmd
docker exec -it hadoop-master bash
```

The following commands must be executed inside the master container.

## 4. Check Hadoop and Python

```bash
python3 --version
hadoop version
```

Check HDFS:

```bash
hadoop fs -ls /
hadoop fs -ls input
```

The input dataset should be available at:

```text
input/purchases.txt
```

If the dataset is already present, continue to Step 5.

If the dataset is not present, first copy the dataset from Windows CMD:

```cmd
docker cp data\purchases.txt hadoop-master:/root/purchases.txt
```

Then, inside the master container:

```bash
hadoop fs -mkdir -p input
hadoop fs -put -f /root/purchases.txt input/purchases.txt
```

## 5. Copy the Mapper and Reducer

Run these commands from Windows CMD, in the project root directory:

```cmd
docker cp src\mapper.py hadoop-master:/root/mapper.py
docker cp src\reducer.py hadoop-master:/root/reducer.py
```

Check the files inside the master:

```cmd
docker exec hadoop-master ls -l /root/mapper.py /root/reducer.py
```

## 6. Execute the Hadoop Streaming job

Enter the master:

```cmd
docker exec -it hadoop-master bash
```

Inside the master:

```bash
STREAMING_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar"
```

Remove the previous output directory:

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

Wait until the job finishes.

Expected status:

```text
completed successfully
```

## 7. Check the results

Display the output:

```bash
hadoop fs -cat output_sales_by_store/part-00000
```

Count the output records:

```bash
hadoop fs -cat output_sales_by_store/part-00000 | wc -l
```

Expected result for the project dataset:

```text
103
```

Check the output directory:

```bash
hadoop fs -ls output_sales_by_store
```

It should contain:

- `_SUCCESS`
- `part-00000`

## 8. Copy the results to Windows

Inside the master container:

```bash
hadoop fs -get output_sales_by_store/part-00000 /root/hadoop_output.txt
exit
```

Back in Windows CMD:

```cmd
docker cp hadoop-master:/root/hadoop_output.txt results\hadoop_output.txt
```

## 9. Hadoop Web Interfaces

Open the following URLs in a browser while the Hadoop containers are running:

| Interface | URL | Purpose |
|---|---|---|
| YARN ResourceManager | http://localhost:8088 | Monitor Hadoop applications |
| HDFS NameNode | http://localhost:50070 | Monitor HDFS and its files |

## 10. Stop the containers

When the work is finished, run in Windows CMD:

```cmd
docker stop hadoop-slave2
docker stop hadoop-slave1
docker stop hadoop-master
```

## Important Notes

- Do not execute Linux commands in Windows CMD unless they are preceded by `docker exec ...`.
- Commands such as `hadoop fs`, `python3`, and `ls` must be executed inside the master container.
- Commands such as `docker cp`, `docker start`, and `docker stop` are executed in Windows CMD.
- The Hadoop output directory must not already exist when launching a new job.
- The full dataset is not included in the GitHub repository. Each person who wants to execute the full Hadoop job must obtain the dataset separately.

**Important for a new computer:** these commands start containers that already exist. They do not create a new Hadoop cluster. A new computer needs the original Docker cluster creation configuration before it can run the Hadoop job.