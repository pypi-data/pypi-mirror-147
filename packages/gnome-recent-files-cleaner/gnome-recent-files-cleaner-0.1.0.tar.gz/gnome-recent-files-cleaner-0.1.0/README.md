# recent-files-cleaner for GNOME Desktop

Script to clean your recent files used from files that are either hidden or are located in a hidden folder. If you keep it running, it will also prevent those files from being added in the first place. This keeps your history clean for your normal usage, without listing config files that you manipulated or, a "homework"-directory containing content that shall not be listed under recent files.


## How to use

create python environment

    python3 -m venv venv
    . venv/bin/activate
    python3 -m pip install gnome-recent-files-cleaner

run using 

    python -m gnome_recent_files_cleaner.grfc
