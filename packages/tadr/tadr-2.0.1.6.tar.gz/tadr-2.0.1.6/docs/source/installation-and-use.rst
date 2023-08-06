Installation and Use
=====================

.. note:: TADR was created on Linux and, given the developer has no access to other operating systems, support for macOS and Windows is limited.

Requirements
-------------

In order to install TADR, you will need a version of Python installed. The program was written using 3.9, but anything 3.5 onwards should work. A minimum of 3.5 is required because that is when type-hinting, which TADR uses extensively, was added.

TADR also relies on some python packages:

- configparser, any version
- PRAW >= 7.5.0
- PyGObject ~= 3.42.0
- setuptools >= 57.0.0.

Installation
-------------

To install TADR,

1. Run either ``python -m pip install tadr`` or ``pip install tadr`` in your command line. It should automatically install the program as well as any dependencies.
2. Before doing anything else, you should now create an app for your Reddit account. You can do this by going to `the apps page in preferences <https://www.reddit.com/prefs/apps/>`_ and creating a new app:

    - Give it a name ("TADR" is easy to remember).
    - Choose "script".
    - Give it a description (which can really be anything you want).
    - Set an about url and redirect uri. The about url doesn't matter (I just linked the project's repository), and the redirect uri will not matter either; it is related to refresh tokens, which ADR does not currently support.
    
3. Now, in your console, run the command ``tadr`` and the program will create its config and data directories, in your config folder and home folder on Linux and macOS, or in AppData on Windows. It will then tell you that it is missing the ``praw.ini`` file, and you will need to set it up. This is a simple process, but you will need your client id and client secret, which you can see on `the apps page <https://www.reddit.com/prefs/apps/>`_.

    - Go to the page and scroll down until you find the bot you created. Underneath its name should be "personal use script", and below that a string of random characters. This is your client id. If you can't see a field that labeled "secret" with another, longer string of random characters after it, then click the edit button and it should appear (along with other fields you filled out when you were creating the bot).
    
    - TADR will then open a tab in your browser to complete the authentication process. Once you click 'allow', it will automatically append your refresh_token to ``praw.ini``. Once fully initialised, the contents of your praw.ini file should look something like this:::

    [tadr]
    client_id=lI3fAkE7x82LiE
    client_secret=4lS0f4Ke1234567894NdN0tR3aL
    redirect_uri = http://localhost:8080/users/auth/reddit/callback
    refresh_token = your refresh token here


4. After this is set up, you should be good to run the program! Remember: TADR does not check any messages that were already there when it was started, so you will need to start it before you begin transcribing and keep it running the whole time you are doing so if you want it to catch everything.

Updating
---------

To update the program to a newer version, run ``python -m pip install --upgrade tadr`` or ``pip install --upgrade tadr`` in your command line.

Using the Latest Testing Version
---------------------------------

To use the latest testing version, download the `testing branch files <https://github.com/MurdoMaclachlan/oscr/tree/testing>`_, extract the archive you have downloaded, and use ``pip install .`` after navigating into the directory the files were extracted to.
