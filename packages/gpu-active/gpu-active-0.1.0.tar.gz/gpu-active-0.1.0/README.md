# get_gpu

`get_gpu` is a Python package that simplifies GPU management in PyTorch projects. It helps users activate a GPU (if available) and move data to GPU memory for faster training and inference.

---

## Features

- Automatically detect and use the GPU if available, else fallback to CPU.
- Transfer tensors or datasets to the selected device.
- Wrap PyTorch DataLoader to seamlessly move data to the GPU during iteration.

---

## Installation

Install the package directly from PyPI:

```bash
pip install get-gpu
