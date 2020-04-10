# ImageGoblin

#### changelog v0.1.9:
+ rebase
+ ongoing re-working of regex's
+ optimizations
+ added goblins
+ code cleanup
+ bug fixes

### This Program:

+ is a web scraping tool specifically for the discovery and retrieval of images on a webpage/server in the highest possible quality
+ is a work in progress

### Requirements

+ Python 3.6+

### Operation

+ *Default*: Inputting either a url or a text file containing urls (1 per line) will try to match the url(s) to a specific goblin. The goblin will download what images it can according to its rule set, in the highest possible quality. if no goblin is matched a generic goblin is used. If a text file is used, only the filename should be input, using the --local argument and the text file should be placed in the directory that the program will be ran from.

  *Examples:*

  ```
  goblin https://www.website.com/files/cropped/image.jpg

  goblin https://www.website.com/pages/somewebpage.html --force goblin

  python3 image_goblin.py --local urls.txt --silent
  ```

+ *Generic:* For any site without a specific goblin. Greedy. By default, this mode will automatically try to remove common cropping. Using the '--format' option overrides this functionality. The usage format is '--format _mode_ _modifier_[ _replacement_]'. 'add _modifier_' will append the modifier to the end of the url; for example a query string. 'sub _modifier_ _replacement_' substitutes, while 'rem _modifier_' removes.

  *Examples:*

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

+ *Iterate:* When provided a url to a single image url, the program will try to download that images and all other images with the same url structure that are on the server (but not necessarily displayed on the website). The iterable needs to be surrounded by '#' on either side when input to indicate the portion of the url to be iterated.

  *Example:*

  ```
  goblin https://website.com/uploads/image_#01#.jpg --timeout 10 --delay 3
  ```

  The program will then iterate through and download all images it can find with that url structure on the server.

  * https://website.com/uploads/image_01.jpg
  * https://website.com/uploads/image_02.jpg
  * https://website.com/uploads/image_03.jpg
  * https://website.com/uploads/image_04.jpg
  * https://website.com/uploads/image_05.jpg
  * ...
  * https://website.com/uploads/image_107.jpg

  etc...

+ *Instagram:* Input the instagram page url or username. If only the username is passed, it is necessary to --force instagram in order to match the correct goblin.

+ *Feed:* Using the feed argument, you can accumulate urls by inputting them one by one using the --feed mode. This is useful for accumulating urls as you find them while browsing the web, and downloading all at once.   

#### Misc:
  + A specific goblin can be forced using '--force _goblin_'.
  + All available goblins can be listed using '-l or --list'.
  + The format input needs to be exact so make sure modifiers/spaces have not been erroneously added or left out.
  + If little or no (relevant) images are found then the page is probably generated dynamically with javascript which the program can not handle. You can also try with the --noupgrade handle.
