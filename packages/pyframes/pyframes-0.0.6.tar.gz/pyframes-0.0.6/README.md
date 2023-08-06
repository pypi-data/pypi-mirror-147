# pyframes
Python package for interfacing with the frames.ai database.

## Install
```
pip3 install pyframes
```

## Example
Get your JWT from [spothole.sensorit.io/api/](https://spothole.sensorit.io/api/).
```
import pyframes
fm = pyframes.FramesManager()
fm.set_jwt("<jwt>")
record = fm.get_record(1)
print(record.id)
```
