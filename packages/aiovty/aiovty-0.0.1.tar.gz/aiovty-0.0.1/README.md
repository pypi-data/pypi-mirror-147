- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)

# Description

`aiovty` is an asynchronous implementation of the VTY protocol.

# Installation

Install the last released version using `pip`:

```shell
python3 -m pip install --user -U aiovty
```

Or install the latest version from sources:

```shell
git clone git@github.com:matan1008/aiovty.git
cd aiovty
python3 -m pip install --user -U -e .
```

# Usage

To create a client, you need to supply the server's prompt name (e.g. `'Router'`):

```python
from aiovty import AioVtyClient

vty = AioVtyClient('Router')
```

Then you can connect giving address:

```python
connection_string = await vty.connect('127.0.0.1', 23)
```

Note that connecting returns the "connection string", which is the data sent before the first prompt.

After connection you can send your command:

```python
command_response = await vty.command(b'show ip')
```

You can also enter enabled mode:

```python
await vty.enable()
```

And initialize a configure terminal:

```python
await vty.configure_terminal()
await vty.command(b'router rip')
print(vty.node)  # Prints `config-router`
```