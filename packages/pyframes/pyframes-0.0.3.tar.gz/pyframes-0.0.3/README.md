# pyframes
Python package for interfacing with the frames.ai database.

## Install
```
pip3 install pyframes
```

## Example
Get your JWT from [spothole.sensorit.io/api/](https://spothole.sensorit.io/api/).
```
from pyframes import frames
f = frames.Frames()
f.set_jwt("<jwt>")
record = f.get_record(1)
print(record.id)
```
