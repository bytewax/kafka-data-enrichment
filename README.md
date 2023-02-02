# Enriching Streaming Data from Kafka

- Skill level
    
    **Beginner, no prior knowledge requirements**
    
- Time to complete
    
    **Approx. 15 min**
    

Introduction: *This example will cover how to write a dataflow to support in-line data enrichment. Data enrichment is the process of adding to or enhancing data to make it more suitable or useful for a specific purpose. It is most often the result of joining additional data from a 3rd party database or another internal data source. For this specific example we will consume a stream of IP addresses from Kafka as input, enrich them with third party data to determine the location of the IP address, and then produce data to Kafka. This example will leverage the built-in kafka input and kafka output to do so.*

## ****Prerequisites****

**Kafka/Redpanda**
To get started you will need a Kafka (Docker setup) or Redpanda (Docker setup) cluster running.

**Python modules**

pip install bytewax==0.15.0 requests==2.28.0 kafka-python==2.0.2

**Data**

The data source for this example is under the [data directory](/data/data.) in the [bytewax repo](https://github.com/bytewax/bytewax) and you can load it the data to the running kafka cluster with the code shown below. This code is outside of the scope of this example. It is creating an input and output topic and then writing some sample data to the topic.

## Your Takeaway

[What people can expect to gain from reading the tutorial]

*Your takeaway from this tutorial will be a streaming application that lets you aggregate data coming from a Kafka topic using Bytewax.*

## Table of content

- Resources
- Step 1
- Step 2
- Step 3
- Summary

## Resources

Github link

Jupyter Notebook link

Data sample link

## Step 1. Concepts

To start off, we are going to diverge into some concepts around markets, exchanges and orders.

### Concepts

Order book

Bid & Ask

Level 2 Data

## Step 2. ****Inputs & Outputs****

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
