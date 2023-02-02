# Enriching Streaming Data from Kafka or Redpanda

- Skill level
    
    **Intermediate, some knowledge of Kafka/Redpanda required**
    
- Time to complete
    
    **Approx. 15 min**
    

Introduction: *This example will cover how to write a dataflow to support inline data enrichment. Data enrichment is the process of adding to or enhancing data to make it more suitable or useful for a specific purpose. It is most often the result of joining additional data from a 3rd party database or another internal data source. For this specific example we will consume a stream of IP addresses from a Redpanda topic as input, enrich them with third party data to determine the location of the IP address, and then produce data to Kafka. This example will leverage the built-in kafka input and kafka output to do so.*

## ****Prerequisites****

**Kafka/Redpanda**
Kafka and Redpanda can be used interchangeably, but we will use Redpanda in this demo for the ease of use it provides. To get started you will need Redpanda [rpk installed](https://docs.redpanda.com/docs/get-started/rpk-install/). The [startup script]() in the tutorial repository will start a Redpanda cluster.

**Python modules**

bytewax==0.15.0
requests==2.28.0
kafka-python==2.0.2

**Data**

The data source for this example is under the [data directory](/data/dataset.txt.) It will be loaded to the Redpanda cluster upon running the [startup script]() in the repository.

## Your Takeaway

*Enriching streaming data inline is a common pattern. This tutorial will show you how you can do this with Python and provide you with code you can modify to build your own enrichment pipelines.*

## Table of content

- Resources
- Step 1. Redpanda Overview
- Step 2. Constructing the Dataflow
- Step 2. Deploying the Dataflow
- Summary

## Resources

[Github Repo](https://github.com/bytewax/kafka-data-enrichment)

## Step 1. Concepts

[Redpanda](https://docs.redpanda.com/docs/get-started/intro-to-events/) is a streaming platform that uses a kafka compatible API as a way to interface with the underlying system. Redpanda is a pub/sub style system where you can have many producers writing to one topic and many consumers subscribed to, and receiving the same data. Redpanda has the concept of topic partitions and these are used to increase parallelism and therefore throughput of a topic. Like Kafka, Redpanda has a concept of consumer groups to enable multiple consumers to read in a coordinated manner from a topic if you don't want every consumer to receive the same data. This allows you to increase the throughput and scale as your data scales.  

Since Redpanda shares many of the same concepts and the same interface as Kafka, Bytewax can consume from a Redpanda cluster in a similar way. The code we will write in the next sections will not be required to change regardless of whether you are using Redpanda or Kafka.

## Step 2. ****Constructing the Dataflow****

Every dataflow will contain, at the very least an input and an output. In this example the data input source will be a kafka topic and the output sink will be another kafka topic. Between the input and output lies the code used to transform the data. This is illustrated by the diagram below.

<img width="600" alt="dataflow diagram" src="https://user-images.githubusercontent.com/6073079/194627909-9f5d7b52-7fbb-4137-8b0e-1163469a9c75.png">

Let's walk through constructing the input, the transformation code and the output.

**Kafka Input**

Bytewax has a concept around input configurations. At a high level, these are code that can be configured and will be used as the input source for the dataflow. The [`KafkaInputConfig`](https://docs.bytewax.io/apidocs/bytewax.inputs#bytewax.inputs.KafkaInputConfig) is one of the more popular input configurations. It is important to note that the input connection will be made on each worker.



## Step 3. …

## Summary

That’s it, you are awesome and we are going to rephrase our takeaway paragraph

## We want to hear from you!

If you have any trouble with the process or have ideas about how to improve this document, come talk to us in the #troubleshooting Slack channel!

## Where to next?

- Relevant explainer video
- Relevant case study
- Relevant blog post
- Another awesome tutorial

See our full gallery of tutorials →

[Share your tutorial progress!](https://twitter.com/intent/tweet?text=I%27m%20mastering%20data%20streaming%20with%20%40bytewax!%20&url=https://bytewax.io/tutorials/&hashtags=Bytewax,Tutorials)
