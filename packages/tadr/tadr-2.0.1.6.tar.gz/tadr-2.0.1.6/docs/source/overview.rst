Overview
=========

**This is an unofficial program. It is not officially endorsed by the Transcribers of Reddit or the Grafeas Group; they are in no way involved with or liable for this program or any matters relating to it. It is developed unofficially, in my capacity as a volunteer, NOT a moderator.**

The ToR Auto Done Replier, abbreviated to TADR, is a program that automatically replies to certain Reddit message from the `r/TranscribersOfReddit <https://www.reddit.com/r/TranscribersOfReddit>`_ bot.

After receiving a "done" comment, the `r/TranscribersOfReddit <https://www.reddit.com/r/TranscribersOfReddit>`_ bot will sometimes not be able to find the user's transcription, if the done was replied very quickly after the transcription was posted. In these cases, all that is required is a second done, by which point enough time will have passed for the `r/TranscribersOfReddit <https://www.reddit.com/r/TranscribersOfReddit>`_ bot to find the transcription.

What TADR does is simple: it continually monitors the user's Reddit inbox, and when it detects a message with the `r/TranscribersOfReddit <https://www.reddit.com/r/TranscribersOfReddit>`_ bot's reply for when it cannot find a transcription, it checks the parent comment of that message. If the parent comment is simply "done", it will respond with its automated message. If the parent comment is already its automated message, that means that a second done was not enough and there is another problem, at which point it will send a desktop notification the user.

Copyright
----------

Copyright (C) 2021-present, Murdo B. Maclachlan

TADR program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

TADR is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License for more details.

You should receive a copy of the GNU General Public License when you
install TADR. If not, see https://www.gnu.org/licenses/.

For help, contact me at murdomaclachlan@duck.com
