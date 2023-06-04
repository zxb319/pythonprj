import time

import pywinauto


app=pywinauto.Application(backend='uia').connect(title=r'微信')

win=app.window(title=r'微信')

# win.set_focus()
# win.print_control_identifiers()

w2=win.child_window(best_match='文件传输助手')

w2.click_input()
# w2.type_keys('早啊')
# # win.child_window(best_match='Edit5').set_edit_text('qqq')
# time.sleep(1)
#
# w3=win.child_window(best_match='sendBtnButton')
# w3.click_input()
#
#
