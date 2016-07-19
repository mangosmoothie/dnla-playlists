# dnla-playlists
Dynamically build DNLA playlists

## Setup
1. [download and install](https://www.python.org/downloads/) python 3.5 or greater
2. verify python version
3. 
    ```
    $ python --version
    ```
or

    ```
    $ python3 --version
    ```
3. installing and configuring virtualenv and virtualenvwrapper is not required but highly recommended. You will have to configure virtualenvwrapper for you environment after installing.

    ```
    $ pip install virtualenv virtualenvwrapper
    ```

## Running the playlist generator
1. [Optionally] create a new virtualenv and activate it
2. Load the dependencies from requirements.txt

    ```
    $ pip install -r /path/to/requirements.txt
    ```
3. Run the script - you can drop it in at the root of the directory tree you wish to traverse or use the optional parameters to define the root directory to search and the output dir for the playlists

    ```
    $ python playlists.py [--start-at /path/to/root] [--outdir /path/to/outdir]
    ```
4. Help is also available

    ```
    $ python playlists.py -h
    ```

    ```
    Usage: playlists.py [options]

    Options:
    -h, --help            show this help message and exit
    -n NAME, --name=NAME  NAME of playlist
    -s DIR, --start-at=DIR DIR location to start media file search from (default is current DIR)
    -e, --extended        use m3u extended format (has additional media metadata)
    -a, --absolute        use absolute file paths (default is relative paths)
    -d DEPTH, --depth=DEPTH depth to search, 0 for target dir only (default is fully recursive)
    -o DIR, --outdir=DIR  DIR location of output file(s) (default is current DIR)
    -c SUBSTR, --contains=SUBSTR case insensitive match on given string, i.e. "string contains SUBSTR". Checks file names and metadata.
    -r EXP, --regex=EXP   regex match. checks file name and metadata
    -f, --force           force execution through warnings
    ```


### Examples
1. Create a playlist of all songs in and under current directory by Billy Joel (search filenames and metadata - i.e. artist - if available):

    ```
    $ python playlists.py -c "Billy Joel"
    ```
2. Create a playlists of all songs in and under current directory

    ```
    $ python playlists.py -r ".*"
    ```
