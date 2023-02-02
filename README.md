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

## Step 1. Redpanda Overview

[Redpanda](https://docs.redpanda.com/docs/get-started/intro-to-events/) is a streaming platform that uses a kafka compatible API as a way to interface with the underlying system. Redpanda is a pub/sub style system where you can have many producers writing to one topic and many consumers subscribed to, and receiving the same data. Redpanda has the concept of topic partitions and these are used to increase parallelism and therefore throughput of a topic. Like Kafka, Redpanda has a concept of consumer groups to enable multiple consumers to read in a coordinated manner from a topic if you don't want every consumer to receive the same data. This allows you to increase the throughput and scale as your data scales.  

Since Redpanda shares many of the same concepts and the same interface as Kafka, Bytewax can consume from a Redpanda cluster in a similar way. The code we will write in the next sections will not be required to change regardless of whether you are using Redpanda or Kafka.

## Step 2. ****Constructing the Dataflow****

Every dataflow will contain, at the very least an input and an output. In this example the data input source will be a kafka topic and the output sink will be another kafka topic. Between the input and output lies the code used to transform the data. This is illustrated by the diagram below.

<img width="600" alt="dataflow diagram" src="https://user-images.githubusercontent.com/6073079/194627909-9f5d7b52-7fbb-4137-8b0e-1163469a9c75.png">

Let's walk through constructing the input, the transformation code and the output.

**Kafka Input**

Bytewax has a concept of built-in, configurable input sources. At a high level, these are code that can be configured and will be used as the input source for the dataflow. The [`KafkaInputConfig`](https://docs.bytewax.io/apidocs/bytewax.inputs#bytewax.inputs.KafkaInputConfig) is one of the more popular input sources. It is important to note that the input connection will be made on each worker, which allows the code to be parallelized across input partitions.

https://github.com/bytewax/kafka-data-enrichment/blob/a46b1b5877c44ccc6a8e4ae07e06d94ff2df144a/dataflow.py#L24-L30

In the code above, we have first initialized a Dataflow object, and used the `input` method to define our input. The input method takes two arguments, the `step_id` and the `input_config`. The `step_id` is used for recovery purposes and the input configuration is where we will use the `KafkaInputConfig` to set up our dataflow to consume from Kafka.

_A Quick Aside on Recovery: With Bytewax you can persist state in more durable formats. This is so that in the case that the dataflow fails, you can recover state and the dataflow will not be required to recompute from the beginning. This is oftentimes referred to as checkpointing for other processing frameworks. With the `KafkaInputConfig` configuring recovery will handle the offset and consumer groups for you. This makes it easy to get started working with data in Kafka._

**Data Transformation**

[Operators](https://docs.bytewax.io/apidocs/bytewax.dataflow) are Dataflow class methods that define how data will flow through the dataflow. Whether it will be filtered, modified, aggregated or accumulated. In this example we are modifying our data in-flight and will use the `map` operator. The `map` operator will receive a Python function as an argument and this will contain the code to modify the data payload.

https://github.com/bytewax/kafka-data-enrichment/blob/a46b1b5877c44ccc6a8e4ae07e06d94ff2df144a/dataflow.py#L9-L21

In the code above, we are making an http request to an external service, this is only for demonstration purposes. You should use something that is lower latency so you do not risk having the http request as a bottleneck or having network errors.

**Kafka Output**

To capture data that is transformed in a dataflow, we will use the `capture` method. Similar to the input method, it takes a configuration as the argument. Bytewax has built-in output configurations and [`KafkaOutputConfig`](https://docs.bytewax.io/apidocs/bytewax.outputs#bytewax.outputs.KafkaOutputConfig) is one of those. We are going to use it in this example to write out the enriched data to a new topic.

https://github.com/bytewax/kafka-data-enrichment/blob/a46b1b5877c44ccc6a8e4ae07e06d94ff2df144a/dataflow.py#L32-L34

### Kicking off execution

With the above dataflow written, the final step is to specify the execution method. Whether it will run as a single threaded process on our local machine or be capable of scaling across a Kubernetes cluster. The methods used to define the execution are part of the execution module and more detail can be found in the long format documentation as well as in the API documentation.

https://github.com/bytewax/kafka-data-enrichment/blob/a46b1b5877c44ccc6a8e4ae07e06d94ff2df144a/dataflow.py#L36-L39

There are two types of workers: worker threads and worker processes. In most use cases where you are running Python code to transform and enrich data, you will want to use processes.

## Step 3. Deploying the Dataflow

Bytewax dataflows can be run as you would a regular Python script `> python dataflow.py` for local testing purposes. Although the recommended way to run dataflows in production is to leverage the [waxctl command line tool](https://www.bytewax.io/docs/deployment/waxctl) to run the workloads on cloud infrastructure or on the [bytewax platform](https://www.bytewax.io/platform).

To run this tutorial, you will need to clone the repo to your machine and then run the `run.sh` script. Which will start a container running Redpanda, load it with sample data while building the docker image and then run the dataflow from the tutorial.

https://github.com/bytewax/kafka-data-enrichment/blob/b38c9579c35fce6c7ead71a1ea4115e3551dfcb5/run.sh#L1-L8

For informational purposes, the below steps will show you how you can use `waxctl` to run a Bytewax dataflow on one of the public clouds, like AWS, with very little configuration. You will need to have the AWS CLI installed and configured and you will also have to have your streaming platform (Redpanda or Kafka) accessible from the instance.

```bash doctest:SKIP
waxctl aws deploy kafka-enrichment.py --name kafka-enrichment \
  --requirements-file-name requirements-ke.txt
```

`waxctl` will configure and start an AWS EC2 instance and run your dataflow on the instance. To see the default parameters, you can run the help command and see them in the command line:

```bash doctest:SKIP
waxctl aws deploy -h                                               
Deploy a dataflow to a new EC2 instance.
​
The deploy command expects one argument, which is the path of your Python dataflow file.
By default, Waxctl creates a policy and a role that will allow the EC2 instance to store Cloudwatch logs and start sessions through Systems Manager.
​
Examples:
  # The default command to deploy a dataflow named "bytewax" in a new EC2 instance running my-dataflow.py file.
  waxctl aws deploy my-dataflow.py
​
  # Deploy a dataflow named "custom" using specific security groups and instance profile
  waxctl aws deploy dataflow.py --name custom \
    --security-groups-ids "sg-006a1re044efb2d23" \
    --principal-arn "arn:aws:iam::1111111111:instance-profile/my-profile"
​
Usage:
  waxctl aws deploy [PATH] [flags]
​
Flags:
  -P, --associate-public-ip-address     associate a public IP address to the EC2 instance (default true)
  -m, --detailed-monitoring             specifies whether detailed monitoring is enabled for the EC2 instance
  -e, --extra-tags strings              extra tags to apply to the EC2 instance. The format must be KEY=VALUE
  -h, --help                            help for deploy
  -t, --instance-type string            EC2 instance type to be created (default "t2.micro")
  -k, --key-name string                 name of an existing key pair
  -n, --name string                     name of the EC2 instance to deploy the dataflow (default "bytewax")
  -p, --principal-arn string            principal ARN to assign to the EC2 instance
      --profile string                  AWS cli configuration profile
  -f, --python-file-name string         python script file to run. Only needed when [PATH] is a tar file
      --region string                   AWS region
  -r, --requirements-file-name string   requirements.txt file if needed
      --save-cloud-config               save cloud-config file to disk for troubleshooting purposes
  -S, --security-groups-ids strings     security groups Ids to assign to the EC2 instance
  -s, --subnet-id string                the ID of the subnet to launch the EC2 instance into
​
Global Flags:
      --debug   enable verbose output
```


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
