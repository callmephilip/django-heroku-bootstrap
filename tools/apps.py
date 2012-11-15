import os

def enumerate_apps():
    return [ name for name in os.listdir('./apps') if os.path.isdir(os.path.join('./apps', name)) ]