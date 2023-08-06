from __future__ import annotations
import shutil
import os
import sys
import pathlib
import datetime
import subprocess
import platform
import functools
from typing import List, Any, Tuple

from parent_class import ParentClass
import py_starter as ps

DELIM = '/'
SECONDARY_DELIM = '\\'

def get_cwd() -> str:

    """returns current working directory"""

    cd = os.getcwd()

    #replace the cd with primary delim
    cd_replaced = join( * path_to_dirs(cd) )
    return cd_replaced

def path_to_dirs( path: str ) -> List[str]:

    """splits a path into directories"""
    if path == '':
        return []
    return path.split( DELIM )

def is_file( path: str ) -> bool :

    """returns a boolean value to check if the path is a file"""
    return os.path.isfile( path )

def is_dir( path: str ) -> bool :

    """returns a boolean value to check if the path is a directory"""
    return os.path.isdir( path )

def replace_delims( path: str, secondary_delim: str = SECONDARY_DELIM, delim: str = DELIM ) -> str :

    """turns data\dir\file.txt into data/dir/file.txt"""
    return path.replace( secondary_delim, delim )

def join( *items: str ) -> str:

    """joins a list of dirs into a path"""
    return DELIM.join( items )

def convert_bytes( bytes: int, conversion: str = 'MB' ) -> Tuple[ Any, Any ]:

    try:
        conversion = conversion.upper()
    except:
        pass

    kb_to_b = 1024

    conversion_factors = ['KB','MB','GB','TB','PB','EB']
    if conversion in conversion_factors:

        power = conversion_factors.index(conversion) + 1
        return bytes / (kb_to_b ** power), conversion

    return bytes, None


def add_prefix_to_paths( prefix_path, relative_paths ):

    """adds prefix to a list of relaive paths"""

    full_paths = []
    for relative_path in relative_paths:
        full_paths.append( join(prefix_path, relative_path) )

    return full_paths

def remove_prefix_from_paths( prefix_path, full_paths ):

    """Removes prefix from full paths"""

    number_of_dirs = len( path_to_dirs(prefix_path) )

    relative_paths = []
    for full_path in full_paths:

        folder_list = path_to_dirs( full_path )
        relative_list = folder_list[ number_of_dirs : ]

        relative_paths.append( join(*relative_list) )

    return relative_paths

def remove_hanging_slashes( path ):

    """removes ending slashes from paths
    turns "asdf/asdf//" into "asdf/sadf"   """

    # dont go through all the
    for i in range( len(path)-1, -1, -1 ):

        if path[i] != '/':
            return path[:i+1]

    return path

def get_desktop_dir() -> Any:

    """get the location of the desktop"""

    if platform.system() == 'Windows':
        import winshell
        return winshell.desktop()

    return None

def create_shortcut_on_desktop( target_Path: Path ) -> None:

    """places a shortcut to target_Path on the Desktop"""

    desktop_Dir = Dir( get_desktop_dir() )
    create_shortcut( target_Path, desktop_Dir )

def create_shortcut( target_Path: Path, shortcut_Dir: Dir ) -> None:

    """places a shortcut from target_Path to shortcut_Dir"""

    if platform.system() == 'Windows':
        import winshell

        shortcut_Path = Path( shortcut_Dir.join( target_Path.root + '.lnk' ) )
        winshell.CreateShortcut( Path=shortcut_Path.p, Target=target_Path.p )

    else:
        print ('No instructions for current OS')

def get_env_var_path_delim() -> str:

    """Returns the delimitter for the OS's path environment variables"""

    if platform.system() == 'Windows':
        return ';'
    elif platform.system() == 'Linux':
        return ':'

def split_env_var_paths( string: str ) -> List[str]:

    """returns a list of path strings split on the system delimitter"""

    return string.split( get_env_var_path_delim() )

def join_env_var_paths( paths: List[str] ) -> str:

    """ returns 'C:/Path1;C:/Path2' """
    return get_env_var_path_delim().join( paths )

def print_to_from( print_off: bool, action_str: str, from_str: str, to_str: str ):

    """ Copying C:/Users/path/file.txt ->  C:/Users/newfile.txt """

    if print_off:
        print ( "{action_str} \t {from_str} -> \t {to_str}".format( action_str = action_str, to_str = to_str, from_str = from_str ) )

### Decorators

def copy_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, override: bool = False, print_off: bool = False, 
                    Destination = None, destination = None, **kwargs ):

        #whether this is a Dir or a Path, create the parents before copying        
        if Destination == None:
            if self.type_path:
                Destination = Path( destination )
            if self.type_dir:
                Destination = Dir( destination )

        Destination.create_parents()

        #check to make sure the user wants to do this
        if not override:
            print_to_from( True, 'Copying', str(self), str(Destination) )
            override = ps.confirm_raw( string = '' )

        # perform the actual method        
        if override:
            print_to_from( print_off, 'Copying', str(self), str(Destination) )

            if method( self, *args, destination = Destination.path, override=override, print_off=print_off, **kwargs ):
                return True

        return False

    return wrapper


def remove_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, override: bool = False, print_off: bool = False, **kwargs ):
        
        if not override:
            override = ps.confirm_raw( string = 'This operation will delete ' + str(self) )
        
        if override:
            print_to_from( print_off, 'Removing', str(self), '' )

            if method( self, *args, **kwargs ):
                return True
            else:
                print ('Could not delete ' + str(self))

        return False

    return wrapper

def get_size_wrap( method ):

    @functools.wraps( method )
    def wrapper( self, *args, **kwargs ):
        size, size_units = method( self, *args, **kwargs )
        self.size = size
        self.size_units = size_units

        return size, size_units

    return wrapper


def dir_ops_instance_method(method):

    """instance methods call the corresponding staticmethod 
    Example: Dir_instance.exists(*,**) calls Dir.exists_dir( Dir_instance.path,*,** )   
    """

    @functools.wraps(method)
    def wrapper( self, *called_args, **called_kwargs):

        new_method_name = method.__name__ + self.STATIC_METHOD_SUFFIX
        return self.get_attr( new_method_name )( self.path, *called_args, **called_kwargs )
        
    return wrapper

def inherited_instance_method(method):

    """instance methods call the corresponding staticmethod 
    Example: Dir_instance.exists(*,**) calls Dir.exists_dir( Dir_instance.path,*,** )   """

    @functools.wraps(method)
    def wrapper( self, *called_args, **called_kwargs):

        new_method_name = method.__name__ + self.STATIC_METHOD_SUFFIX
        instance_args = [ self.get_attr( attr ) for attr in self.INSTANCE_METHOD_ATTS ]

        return self.get_attr( new_method_name )( *instance_args, *called_args, **called_kwargs )
      
    return wrapper


class Dir (ParentClass) :

    STATIC_METHOD_SUFFIX = '_dir'
    INSTANCE_METHOD_ATTS = ['path']

    def __init__ ( self, *args, **kwargs ):

        ParentClass.__init__( self )
        self.dir_construct( *args, **kwargs )

        self.DIR_CLASS = Dir
        self.PATH_CLASS = Path
        self.DIRS_CLASS = Dirs
        self.PATHS_CLASS = Paths

    def __eq__( self, other_Dir ):

        if isinstance( other_Dir, Dir ):
            return self.path == other_Dir.path
        return False

    def dir_construct( self, absolute_path, **kwargs ):

        absolute_path = replace_delims( absolute_path )
        self.path = remove_hanging_slashes( absolute_path )  # 'C:/Users/e150445/Documents/MO-EE/Data/Raw'
        self.dirs = path_to_dirs( self.path )                #[ 'C','Users','e150445','Documents','MO-EE','Data','Raw' ]
        self.type_path = False
        self.type_dir = True

        self.size = None                          # don't init with checking the size, takes too long
        self.size_units = None

        #alias just for quick coding
        self.p = self.path

    def print_imp_atts( self, print_off = True ):

        return self._print_imp_atts_helper( atts = ['path','dirs'], print_off = print_off )

    def print_one_line_atts(self, print_off = True, leading_string = '\t' ):

        return self._print_one_line_atts_helper( atts = ['type','path'], print_off = print_off, leading_string = leading_string )

    @staticmethod
    def is_Dir( Object: Any ) -> bool:

        """returns boolean if Object is a Dir"""
        return isinstance( Object, Dir )

    def ascend( self, level_to_ascend: int = 1 ) -> Dir :
        
        """go up a x number directories -> "levels_to_ascend" """

        return Dir( join( *self.dirs[:-1*level_to_ascend] ))
    
    @staticmethod
    def ascend_dir( dir: str, levels_to_ascend: int = 1 ) -> str:

        """go up a x number directories -> "levels_to_ascend" """

        dirs = path_to_dirs( dir )
        return join( *dirs[:-1*levels_to_ascend] )

    @dir_ops_instance_method
    def join( self, *args, **kwargs ):
        pass
    
    @staticmethod
    def join_dir( dir: str, *other_dirs, **kwargs ):
        
        """add more dirs to the Dir path"""
        if dir != '':
            return join( dir, *other_dirs )
        else:
            return join( *other_dirs )


    def join_Dir( self, other_Dir: Dir ) -> Dir:

        return Dir( self.join( other_Dir.path ) )

    def join_Path( self, other_Path: Path ) -> Path:

        return Path( self.join( other_Path.path ) )

    @inherited_instance_method
    def open( self, *args, **kwargs ):
        pass
    
    @staticmethod
    def open_dir( dir ):

        """Opens the dir in the file explorer """

        if platform.system() == 'Windows':
            os.startfile(dir)

        elif platform.system() == 'Darwin':
            subprocess.call(['open', dir])

    @inherited_instance_method
    def exists( self, *args, **kwargs ):
        pass

    @staticmethod
    def exists_dir( dir: str, *args, **kwargs ) -> bool:
        return os.path.exists( dir )

    @remove_wrap
    @inherited_instance_method
    def remove(self, *args, **kwargs) -> bool:
        pass
    
    @staticmethod
    def remove_dir( dir: str, *args, **kwargs ) -> bool:

        """deletes the entire folder and all contents underneath, returns True is successful"""

        try:
            shutil.rmtree(dir)
        except:
            return False

        return True

    def create(self, *args, **kwargs) -> bool:

        """creates a directory and parent directories of dir"""

        if not self.exists():
            self.create_parents()
        
        return self.create_dir( self.path )

    @staticmethod
    def create_dir( dir: str ) -> bool:

        try:
            os.mkdir( dir )
        except:
            return False
        return True

    def create_parents(self):

        """use recursion to travel all the way up the parent directories until we find one that exists, then unfold and create each directory"""

        parent_Dir = self.ascend()
        if parent_Dir.exists() or len(self.dirs) <= 1: #Parent Dir exists or we are at the base directory
            return

        else:
            parent_Dir.create_parents()
            parent_Dir.create()

    @copy_wrap
    @inherited_instance_method
    def copy(self, *args, **kwargs):
        pass

    @staticmethod
    def copy_dir( dir: str, destination: str = '') -> bool:

        try:
            shutil.copytree( dir, destination )
        except:
            return False
        return True

    @inherited_instance_method
    def list_contents( self, *args, **kwargs ):
        pass

    @staticmethod
    def list_contents_dir( dir: str ) -> List[str]:

        """returns all directories and files contained in dir""" 
        return os.listdir( dir )

    @get_size_wrap
    @inherited_instance_method
    def get_size( self, *args, **kwargs ):
        pass

    def get_size_dir( dir: str, *args, **kwargs ):

        self = Dir( dir )
        Paths_inst = self.list_contents_Paths( block_dirs=True, block_paths=False )

        bytes = 0
        for Path_inst in Paths_inst:
            Path_inst.get_size( conversion = None )
            bytes += Path_inst.size 
        
        return convert_bytes( bytes, **kwargs )

    def get_rel( self, other_Dir ) -> Dir:

        """Given a Dir object, find the relative Dir from Dir to self"""

        return Dir( self.get_rel_dir( self.path, other_Dir.path ) )

    @staticmethod
    def get_rel_dir( dir, other_dir ) -> str:
        
        if dir != '':
            return os.path.relpath( dir, other_dir )
        else:
            return other_dir

    def list_contents_Paths( self, block_dirs: bool = True, block_paths: bool = False ) -> Paths: 

        """returns all first sublevel contents of Directory as a Paths instance"""

        filenames = self.list_contents() # a list of filenames and directories
        Paths_inst = self.PATHS_CLASS()

        for filename in filenames:
            path = self.join( filename )

            if is_dir( path ):
                if not block_dirs:
                    Paths_inst._add( Dir( path ) )

            else:
                if not block_paths:
                    Paths_inst._add( Path( path ))
            
        return Paths_inst

    def walk( self, folders_to_skip: List[str] = ['.git'] ) -> Paths:

        """Walk through all the contents of the directory"""

        Paths_inst = self.PATHS_CLASS()
        Paths_inst._add( self )

        Paths_under = self.list_contents_Paths( block_dirs = False, block_paths = False )

        for Path_inst in Paths_under:

            # all Paths are also Dirs
            if Path_inst.type_path:
                Paths_inst._add( Path_inst )

            elif Path_inst.type_dir:
                
                if Path_inst.dirs[-1] not in folders_to_skip:
                    Paths_inst.merge( Path_inst.walk( folders_to_skip = folders_to_skip ) )

        return Paths_inst

    def walk_contents_Paths( self, block_dirs: bool = True, block_paths: bool = False, folders_to_skip: List[str] = ['.git'] ) -> Paths:

        """get all Paths and/or Dirs underneath the entire directory, optional params for returning paths and/or dirs"""

        Paths_inst = self.walk( folders_to_skip=folders_to_skip )
        keep_Paths = self.PATHS_CLASS()

        for Path_inst in Paths_inst:
            if Path_inst.type_path and not block_paths:
                keep_Paths._add( Path_inst )

            if Path_inst.type_dir and not block_dirs:
                keep_Paths._add( Path_inst )

        return keep_Paths

    def get_unique_Path( self, filename: str ) -> str:

        """finds a unique Path for the proposed filename based on the contents of the Directory
        if file.txt already exists in the dir, return file1.txt or file2.txt, etc  """

        Paths_in_Dir = self.list_contents_Paths( block_dirs=True, block_paths=False )
        filenames = [ P.filename for P in Paths_in_Dir ]

        if filename not in filenames:
            return Path( self.join(filename) )

        filename_Path = Path( filename )
        counter = 0

        while True:
            proposed_filename = filename_Path.root + str(counter) + filename_Path.extension
            if proposed_filename not in filenames:
                return Path( self.join(proposed_filename) )

            counter += 1

class Path( Dir ):

    """
    Inherits from the Dir class found in Dir.py
    Path (uppercase P) is a Path class, path (lowercase P) is a string with file absolute path
    """

    STATIC_METHOD_SUFFIX = '_path'
    INSTANCE_METHOD_ATTS = ['path']

    def __init__( self, absolute_path ):

        self.path_construct(absolute_path)

        self.DIR_CLASS = Dir
        self.PATH_CLASS = Path
        self.DIRS_CLASS = Dirs
        self.PATHS_CLASS = Paths

    def path_construct(self, absolute_path):

        """Since the Path is different from a Dir, add the extra attiributes"""

        Dir.__init__( self, absolute_path )
        self.filename =     Path.get_filename( self.path )                  # feb_mar_v1.0.txt
        self.root =         Path.get_root( self.path )                      # feb_mar_v1
        self.root_dots =    Path.get_root( self.path, allow_dots=True )     # feb_mar_v1.0
        self.ending =       Path.get_ending( self.path )                    # txt
        self.extension =    '.' + self.ending                               # .txt
        self.size = None                          # don't init with checking the size, takes too long
        self.size_units = None
        self.mtime = None                        # a datetime object when its ready

        self.parent_Dir = self.ascend()
        self.type_path = True
        self.type_dir = False

    def __eq__( self, other_Path: Path ) -> bool:

        """checks if self is equal to other_Path, returns bool"""

        if isinstance( other_Path, Path ):
            return self.path == other_Path.path
        return False

    @staticmethod
    def is_Path( Object: Any ) -> bool:

        """returns boolean if Object is a Dir"""
        return isinstance( Object, Path )

    def print_imp_atts(self, print_off = True):

        return self._print_imp_atts_helper( atts = ['path','dirs','ending','size'], print_off = print_off )

    @inherited_instance_method
    def exists( self, *args, **kwargs ):
        pass

    @staticmethod
    def exists_path( path: str, **kwargs ) -> bool:
        return os.path.exists( path )

    @staticmethod
    def copy_path( path: str, destination_path: str ) -> bool:

        """copies an the contents from source to destination"""

        if Path.exists_path(path) and not Path.exists_path(destination_path):
            try:
                shutil.copyfile(path, destination_path)
            except:
                return False
            return True
        return False

    @remove_wrap
    @inherited_instance_method
    def remove( self, *args, **kwargs ):
        pass

    @staticmethod
    def remove_path(path: str, *args, **kwargs) -> bool:

        """deletes file at path: BE CAREFUL"""

        try:
            os.remove(path)
        except:
            return False
        return True

    @inherited_instance_method
    def rename( self, *args, **kwargs):
        pass
    
    @staticmethod
    def rename_path( path, new_Path = None, new_path = '', print_off = False ):

        """renames the file using string new_path or object new_Path
        Give option to overwrite Class instance with new path"""

        if new_Path != None:
            new_path = new_Path.path

        if Path.exists_path( path ) and not Path.exists_path( new_path ):
            if print_off:
                print ('Renaming ' + path + ' to ' + new_path )

            try:
                os.rename(path, new_path)
            except:
                return False
            return True

        else:
            return False

    @staticmethod
    def get_size_path( path, *args, **kwargs ) -> Tuple[ float, str ]:

        size = os.stat( path ).st_size
        return convert_bytes( size, **kwargs )

    def get_mtime( self, *args, **kwargs ):
        self.mtime = self.get_mtime_path( self.path )

    @staticmethod
    def get_mtime_path( path, *args, **kwargs ) -> datetime.datetime:

        """get the time of modification as a datetime object"""

        mtime = pathlib.Path(path).stat().st_mtime
        dt = datetime.datetime.fromtimestamp( mtime )
        return dt

    @inherited_instance_method
    def write( self, *args, **kwargs):
        pass
       
    @staticmethod
    def write_path( path, **kwargs ):
        
        """writes to a text file at path, read py_starter.write_text_file() for kwargs """
        ps.write_text_file( path, **kwargs )

    @inherited_instance_method
    def create( self, *args, **kwargs ):
        pass
    
    @staticmethod
    def create_path( path, string = '', **kwargs ):

        """initialize the contents of the path"""
        Path.write_path( path, string = string, **kwargs )

    @inherited_instance_method
    def read( self, *args, **kwargs):
        pass
    
    @staticmethod
    def read_path( path, **kwargs ):

        """reads from a text file at path, read py_starter.read_text_file() for kwargs """
        return ps.read_text_file( path, **kwargs )

    @inherited_instance_method
    def import_module( self, *args, **kwargs):
        pass
    
    @staticmethod
    def import_module_path( path, *args, **kwargs ):

        """imports the contents of path as a module"""
        return ps.import_module_from_path( path, **kwargs )

    @inherited_instance_method
    def smart_format( self, *args, **kwargs) -> str:
        pass

    @staticmethod
    def smart_format_path( path, formatting_dict, write = True, **kwargs ) -> str:

        """passthrough function for py_starter.smart_format()"""
        string = Path.read_path( path )
        formatted_string = ps.smart_format( string, formatting_dict, **kwargs )

        if write:
            Path.write_path( path, string = formatted_string )

        return formatted_string


    def get_rel( self, Dir_inst ) -> Path:

        """Given a Dir object, find the relative Path from Dir to self"""

        return Path( Path.get_rel_path( self.path, Dir_inst.path ) )

    @staticmethod
    def get_rel_path( path, dir ) -> str:
        return os.path.relpath( path, dir )

    @staticmethod
    def get_filename( path: str ) -> str:

        """returns the filename ('file.txt') from a long path ('C:/path/to/file.txt') """

        dirs = path_to_dirs(path)
        return dirs[-1]
    
    @staticmethod
    def get_root( path: str, allow_dots: bool = False ) -> str:

        '''returns the root of the filename from a path  Dir/a_file1.txt returns "a_file1" '''
        filename = Path.get_filename(path)

        if allow_dots:
            root = '.'.join( filename.split('.')[:-1] )

        else:
            root = filename.split('.')[0]
        
        return root
    
    @staticmethod
    def get_ending( path: str ) -> str:

        '''returns the file ending from a path'''
        
        filename = Path.get_filename(path)
        ending = filename.split('.')[-1]
        return ending



class Dirs(ParentClass):

    STATIC_METHOD_SUFFIX = '_dirs'
    INSTANCE_METHOD_ATTS = ['path']

    def __init__ ( self, Dirs = [], dirs = [] ):

        ParentClass.__init__( self )

        self.Dirs = []
        self.Objs = self.Dirs # Make an Alias

        for D in Dirs:
            self._add( D )
        for d in dirs:
            self._add( Dir( d ) )

        self.DIR_CLASS = Dir
        self.PATH_CLASS = Path
        self.DIRS_CLASS = Dirs
        self.PATHS_CLASS = Paths

    @staticmethod
    def is_Dirs( Object: Any ) -> bool:

        """returns boolean if Object is a Dir"""
        return isinstance( Object, Dirs )

    def __len__( self ):

        return len( self.Objs )

    def __iter__( self ):

        self.i = -1
        return self

    def __next__( self ):

        self.i += 1

        if self.i < len(self):
            return self.Objs[self.i]
        else:
            raise StopIteration

    def __contains__( self, Obj_to_check: Any ) -> bool:

        """returns the boolean value for Dir/Path Obj being contained in the list of Objects"""

        for Obj in self:
            if Obj == Obj_to_check:
                return True
        return False

    def _add( self, new_Obj: Any ) -> None:

        """add a new Object to the list of Objects"""

        self.Objs.append( new_Obj )

    def print_imp_atts( self, print_off = True ):

        string = self._print_imp_atts_helper( print_off = False ) + '\n'
        string += 'Dirs:\n'

        for D in self:
            string += D.print_one_line_atts( print_off = False ) + '\n'

        string = string [:-1]
        return self.print_string( string, print_off = print_off )

    def print_one_line_atts(self, print_off = True, leading_string = '\t' ):

        self.len_Dirs = len(self)
        return self._print_one_line_atts_helper( atts = ['type','len_Dirs'], print_off = print_off, leading_string = leading_string )

    def join_Dir( self, Dir_inst: Dir ) -> Paths:

        """Joins Dir_inst to each Dir/Path contained in the Object"""

        Paths_inst = self.PATHS_CLASS()

        for DirPath in self:

            if DirPath.type_path:
                Paths_inst._add( Dir_inst.join_Path( DirPath ) )
            
            if DirPath.type_dir:
                Paths_inst._add( Dir_inst.join_Dir( DirPath ) )

        return Paths_inst

    def merge( self, other_Dirs: Any ):

        """add all Dir objects from another Dirs instance to self"""

        for Dir_inst in other_Dirs:
            self._add( Dir_inst )

    def export_strings( self ) -> List[str]:

        """Returns all the paths of each Dir/Path contained"""

        return [ O.path for O in self ]


class Paths( Dirs ):

    STATIC_METHOD_SUFFIX = '_paths'
    INSTANCE_METHOD_ATTS = ['path']

    def __init__ ( self, Paths = [], paths = [] ):

        ParentClass.__init__( self )

        self.Paths = []
        self.Objs = self.Paths # Make an Alias

        for P in Paths:
            self._add( P )
        for p in paths:
            self._add( Path( p ) )

        self.DIR_CLASS = Dir
        self.PATH_CLASS = Path
        self.DIRS_CLASS = Dirs
        self.PATHS_CLASS = Paths

    @staticmethod
    def is_Paths( Object: Any ) -> bool:

        """returns boolean if Object is a Dir"""
        return isinstance( Object, Paths )

    def print_imp_atts( self, print_off = True ):

        string = self._print_imp_atts_helper( print_off = False ) + '\n'
        string += 'Paths:\n'

        for P in self:
            string += P.print_one_line_atts( print_off = False ) + '\n'

        string = string [:-1]
        return self.print_string( string, print_off = print_off )

    def print_one_line_atts(self, print_off = True, leading_string = '\t' ):

        self.len_Paths = len(self)
        return self._print_one_line_atts_helper( atts = ['type','len_Paths'], print_off = print_off, leading_string = leading_string )


    def get_rels( self, Dir_inst ) -> Paths:

        """Given a Dir object, find the relative Paths from Dir to the Paths"""

        Paths_inst = self.PATHS_CLASS()
        for P in self:
            Paths_inst._add( P.get_rel( Dir_inst ) )

        return Paths_inst

   

