# Enriching Streaming Data from Kafka or Redpanda

- Skill level
    
    **Intermediate, some knowledge of Kafka/Redpanda required**
    
- Time to complete
    
    **Approx. 15 min**
    

Introduction: *This example will cover how to write a dataflow to support inline data enrichment. Data enrichment is the process of adding to or enhancing data to make it more suitable or useful for a specific purpose. It is most often the result of joining additional data from a 3rd party database or another internal data source. For this specific example we will consume a stream of IP addresses from a Redpanda topic as input, enrich them with third party data to determine the location of the IP address, and then produce data to Kafka. This example will leverage the built-in kafka input and kafka output to do so.*

## ****Prerequisites****

**Kafka/Redpanda**
Kafka and Redpanda can be used interchangeably, but we will use Redpanda in this demo for the ease of use it provides. We will use [Docker Compose](https://docs.docker.com/compose/) to start a local Redpanda cluster.

https://github.com/bytewax/kafka-data-enrichment/blob/a2a37c1391521aa141550405a6e6c8087d32eb12/docker-compose.yaml#L1-L30

**Python modules**

bytewax[kafka]==0.16.*
requests==2.28.0

**Data**

The data source for this example is under the [data directory](https://github.com/bytewax/kafka-data-enrichment/tree/a2a37c1391521aa141550405a6e6c8087d32eb12/data) It will be loaded to the Redpanda cluster via the [utility script](https://github.com/bytewax/kafka-data-enrichment/blob/a2a37c1391521aa141550405a6e6c8087d32eb12/utils/utils.py) in the repository.

## Your Takeaway

*Enriching streaming data inline is a common pattern. This tutorial will show you how you can do this with Python and provide you with code you can modify to build your own enrichment pipelines.*

## Table of content

- Resources
- Step 1. Redpanda Overview
- Step 2. Constructing the Dataflow
- Step 3. Running the Dataflow
- Summary

## Resources

[Github Repo](https://github.com/bytewax/kafka-data-enrichment)

## Step 1. Redpanda Overview

[Redpanda](https://docs.redpanda.com/docs/get-started/intro-to-events/) is a streaming platform that uses a kafka compatible API as a way to interface with the underlying system. Redpanda is a pub/sub style system where you can have many producers writing to one topic and many consumers subscribed to, and receiving the same data. Like Kafka, Redpanda has the concept of partitioned topics, which can be read from independently, and increase throughput of a topic.

Since Redpanda shares many of the same concepts and the same interface as Kafka, Bytewax can consume from a Redpanda cluster in a similar way. The code we will write in the next sections will not be required to change regardless of whether you are using Redpanda or Kafka.

## Step 2. ****Constructing the Dataflow****

Every dataflow will contain, at the very least an input and an output. In this example the data input source will be a kafka topic and the output sink will be another kafka topic. Between the input and output lies the code used to transform the data. This is illustrated by the diagram below.

<img width="600" alt="dataflow diagram" src="https://user-images.githubusercontent.com/6073079/194627909-9f5d7b52-7fbb-4137-8b0e-1163469a9c75.png">

Let's walk through constructing the input, the transformation code and the output.

**Redpanda Input**

Bytewax has a concept of built-in, configurable input sources. At a high level, these are sources that can be configured and will be used as the input for a dataflow. The [`KafkaInput`](https://bytewax.io/apidocs/bytewax.connectors/kafka) is one of the more popular input sources. It is important to note that a connection will be made on each worker, which allows each worker to read from a disjoint set of partitions for a topic.

https://github.com/bytewax/kafka-data-enrichment/blob/a2a37c1391521aa141550405a6e6c8087d32eb12/dataflow.py#L8-L15

In the code snippet, we have first initialized an empty `Dataflow` object, and used the `input` method to define our input. The input method takes two arguments, the `step_id` and the `input_config`. The `step_id` is used for recovery purposes and the input configuration is where we will use the `KafkaInput` to set up our dataflow to consume from Redpanda.

_A Quick Aside on Recovery: Bytewax can be configured to checkpoint the state of a running Dataflow. When recovery is configured, `KafkaInput` will store offset information so that when a dataflow is restarted, input will resume from the last completed checkpoint. This makes it easy to get started working with data in Kafka, as managing consumer groups and offsets is not neccessary._

**Data Transformation**

[Operators](https://docs.bytewax.io/apidocs/bytewax.dataflow) are Dataflow class methods that define how data will flow through the dataflow. Whether it will be filtered, modified, aggregated or accumulated. In this example we are modifying our data in-flight and will use the `map` operator. The `map` operator takes a Python function as an argument which will be called for every input item.

https://github.com/bytewax/kafka-data-enrichment/blob/a2a37c1391521aa141550405a6e6c8087d32eb12/dataflow.py#L18-L33

In the code above, we are making an http request to an external service. This is only for demonstration purposes as issuing an http request to an external system for each item can be slow.

**Redpanda Output**

To capture data that is transformed in a dataflow, we will use the `output` method. Similar to the input method, it takes a configuration class as an argument. As with `KafkaInput`, Bytewax has a built-in output configuration for Kafka [`KafkaOutput`](https://docs.bytewax.io/apidocs/bytewax.outputs#bytewax.outputs.KafkaOutput). We will configure our Dataflow to write the enriched data to a second topic: `ip_address_by_location`.

https://github.com/bytewax/kafka-data-enrichment/blob/a2a37c1391521aa141550405a6e6c8087d32eb12/dataflow.py#L35

## Step 3. Deploying the Dataflow

To run this tutorial, we will need to start our local redpanda cluster, and populate it with data.

``` bash
❯ docker-compose up -d
[+] Running 1/1
 ✔ Container redpanda-1  Started
```

Now that Redpanda is running, we'll use our utility script to populate it with sample data:

``` bas
❯ python ./utils/utils.py
input topic ip_address_by_country created successfully
output topic ip_address_by_location created successfully
input topic ip_address_by_location populated successfully
```

The only thing left to do is run our dataflow:

``` bash
❯ python -m bytewax.run dataflow:flow
(b'Country', b'{"ip": "IP Address", "city": null, "region": null, "country_name": null}')
(b'United States', b'{"ip": "76.132.87.205", "city": "Antioch", "region": "California", "country_name": "United States"}')
(b'China', b'{"ip": "117.35.153.78", "city": "Xi\'an", "region": "Shaanxi", "country_name": "China"}')
(b'China', b'{"ip": "61.237.226.46", "city": "Beijing", "region": "Beijing", "country_name": "China"}')
(b'Germany', b'{"ip": "194.245.212.229", "city": "D\\u00fcsseldorf", "region": "North Rhine-Westphalia", "country_name": "Germany"}')
...
```


## Summary

In this tutorial we learned how to build a Dataflow to enrich data read from Kafka.

## We want to hear from you!

If you have any trouble with the process or have ideas about how to improve this document, come talk to us in the #troubleshooting Slack channel!

## Where to next?

- Relevant explainer video
- Relevant case study
- Relevant blog post
- Another awesome tutorial

See our full gallery of tutorials →

[Share your tutorial progress!](https://twitter.com/intent/tweet?text=I%27m%20mastering%20data%20streaming%20with%20%40bytewax!%20&url=https://bytewax.io/tutorials/&hashtags=Bytewax,Tutorials)
