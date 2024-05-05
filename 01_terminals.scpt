#!/usr/bin/osascript
on run argv
  set BASEDIR to item 1 of argv as string
  tell application "iTerm2"
    # open first terminal start cp cv files
    tell current session of current tab of current window
        write text "cd " & BASEDIR
        write text "bash ./01-cp-cv-files.sh"
        split horizontally with default profile
        split vertically with default profile
    end tell
    # open second terminal and start UI with
    tell second session of current tab of current window
        write text "cd " & BASEDIR
        write text "bash ./01_start_cv-summarizer-ui.sh"
    end tell
    # open third terminal and consume loaded-cv-files
    tell third session of current tab of current window
        write text "cd " & BASEDIR
        write text "bash ./01_start-cv-summarizer-SFTP.sh"
        split horizontally with default profile
    end tell
    # open fourth terminal and consume cv-summaries
    tell fourth session of current tab of current window
        write text "cd " & BASEDIR
        write text "bash ./01-consumer-cv-summaries.sh"
    end tell
  end tell
end run