#versionable magic functions
from IPython.core.magic import (register_cell_magic)
@register_cell_magic
def writefile_versionable_write(line, cell):
    """ 
    Writes cell contents in file named as 'versionable_file' if 'write_to_file'.

    """
    if write_to_file:
        return get_ipython().run_cell_magic(u'writefile', versionable_file, cell)
    else:
        print("Executed.")
        return get_ipython().run_cell_magic(u'capture',str("--no-stderr --no-stdout --no-display"),cell)

@register_cell_magic
def writefile_versionable_add(line, cell):
    """ 
    Adds cell contents in file named as 'versionable_file' if 'write_to_file'.
    """
    if write_to_file:
        return get_ipython().run_cell_magic(u'writefile',str("-a ") + versionable_file, cell)
    else:
        print("Executed.")
        return get_ipython().run_cell_magic(u'capture',str("--no-stderr --no-stdout --no-display"),cell)

@register_cell_magic
def writefile_versionable_ignore(line, cell):
    """ 
    Ignores cell contents to be executed neither write if 'write_to_file'.
    """
    if write_to_file:
        print("Ignoring while writing")
    else:
        print("Executed.")
        return get_ipython().run_cell_magic(u'capture',str("--no-stderr --no-stdout --no-display"),cell)