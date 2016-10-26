import types
import os,sys,re

VERSIONABLE_CLASS_PREFIX = "Backend"
VERSIONABLE_FILE_PREFIX = "backend"
VERSIONABLE_FILE_SEPARATOR = "_"
VERSIONABLE_FOLDER = ""
VERSIONABLE_AUTOGEN_CONTENT = """import versionable

class {}(versionable.Versionable):
    \"""
        (Auto generated).
        Class that enables Backend access. (Versionable)
    \"""
    def __init__(self,version=None):
        versionable.Versionable.__init__(self,version)"""


class Versionable(object):
    """
        Object that wraps dynamic implementations loading and versioning
    """
    
    def __init__(self,version):
        name = str(self.__class__.__name__)
        name = name.split(".")[0].split("/")[-1]
        if version is None:
            version=self.__greatest_version(name)
        else:
            version = str(version)
        implementation = self.__load(name,version)
        functions = [x for x in dir(implementation) if not x.startswith('__')]
        for function_name in functions:
            setattr(self,function_name,getattr(implementation,function_name))
            
        

    def __load(self,name,version):
        if name in version:
            #TO catch any version string diferent than "name_versionnumber"
            to_import = version.split(".")[0]
        else:
            to_import = name + VERSIONABLE_FILE_SEPARATOR +str(version)
            
        print("Loading : " + name + " version "+ str(version))
        try:
            if to_import in list(sys.modules):
                sys.modules.pop(to_import)
                print("Refreshed: "+ str(to_import))
            return __import__(to_import)
        except Exception as inst:
            print(inst)
        
        
    def __greatest_version(self,name):
        """
        Takes greater version formated
        """
        reg = re.compile(".*?(\d+)\.py$")
        version_files = [file_ for file_ in os.listdir(".") if reg.search(file_)]
        versions = {reg.match(v).group(1):v for v in version_files}
        last_version = max(versions.keys())
        print("Greatest version file: {}".format(versions[last_version]))
        return versions[last_version]        

def buildup(name,version):
    versionable_class = VERSIONABLE_CLASS_PREFIX+VERSIONABLE_FILE_SEPARATOR+name
    versionable_file = versionable_class+VERSIONABLE_FILE_SEPARATOR+version+".py"
    
    versionable_base_file = VERSIONABLE_FILE_PREFIX+VERSIONABLE_FILE_SEPARATOR+name+".py"

    #create base file
    if not os.path.exists(versionable_base_file):
        file_content = VERSIONABLE_AUTOGEN_CONTENT.format(versionable_class)
        f = open(versionable_base_file,"w")
        f.write(file_content)
        print("Created file: "+ versionable_base_file)
    else:
        print("Existing file: "+ versionable_base_file)
        
    return versionable_file
        
        
        


