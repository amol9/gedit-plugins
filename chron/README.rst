# Chron

Inserts date/time in the current document at the cursor.

* F2: Insert date
* F3: Insert time
* F4: Insert date and time


Settings

* Insert a line break after date/time
* Use all lower case letters
* Specify date format
* Specify time format


Installation

1. Copy chron.py and chron.plugin to ~/.local/share/gedit/plugins
2. Copy the gsettings schema xml file to /usr/share/glib-2.0/schemas
3. Compile the schemas: `> sudo glib-compile-schemas <path to schemas dir>`
4. Enable the plugin in gedit

