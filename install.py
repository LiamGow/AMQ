import pip

def install(package):
    try:
        __import__(package)
    except:
        pip.main(['install', package])

install("pytube")
install("progress")
