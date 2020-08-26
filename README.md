# ImageGoblin

#### changelog v0.4.0:
+ added slugify option to make filenames web and script safe
+ new goblin
+ bug fixes
+ misc code clean up and improvements

### This Program:
+ is a web scraping tool specifically for the discovery and retrieval of images on a web server, in the highest possible quality
+ is a personal project designed according to my own needs
+ is a work in progress

### Requirements
+ Python 3.6+

### Operation
+ *default*: will try to match the input url(s) to a specific goblin. the matched goblin(s) will download what images they can according to their rule sets, in the highest possible quality. if no goblin is matched a generic goblin is used. if a text file is used as input, only the filename of the text file should be input using the --local argument and the text file should be placed in the same directory that the program will be ran from. it should contain 1 url per line.

  *examples:*

  ```
  image-goblin --verbose https://www.website.com/pages/somewebpage.html

  image-goblin https://www.website.com/files/cropped/image-600x600.jpg

  image-goblin --local urls.txt
  ```

+ *generic:* for any site without a specific goblin. by default, this goblin will automatically try to remove common cropping. using the '--format' option overrides this functionality and instead formats according to user input modifier(s). the usage format for this is '--format _mode_ _modifier_[ _replacement_]'. 'add _modifier_' will append the modifier to the end of the url; for example a query string. 'sub _modifier_ _replacement_' substitutes, while 'rem _modifier_' removes. the modifier can be a regular string or regex pattern. using the --noup flag prevents any automatic manipulation of urls. you can also enforce greedy mode with --greedy; sometimes this will find more images. be sure to quote the pattern as some terminals will remove backslashes.

  *examples:*

  ```
  image-goblin -f rem '-\d+x\d+' https://website.com/pages/somewebpage.html

  image-goblin --format sub 'size=\w+' size=large https://website.com/uploadsimage_01.jpg?size=some_size
  ```

+ *iterate:* when provided a url to a single image, the program will try to download that image and all other images with the same url structure that are on the server (but not necessarily displayed on the website). the iterable needs to be surrounded by '#' on either side when input to indicate the portion of the url to be iterated. use the --step argument to set step size (default 1); negative values will iterate down. set --timeout 0 to prevent timing out.

  *example:*

  ```
  image-goblin --timeout 10 --delay 3 https://website.com/uploads/image_#01#.jpg
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

#### NOTE: instagram recently took the nuclear option and seemingly banned all non residential ips. currently logging in is required if you are using a vpn/proxy.
+ *instagram:* this goblin will scrape an entire profile by default. stories require the user to be logged in; pass the --login flag to do so. the number of posts to retrieve can also be specified with --posts n (n < 100). finally, if 'latest' or 'recent' are passed as the --mode argument, the program will only retrieve the main stories (if logged in) and the six most recent posts. note, using a scraper while logged in is likely to get your account suspended.

    *examples:*

    ```
    image-goblin --login --mode recent https://www.instagram.com/username/

    image-goblin --posts 30 --force instagram username
    ```

+ *feed:* using the feed flag, you can accumulate urls by inputting them one by one. this is useful for accumulating urls as you find them while browsing the web, and downloading all at once. press "enter" with an empty input when finished. try it :)

#### Misc:
  + this program has only been tested on linux but should work on windows/mac as well.
  + the install script is optional and linux specific. it only serves to add a symlink to /usr/local/bin so that the program can be run from the shell with 'image-goblin' instead of 'python3 /path/to/image_goblin.py or ./image_goblin.py'.
  + a specific goblin can be forced using '--force _goblin_'.
  + a random delay (0<=n<=10) can be used with --delay -1
  + the --format input needs to be exact so make sure modifiers/spaces have not been erroneously added or left out.
  + if little or no (relevant) images are found then the page is probably generated dynamically with javascript which the program does not handle. you can also try with the --noup/--greedy handles.


#### PLEASE USE RESPONSIBLY :)
