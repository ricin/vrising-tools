# Edit V Rising character names

This will search for all occurrences of a name in the save files and change them to a new name.

**MAKE BACKUPS OF YOUR SAVE FILES BEFORE RUNNING**

I have tested this, but I can't guarantee it won't mess up your save files.

## Steps

- Shut down your server
- **Make a backup of your saves directory**
- Run this and point it to the saves directory that contains *.save.gz files
- Restart server


## Usage
```
usage: edit-vrising-name.py [-h] [-f [SAVE_FILE]] [-c] [-v] save_path rename_pair [rename_pair ...]

Edit character names within V Rising save files

positional arguments:
  save_path             Path to directory containing save files to edit
  rename_pair           Pair of old and new name in the form of old_name:new_name

options:
  -h, --help            show this help message and exit
  -f [SAVE_FILE], --file [SAVE_FILE]
                        Path to specific file to edit
  -c, --compress        Compress save file after editing
  -v, --verbose         More verbose output with debug information
```

## Run example
```
pip install -r requirements.txt

python3 edit-vrising-name.py F:\SteamLibrary\steamapps\common\VRising\VRising_Server\save-data\Saves\v3\world1 old_name:new_name old_name2:new_name2 old_name3:new_name3
```

## Run example (Windows)
* Download latest [release](https://github.com/ricin/vrising-tools/releases)
* Run and extract to a location
* Run `edit-vrising-name.exe` within extracted directory at the command prompt.
```
edit-vrising-name.exe F:\SteamLibrary\steamapps\common\VRising\VRising_Server\save-data\Saves\v3\world1 old_name:new_name old_name2:new_name2 old_name3:new_name3
```

## Run example via docker
```
docker run -it --rm -v /path/to/autosaves:/saves ricin/edit-vrising-name old_name:new_name old_name2:new_name2 old_name3:new_name3
```

> If you want to edit a specific file, you can use the `-f` flag to specify the file name.

```
docker run -it --rm -v /path/to/autosaves:/saves ricin/edit-vrising-name -f AutoSave_1.save.gz old_name:new_name old_name2:new_name2 old_name3:new_name3
```