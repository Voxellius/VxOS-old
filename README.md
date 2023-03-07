# VxOS
The small and efficient operating system that powers Voxellius's devices.

## Simulator
In order to use the simulator, you must install the required Python modules. To do this, run:

```bash
pip3 install -r requirements.txt
```

To run the VxOS simulator, run:

```bash
python3 src/code.py
```

## Uploading to a device
To upload the system files to a CircuitPython device, run (where `$DESTINATION_PATH` is the path of the mounted device):

```bash
./upload.sh $DESTINATION_PATH
```

This command will only upload the files that have been changed but have not yet been commited on git to save time. Add the `--force` argument to force all system files to be uploaded, or the path to a file (excluding the leading `src/`) as an argument to force an unchanged file to be uploaded.