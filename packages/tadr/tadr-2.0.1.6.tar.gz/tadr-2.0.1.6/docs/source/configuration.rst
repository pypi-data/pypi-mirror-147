Configuration
==============

There are a number of configuration options hardcoded into the program, in the ``Static`` class in ``core/classes.py``. These can be edited by manually changing the values. I may implement a proper settings menu at a later point.

The following is an explanation of what each configuration option does:

.. list-table::
   :header-rows: 1
   
   * - Name
     - Type
     - Description
   * - authors
     - Array
     - The list of users that TADR will check messages from. Only contains "transcribersofreddit" by default.Set to False by default.
   * - limit
     - Integer
     - The number of messages TADR will retrieve each cycle, always starting with the most recent message. Set to 10 by default.
   * - log_updates
     - Boolean
     - Determines whether or not TADR will write the log to a file. Set to False by default.
   * - messages
     - Array
     - Contains all of the terms TADR searches for in messages it checks. Contains only the beginning of the r/TranscribersOfReddit bot's response by default.
   * - reply
     - String
     - The message TADR replies with.
   * - sleep
     - Integer
     - The number of seconds TADR waits in-between cycles. Set to 10 by default.
   * - splitter
     - String
     - Used in conjunction with messages; each message from the bot will be split into sections using this value as its separator. For a value in messages to be detected, it must be the *entire first section* in a message. The splitter is set to "." by default.
   * - verbose
     - Boolean
     - Determines whether or not TADR will send a desktop notification for every message it replies to. Set to True by default.
