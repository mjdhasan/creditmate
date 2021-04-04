import platform
import os
if platform.platform() == 'macOS-11.1-x86_64-i386-64bit':
    platform_user = 'majid'
else:
    platform_user = 'majid-mac'

# set keys dir
DIR_KEYS = f'/Users/{platform_user}/Dropbox/code/api_keys'
DIR_DUMPS = f'/Users/{platform_user}/Dropbox/startup/content/dumps'
DIR_VIDEOS = f'/Users/{platform_user}/Dropbox/startup/content/demo/docParser/creditmate/'
UPLOAD_DIRECTORY = os.path.join(os.getcwd(), 'uploads')
SCRAPED_DIRECTORY = os.path.join(os.getcwd(), 'scraped')
UPLOAD_PARSED_DIRECTORY = os.path.join(os.getcwd(), 'uploads_parsed')
