#!/bin/bash

plugin_dir="$HOME/.local/share/gedit/plugins"

if [ ! -d $plugin_dir ]
then
	echo creating dir $plugin_dir..
	mkdir -p "$plugin_dir"
fi

echo copying plugin files..
cp chron.py $plugin_dir
cp chron.plugin $plugin_dir

schema_dir="/usr/share/glib-2.0/schemas"

echo copying schema file..
sudo cp org.gnome.gedit.plugins.chron.gschema.xml $schema_dir

echo compiling schema..
sudo glib-compile-schemas $schema_dir

plugin_key="org.gnome.gedit.plugins active-plugins"

active_plugins=$(gsettings get $plugin_key)

echo $active_plugins | grep chron >/dev/null

if [ $? -ne 0 ]
then
	echo enabling plugin..
	gsettings set $plugin_key "${active_plugins%]*}, 'chron']"
fi

echo plugin installed.
