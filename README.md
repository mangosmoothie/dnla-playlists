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
    or
    ```
    $ pip3 install virtualenv virtualenvwrapper
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

### Notes
You can run the default which expects a very particular file structure (top 100 by year) or use the options to build your own playlist.

You can build your own playlists by searching through files and their metadata for a particular substring or even a regular expression. Searches are recursive through all directories from the root.
