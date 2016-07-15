# dnla-playlists
Dynamically build DNLA playlists

## Setup
1. [download and install](https://www.python.org/downloads/) python 3.5 or greater
2. verify python version
        $ python --version
   or
        $ python3 --version
3. installing and configuring virtualenv and virtualenvwrapper is not required but highly recommended. You will have to configure virtualenvwrapper for you environment after installing.
        $ pip install virtualenv virtualenvwrapper

## Running the playlist generator
1. [Optionally] create a new virtualenv and activate it
2. Load the dependencies from requirements.txt
        $ pip install -r /path/to/requirements.txt
3. Run the script - you can drop it in at the root of the directory tree you wish to traverse or use the optional parameters to define the root directory to search and the output dir for the playlists
        $ python playlists.py [--start-at /path/to/root] [--outdir /path/to/outdir]
4. Help is also available
        $ python playlists.py -h


### Notes
Right now it only writes regular m3u format. Extended m3u (artist name, song length) is coming soon.

Right now, it only searches for and writes Billboard 100 by the pre-determined file naming convention and directory structure. Search strings will be added soon.
