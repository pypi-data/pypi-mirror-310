# TaiwanID

## Introduction

This is a package for Taiwan ID card number validation, generation and parsing.

## Installation

```bash
pip install taiwanid
```

## Usage

```python
from taiwanid import TaiwanID

# Validate Taiwan ID card number
id_number = 'A123456789'
print(TaiwanID.validate(id_number))
# out TaiwanID.ValidateStatus.SUCCESS
```

More examples can be found in the [examples](examples) directory.

---

```bash
pip install -e .
```
