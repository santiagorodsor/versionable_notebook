import types
import os
import sys

VERSIONABLE_CLASS_PREFIX = "Backend"
VERSIONABLE_FILE_PREFIX = "backend"
VERSIONABLE_FOLDER = "."
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
        Interface that enable load diferent versions at request
    """
    
    def __init__(self,version):
        name = str(self.__class__.__name__)
        name = name.split(".")[0].split("/")[-1]
        if version is None:
            version=self.__last_flagged_version(name)
        else:
            version = str(version)
        implementation = self.__load(name,version)
        functions = [x for x in dir(implementation) if not x.startswith('__')]
        for function_name in functions:
            setattr(self,function_name,getattr(implementation,function_name))
            
        

    def __load(self,name,version):
        if name in version:
            to_import = version.split(".")[0]
        else:
            to_import = name + "_v_"+str(version)
            
        print("Loading : " + name + " version "+ str(version))
        try:
            self.__refresh(to_import) 
            return __import__(to_import)
        except Exception as inst:
            print(inst)
        
        #import to_import as imported
        #return imported
#        raise NotImplementedError("Class %s doesn't implement load()" % (self.__class__.__name__))
        
    def __last_flagged_version(self,name):
        version_files = [file_ for file_ in os.listdir(".") if name in file_ and file_.endswith(".py")]
        versions = {v.split(".")[0].split("_")[-1]:v for v in version_files}
        print(versions)
        last_flag = "last"
        last_version = last_flag if last_flag in versions.keys() else max(versions.keys())
        print(last_version)
        return versions[last_version]
    
    def __refresh(self,lib):
        if lib in list(sys.modules):
            something = sys.modules.pop(lib)
            print("Refreshed: "+ str(lib))

def buildup(name,version):
    versionable_class = VERSIONABLE_CLASS_PREFIX+"_"+name
    versionable_file = versionable_class+"_"+version+".py"
    
    versionable_base_file = VERSIONABLE_FILE_PREFIX+"_"+name+".py"

    #create base file
    if not os.path.exists(versionable_base_file):
        file_content = VERSIONABLE_AUTOGEN_CONTENT.format(versionable_class)
        f = open(versionable_base_file,"w")
        f.write(file_content)
        print("Created file: "+ versionable_base_file)
    else:
        print("Existing file: "+ versionable_base_file)
        
    return versionable_file
        
        
        


