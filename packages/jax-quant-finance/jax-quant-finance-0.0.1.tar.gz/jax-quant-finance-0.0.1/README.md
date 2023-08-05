# JAX-Quant-Finance: High Performance Quantative Finance on JAX

## Introduction

Inspired by [TF Quant Finance](https://github.com/google/tf-quant-finance), we developed a quantative finance library based on [JAX](https://github.com/google/jax). This library provides high-performance components leveraging the hardware
acceleration, parallel scientific computing and automatic differentiation of JAX. 

We can:

* run financial workloads on CPU/GPU/TPU with XLA acceleration

* calculate mathematical derivative of financial models, i.e. Greeks

* distribute workloads on multiple devices and machines

`examples` directory contains several demonstrations of using the JAX-Quant-Finance.

## Install

### JAX installation

You must first follow [JAX's installation guide](https://github.com/google/jax/#installation) to install JAX based on your device architecture (CPU/GPU/TPU).

### JAX-Quant-Finance

```
pip install jax-quant-finance --upgrade
```

### 64-bit precision

To enable 64-bit precision, set the respective JAX flag _before_ importing `jax_quant_finance` (see the JAX [guide](https://jax.readthedocs.io/en/latest/notebooks/Common_Gotchas_in_JAX.html#double-64bit-precision)), for example:

```python
from jax.config import config
config.update("jax_enable_x64", True)
```

