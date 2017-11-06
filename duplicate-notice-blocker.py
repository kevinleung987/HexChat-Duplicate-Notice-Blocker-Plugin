import hexchat

__module_name__ = 'duplicate-notice-blocker'
__module_version__ = '1.0'
__module_description__ = 'Blocks duplicate Notices.'

last_notice = None
timer_hook = None
block_time = 60000  # Duration in milliseconds to block the event


def on_notice(word, word_eol, userdata):
    global last_notice
    if word_eol[0] != last_notice:
        last_notice = word_eol[0]
        global timer_hook
        global block_time
        # If there is a timer currently running, replace it with a fresh one
        if timer_hook is not None:
            hexchat.unhook(timer_hook)
            timer_hook = hexchat.hook_timer(block_time, timer)
        else:
            timer_hook = hexchat.hook_timer(block_time, timer)
        return hexchat.EAT_NONE
    else:
        # Eat the event so other plugins/HexChat don't see it
        return hexchat.EAT_ALL


def timer(userdata):
    global last_notice
    global timer_hook
    # Delete the timer and reset the currently stored notice
    last_notice = None
    timer_hook = None
    return False

notice_hook = hexchat.hook_server("NOTICE", on_notice)
print("Duplicate Notice Blocker plugin loaded.")
