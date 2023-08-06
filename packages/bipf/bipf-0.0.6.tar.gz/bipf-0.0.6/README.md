# BIPF-Python
A Python library for BIPF (Binary In-Place Format)

See [https://github.com/ssbc/bipf](https://github.com/ssbc/bipf)
for the origin of BIPF and a description of the format.

Quick start (the interface is the same as in json and cbor2):

- install the library: ```python3 -m pip install bipf```
- in your code: ```from bipf import dumps, loads```
- ```dumps(<your_python_data>)``` serializes the object to bytes
- ```loads(<some_bipf_bytes>)``` restores a BIPF-serialized object

A rich demo in ```tests/demo.py``` also generates a testvector. The output is:

```
# encoded 80 bytes: f50418666f6f8c02127fff0a800a810aff0a000a010a7f12800012007f1a0080000e002179656168061862616695014046726564686f6c6d4305413da6832fbc3f186261722868656c6c6f1862617a06

# generator demo:
> 18666f6f 8c02127fff0a800a810aff0a000a010a7f12800012007f1a0080000e00217965616806
  > 0 127fff
  > 1 0a80
  > 2 0a81
  > 3 0aff
  > 4 0a00
  > 5 0a01
  > 6 0a7f
  > 7 128000
  > 8 12007f
  > 9 1a008000
  > 10 0e00
  > 11 2179656168
  > 12 06
> 18626166 95014046726564686f6c6d4305413da6832fbc3f
  > 4046726564686f6c6d 4305413da6832fbc3f
> 18626172 2868656c6c6f
> 1862617a 06

# parse entire object and read a single value
{'foo': [-129, -128, -127, -1, 0, 1, 127, 128, 32512, 32768, False, b'yeah', None], 'baf': {'Fredholm': 0.1101000100000001}, 'bar': 'hello', 'baz': None}
hello

# seek and decode a single value
key pos 69 --> hello
path pos 56 --> 0.1101000100000001
```

