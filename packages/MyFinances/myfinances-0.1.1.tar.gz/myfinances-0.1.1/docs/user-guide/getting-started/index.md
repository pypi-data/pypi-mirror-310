# Quick Start

To get started with the MyFinances Python Client, follow these steps.

## Install

Install the package via pip:

```shell
pip install myfinances
```

## Initialize the Client

Create an instance of `MyFinancesClient` by specifying your API base URL and API key:

```python
from myfinances import MyFinancesClient

client = MyFinancesClient(base_url="https://api.myfinances.com", api_key="YOUR_API_KEY")
```

## Basic Usage

Here are some example usages to get you started:

### List All Invoices

```python
invoices = client.invoices.list_invoices()
print(invoices)
```

For more in-depth guides, see:
- [Installation](installation.md)
- [Configuration](configuration.md)
- [Usage](usage/core.md)