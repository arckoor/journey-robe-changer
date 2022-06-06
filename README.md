# JourneyRobeChanger
A tool to quickly switch between saves in [Journey](https://store.steampowered.com/app/638230/Journey/).

**This tool is not maintaned, use https://journey.coldknife2.ninja/editor/ instead!**

## Usage
This script only works with the Steam version of the game. \
Extract the .zip folder to any place you like. \
Start `JourneyRobeChanger.exe` and follow the instructions. \
It is strongly advised to make a backup of your save before using this tool. \
Please only use this tool when the game is closed. \
**Make sure to disable Cloud-Save in Steam for Journey.**

## Automatic backup
This script automatically attempts to create a backup of your current save. \
It always prefers the save located in `C:\Users\%username%\AppData\Local\Annapurna Interactive\Journey\Steam`. \
If no save can be found it attempts to save from `%steam_dir%\userdata\%user_id%\638230\remote`. \
The backup will be located in the directory this script is contained in, under `.\presets\BACKUP.BIN`.


## The config file
`config.json` contains options to customize the behaviour of this script.
The default looks like this:
```
{
  "SteamID3": null,
  "create_backup": true,
  "clear_backup": false,
  "ask_restore": true,
  "ask_clear": true
}
```

`SteamID3` - the script will automatically fill this with your ID if it is required \
`create_backup` - set to `false` if you do not wish the script to automatically create a backup of you current save \
`clear_backup` - set to `true` if you would like the script to clear the last backup automatically \
`ask_restore` - set to `false` if you do not want to be asked to restore the current backup \
`ask_clear` - set to `false` if you do not want to be asked to delete the current backup

**Do not delete entries from the config file!** \
The script will detect invalid entries and automatically reset the file to default, therefore undoing all your customization.

## Presets
If you do not wish to use the script you can still manually replace the saves using the file in `.\presets`. \
The names directly correspond to the content of the file.
To learn which files to replace, visit the [Journey Wiki](https://journey.fandom.com/wiki/Hints_for_the_regularly_travelling_Wayfarer#Steam_version:_Backup_Savefiles). \
Use the `Backing up, restoring, or resetting a save` section for reference.

BB : start as **T4 WR**, with all previous symbols, from Broken Bridge \
PD : start as **T4 WR**, with all previous symbols, from Pink Desert \
SC : start as **T4 WR**, with all previous symbols, from Sunken City \
UG : start as **T4 WR**, with all previous symbols, from Underground \
TO : start as **T4 WR**, with all previous symbols, from Tower \
SN : start as **T4 WR**, with all previous symbols, from Snow \
T1 : start as **T1 RR**, from Broken Bridge \
T2 : start as **T2 RR (WR available)**, from Chapter Select \
T3 : start as **T3 RR (WR available)**, from Chapter Select \
T4 : start as **T4 RR (WR available)**, from Chapter Select

## Run the code yourself
If you want to run directly from source you only need python 3.x and the `colorama` package. \
To make an executable run `pyinstaller -F --icon=icon.ico JourneyRobeChanger.py`. \
The `.exe` will be located in the `.\dist` folder.
