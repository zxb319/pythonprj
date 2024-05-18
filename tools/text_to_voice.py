import win32com.client as win

speaker = win.Dispatch('SAPI.SpVoice')
speaker.speak(
    '''
    张新波
    '''
)
