# web goblin by xioren v1.1



### changelog v1.2:
  + significant reworking and optimizing of all modules
  + code cleanup

### this program:
  + is designed to automate the discovery and retrieval of media on a web server.
  + is a work in progress.

### operation:

+ *mode 1 (default):* parses and downloads media from a supplied url. strings can be added, substituted, or removed from urls as well. input the string you want modified in the format box. 'add' mode will append the element to the end of the url; for example a query string. 'sub' mode substitutes strings, while 'rem' removes them.

    *rem mode:*
    inputting: 'rem -\d+x\d+'

    https://website.com/uploads/image_01-300x300.jpg

    becomes

    https://website.com/uploads/image_01.jpg

    *sub mode:*
    inputting: 'sub \?=\w ?=large' (?=large will be subbed in for anything matching the regex pattern \?=\w)

    https://website.com/uploads/image_01.jpg?=cropped

    becomes

    https://website.com/uploads/image_01.jpg?=large

+ *mode 2:* when provided a url to a single file (instead of entire page), the program will try to download that file and all other files with the same url structure that are on the server (but not necessarily displayed on the website). the iterable needs to be surrounded by '%%%' on either side when input to indicate the portion of the url to be iterated.

    *example:*

    image url: https://website.com/uploads/image_01.jpg

    url to submit: https://website.com/uploads/image_%%%01%%%.jpg

    the program will then iterate through and download all images it can find with that url structure on the server.

    * https://website.com/uploads/image_01.jpg
    * https://website.com/uploads/image_02.jpg
    * https://website.com/uploads/image_03.jpg
    * https://website.com/uploads/image_04.jpg
    * https://website.com/uploads/image_05.jpg
    * ...
    * https://website.com/uploads/image_100.jpg

    etc...

+ *mode 3 (instagram):* this is an instagram specific mode with partial support. for now, the program will only parse the html of an instagram page that is saved to a txt file. the file should be named 'html.txt' and placed in the download folder. this mode will take a while to complete. the url to the instagram page needs to be input when ran.

*misc:*
  + for mode 1, inputting 'auto' as format argument will try to remove some common cropping from image urls.

*troubleshooting:*
  + the format input needs to be exact so make sure elements/spaces/commas have not been erroneously added or left out.
  + error while parsing usually* happens when the server returns a 403 error or is improperly configured.
  + failed to open url could mean the scheme is not present. i.e. https://
  + failed to parse url usually means the format of the image url does not match any regex pattern in the program.
  + if little or no (relevant) images are found then the page is probably generated dynamically with javascript which the program can not handle.
