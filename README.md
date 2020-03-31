# web goblin v1.5 by xioren

### changelog v1.5:
  + homogenize variable names
  + removed --all argument
  + modified hungry goblin behavior
  + removed strings module
  + new handlers
  + removed unused handlers
  + code cleanup
  + bug fixes

### this program:
  + is designed to automate the discovery and retrieval of media on a web server.
  + is a work in progress.

### operation:

+ *default:* inputting either a url or a text file with links (1 per line) will try to match the link(s) to a specific handler. the handler will download what images it can according to its rule set, in the highest possible quality. if no handler is matched a generic handler is used. if a text file is used, only the filename should be input, using the --local argument and the text file should be placed in the directory that the program will be ran from.

  *examples*

  ```
  goblin https://www.website.com/files/image01.jpg

  goblin https://www.website.com/pages/somewebpage.html --force handler

  goblin --local links.txt --silent
  ```

+ *generic:* for any site without a specific handler. greedy. strings can be added, substituted, or removed using a _modifier_. input the _modifier_ as the format argument. 'add _modifier_' will append the modifier to the end of the url; for example a query string. 'sub _modifier_ _replacement_' substitutes, while 'rem _modifier_' removes.

    *examples*

    *rem _modifier_:*

    ```
    goblin https://website.com/uploads/image_01-300x300.jpg -f rem -\d+x\d+
    ```

    https://website.com/uploads/image_01-300x300.jpg

    becomes

    https://website.com/uploads/image_01.jpg

    *sub _modifier_ _replacement_:*

    ```
    goblin https://website.com/uploads/image_01.jpg?size=small --format sub size=\w+ size=large'
    ```

    https://website.com/uploads/image_01.jpg?size=small

    becomes

    https://website.com/uploads/image_01.jpg?size=large

+ *iterate:* when provided a url to a single file (usually an image), the program will try to download that file and all other files with the same url structure that are on the server (but not necessarily displayed on the website). the iterable needs to be surrounded by '%%%' on either side when input to indicate the portion of the url to be iterated.

    *example:*

    ```
    goblin https://website.com/uploads/image_%%%01%%%.jpg --timeout 10 --rate 3
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

+ *instagram:* partial support. for now, this handler will only parse the html of an instagram page that is saved to a txt file. the file should be named 'html.txt' and placed in the directory that this program is ran from. this handler will take a while to complete. the url to the instagram page or username needs to be input when ran. if only the username is passed, it is necessary to --force instagram in order to match the correct handler.

+ *feed:* using the feed argument, you can accumulate urls by inputting them one by one using the --feed mode. this is useful for accumulating urls as you find them while browsing the web, and downloading all at once.   

*misc:*
  + for the generic handler, inputting '-f auto' as an option will try to remove some common cropping patterns from image urls.
  + a specific handler can be forced using '--force _handler_'.
  + all available handlers can be listed using '-l or --list'.
  + the format input needs to be exact so make sure elements/spaces/commas have not been erroneously added or left out.
  + if little or no (relevant) images are found then the page is probably generated dynamically with javascript which the program can not handle.
