# Edit V Rising character names

This will search for all occurrences of a name in the save files and change them to a new name.

**MAKE BACKUPS OF YOUR SAVE FILES BEFORE RUNNING**

I have tested this, but I can't guarantee it won't mess up your save files.

## Steps
- Shut down your server
- **Make a backup of the latest AutoSave_? directory**
- Run this and point it to the latest AutoSave_? directory
- Restart server

## Run example
```
pip install -r requirements.txt

python3 edit-vrising-name.py F:\SteamLibrary\steamapps\common\VRising\VRising_Server\save-data\Saves\v1\world1\AutoSave_1 old_name:new_name old_name2:new_name2 old_name3:new_name3
```

## Run example (Windows)
* Download latest [release](https://github.com/ricin/vrising-tools/releases)
* Run and extract to a location
* Run `edit-vrising-name.exe` within extracted directory at the command prompt.
```
edit-vrising-name.exe F:\SteamLibrary\steamapps\common\VRising\VRising_Server\save-data\Saves\v1\world1\AutoSave_1 old_name:new_name old_name2:new_name2 old_name3:new_name3
```

## Run example via docker
```
docker run -it --rm -v /path/to/autosaves:/saves ricin/edit-vrising-name old_name:new_name old_name2:new_name2 old_name3:new_name3
```
