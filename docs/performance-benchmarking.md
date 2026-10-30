# RiftTrace Performance Benchmarking

## Objective

The benchmark evaluates how RiftTrace execution performance changes
as the size of the modeled digital environment increases.

It measures software execution characteristics and does not measure
cyberattack probability or real-world security effectiveness.

## Primary Scalability Variable

The primary benchmark varies the approximate number of modeled assets:

- 100
- 500
- 1,000
- 5,000

Synthetic benchmark environments are derived from the same ingestion
template and connected so that graph traversal can span multiple
generated clusters.

## Primary Benchmark

The primary scalability benchmark uses the RiftTrace reachability
simulation because graph traversal is a foundational operation used
throughout the platform.

## Measurements

Each benchmark records:

- arithmetic mean latency
- median latency
- 95th-percentile latency
- minimum latency
- maximum latency
- peak Python-managed memory allocation measured with tracemalloc
- mean SQL query count

## Procedure

Each benchmark uses:

1. the same application version for all runs in a comparison;
2. warm-up executions before measurement;
3. repeated measured iterations;
4. the same stored request payload for baseline and optimized runs;
5. the same modeled environment for baseline and optimized runs.

## Optimization Rule

RiftTrace follows a measure-before-optimization policy.

Core simulation algorithms are not modified solely because code
appears inefficient. Profiling evidence is used to identify actual
execution bottlenecks.

After an optimization, the exact same benchmark is repeated and
recorded as the OPTIMIZED variant.

## Interpretation

An optimization is considered useful when it improves one or more
measured engineering characteristics without changing the expected
simulation result or causing regression-test failures.

Examples include:

- reduced execution latency;
- reduced SQL query count;
- reduced memory allocation;
- improved scalability at larger graph sizes.

## Limitations

Benchmark results depend on:

- hardware;
- operating system;
- Python version;
- database configuration;
- application configuration;
- background system activity;
- graph density and structure.

Therefore benchmark values should be interpreted as measurements of
the recorded test environment rather than universal RiftTrace
performance guarantees.
