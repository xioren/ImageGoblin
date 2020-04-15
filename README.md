# ImageGoblin

#### changelog v0.2.1:
+ after adding new features over the last few versions, lots of new bugs sprang up. this
  release revolves around fixing them.

### This Program:

+ is a web scraping tool specifically for the discovery and retrieval of images on a web server, in the highest possible quality
+ is a work in progress

### Requirements

+ Python 3.6+

### Operation

+ *default*: inputting either a url or a text file containing urls (1 per line) will try to match the url(s) to a specific goblin. the goblin will download what images it can according to its rule set, in the highest possible quality. if no goblin is matched a generic goblin is used. if a text file is used, only the filename should be input using the --local argument and the text file should be placed in the same directory that the program will be ran from.

  *examples:*

  ```
  goblin https://www.website.com/pages/somewebpage.html

  goblin https://www.website.com/files/cropped/image.jpg --force goblin

  goblin --local urls.txt --silent
  ```

+ *generic:* for any site without a specific goblin. greedy. by default, this mode will automatically try to remove common cropping. Using the '--format' option overrides this functionality and instead formats according to user input modifier(s). the usage format for this is '--format _mode_ _modifier_[ _replacement_]'. 'add _modifier_' will append the modifier to the end of the url; for example a query string. 'sub _modifier_ _replacement_' substitutes, while 'rem _modifier_' removes.

  *examples:*

  ```
  goblin https://website.com/pages/somewebpage.html -f rem -\d+x\d+
  ```

  https://website.com/uploads/image_01-300x300.jpg

  becomes

  https://website.com/uploads/image_01.jpg


  ```
  goblin https://website.com/uploads/image_01.jpg?size=small --format sub size=\w+ size=large'
  ```

  https://website.com/uploads/image_01.jpg?size=small

  becomes

  https://website.com/uploads/image_01.jpg?size=large

+ *iterate:* when provided a url to a single image url, the program will try to download that images and all other images with the same url structure that are on the server (but not necessarily displayed on the website). the iterable needs to be surrounded by '#' on either side when input to indicate the portion of the url to be iterated.

  *example:*

  ```
  goblin https://website.com/uploads/image_#01#.jpg --timeout 10 --delay 3
  ```

  the program will then iterate through and download all images it can find with that url structure on the server.

  * https://website.com/uploads/image_01.jpg
  * https://website.com/uploads/image_02.jpg
  * https://website.com/uploads/image_03.jpg
  * https://website.com/uploads/image_04.jpg
  * https://website.com/uploads/image_05.jpg
  * ...
  * https://website.com/uploads/image_107.jpg

  etc...

+ *instagram:* input the instagram page url or username. if only the username is passed, it is necessary to --force instagram in order to match the correct goblin.

+ *feed:* using the feed argument, you can accumulate urls by inputting them one by one using the --feed mode. this is useful for accumulating urls as you find them while browsing the web, and downloading all at once.   

#### Misc:
  + the install script is optional and linux specific. it only serves to add a symlink to /usr/local/bin so that the program can be run from the shell with 'goblin' instead of 'python3 /path/to/image_goblin.py'.
  + a specific goblin can be forced using '--force _goblin_'.
  + all available goblins can be listed using '-l or --list'.
  + the --format input needs to be exact so make sure modifiers/spaces have not been erroneously added or left out.
  + if little or no (relevant) images are found then the page is probably generated dynamically with javascript which the program can not handle. you can also try with the --noupgrade handle.
