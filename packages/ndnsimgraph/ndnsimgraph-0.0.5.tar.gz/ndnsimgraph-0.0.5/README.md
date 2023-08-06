# ndnsim-graph

A small graph package used to draw image for ndnsim metrics

## 1. Install

```bash
pip install ndnsimgraph
```

## 2. Usage Example
### 2.1 Throughput

```python
from ndnsimgraph.throughput import ThroughputGraph, ThroughputType, ThroughputTarget

# save picture to file
ThroughputGraph.parse("data_test0409/wfq-test2_throughput.txt"). \
        setThroughputType(ThroughputType.OutData). \
        setThroughputTarget(ThroughputTarget.Kilobytes). \
        setSamplingInterval(0.5). \
        plot("C1", 258). \
        plot("C2", 258). \
        plot("C3", 258). \
        plot("C4", 258). \
        title("test title"). \
        xlabel("Throughputs"). \
        ylabel("Times(s)"). \
        legend(). \
        drawAndSave("output", "test-throughput.svg"). \
        close()

# show
ThroughputGraph.parse("data_test0409/wfq-test2_throughput.txt"). \
        setThroughputType(ThroughputType.OutData). \
        setThroughputTarget(ThroughputTarget.Kilobytes). \
        setSamplingInterval(0.5). \
        plot("C1", 258). \
        plot("C2", 258). \
        plot("C3", 258). \
        plot("C4", 258). \
        title("test title"). \
        xlabel("Throughputs"). \
        ylabel("Times(s)"). \
        legend(). \
        drawAndSave("output", "test-throughput.svg"). \
        close()
```

![test-throughput.svg](doc/test-throughput.svg)

### 2.2 Delay

```python
from ndnsimgraph.delay import DelayGraph, DelayType, DelayTarget

DelayGraph.parse("data_content_delivery/delay_abilene.txt"). \
        setDelayType(DelayType.LastDelay). \
        setDelayTarget(DelayTarget.DelayMS). \
        setSamplingInterval(0.1). \
        plot("C1", 1). \
        plot("C1", 2). \
        title("test title"). \
        xlabel("Delay(ms)"). \
        ylabel("Times(s)"). \
        legend(). \
        drawAndSave("output", "test-delay.svg"). \
        close()
```

![test-delay.svg](doc/test-delay.svg)




## 3. Upload new packet

> [Python 打包自己的库到 PYPI （可pip安装）](https://zhuanlan.zhihu.com/p/79164800)

```bash
python3 setup.py sdist bdist_wheel
twine upload dist/*
```