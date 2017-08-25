The home of the still-to-be-written TAsk LIst GENerator, aka taligen.

# To build on Arch Linux

1. On your Arch Linux development machine, clone this repository:
```
git clone https://github.com/taligen/taligen.git
cd taligen
```

2. Build the package:
```
makepkg
```

# To install on Arch Linux or UBOS
```
sudo pacman -U taligen-*.pkg*
```

# To run on Arch Linux or UBOS
```
taligen <tl-file>
```
or, with parameters:
```
taligen <tl-file> <key1>=<value1> <key2>=<value2>
```
such as:
```
taligen full.tl app=DragonFriends time=future
```
This will generate a JSON file that taliworkdown can render.
