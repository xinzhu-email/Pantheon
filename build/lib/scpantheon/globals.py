from appdirs import AppDirs
import pkg_resources
global dir

def get_version():
    try: 
        return pkg_resources.get_distribution("scpantheon").version
    except:
        return "0.7.0.0"

appname = "scpantheon"
appauthor = "xinzhu"
dirs = AppDirs(appname, appauthor, get_version())
dir = dirs.user_data_dir