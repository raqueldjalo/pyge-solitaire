#! /usr/bin/env python

# I wrote this after reading through several other setup scripts, including PySetup and pygame2exe

# imports
from distutils.core import setup
import sys, os, pygame, shutil, glob

##################################
### Program Specific Variables ###
##################################

path = os.getcwd() + "\\source\\pyge\\"

name = "Pyge"
description = 'Peg Solitaire Implementaton'
version = '1.1'

author = 'Annan Fay Yearian'
author_email = 'annanfay+pyge@gmail.com'
url = 'http://code.google.com/p/pyge-solitaire/'
copyright = "Copyright (C) 2010"
company = None
license = 'GNU General Public License v3'

script = path + "Pyge.py"
icon_file = path + "icon.ico"
dest_file = "Pyge"  # Final name of .exe file
dest_dir = "binaries"   # Final folder to contain the executable, data files, etc.
build_dir = "build" #doesn't change anything yet

optimize = 2
dos_console = 1 #set to 0 for no dos shell when run

extra_data = ['Resources','icon.png' ]
extra_modules = ['pygame.locals'] #extra python modules not auto found
dll_excludes = [] # excluded dlls ["w9xpopen.exe", "msvcr71.dll"]

#Libraries to exclude from the EXE (use to cut down the final EXE filesize.)
lib_excludes = [
    "OpenGL",
    "Numeric",
    "numpy",
    "wxPython",
    "pyglet"
    'email',
    'AppKit',
    'Foundation',
    'bdb',
    'difflib',
    'tcl',
    'Tkinter',
    'Tkconstants',
    'curses',
    'distutils',
    'setuptools',
    'urllib',
    'urllib2',
    'urlparse',
    'BaseHTTPServer',
    '_LWPCookieJar',
    '_MozillaCookieJar',
    'ftplib',
    'gopherlib',
    '_ssl',
    'htmllib',
    'httplib',
    'mimetools',
    'mimetypes',
    'rfc822',
    'tty',
    'webbrowser',
    'socket',
    'hashlib',
    'base64',
    'compiler',
    'pydoc'
]

REMOVE_BUILD_ON_EXIT = False

#########################################
### Don't change anything after here. ###
#########################################

# Run the script if no commands are supplied 
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")
    
cmd = sys.argv[1]
if cmd in ('--help', '-h'):
    print 'Usage: setup.py sdist|py2exe|py2app|cx_freeze'
    raise SystemExit
    
dest_dir = dest_dir + '/' + cmd
try:
    shutil.rmtree(dest_dir)
except: pass

# Use the pygame icon if there's no icon designated
if icon_file is '':
    path = os.path.split(pygame.__file__)[0]
    icon_file = '' + os.path.join(path, 'pygame.ico') 

# Copy extra data files
def install_file(name):
    dst = os.path.join(dest_dir)
    print 'copying', name, '->', dst
    if os.path.isdir(name):
        dst = os.path.join(dst, name)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(name, dst)
    elif os.path.isfile(name):
        shutil.copy(name, dst)
    else:
        print 'Warning, %s not found' % name

# utility for adding subdirectories
def add_files( dest, generator ):
    for dirpath, dirnames, filenames in generator:
        for name in 'CVS', '.svn', '.git':
            if name in dirnames:
                dirnames.remove(name)

        for name in filenames:
            
            suffix = os.path.splitext(name)[1]
            if '~' in name \
            or suffix in ('.pyc', '.pyo')\
            or name[0] == '.':
                continue
            
            filename = os.path.join(dirpath, name)
            dest.append(filename)
            

# define what is our data
data = []
add_files( data, os.walk('data') )
data.extend( glob.glob('*.txt') )

# define what is our source
src = []
add_files( src, os.walk('lib') )
src.extend( glob.glob('*.py') )

##########################
### sdist setup script ###
##########################

if cmd == 'sdist':
    f = open( "MANIFEST.in", "w")
    for l in data: f.write("include "+l+"\n")
    for l in src: f.write("include "+l+"\n")
    f.close()

    setup(
        options         = {'sdist':{
            'dist_dir':dest_dir,
        }},
        name            = name,
        version         = version,
        description     = description,
        author          = author,
        author_email    = author_email,
        url             = url,
        license         = license,
    )

###########################
### py2exe setup script ###
###########################

if cmd == 'py2exe':
    import py2exe
    
    origIsSystemDLL = py2exe.build_exe.isSystemDLL
    def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ["sdl_ttf.dll"]:
            return 0
        return origIsSystemDLL(pathname)
    py2exe.build_exe.isSystemDLL = isSystemDLL
    
    
    class Target:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    # Set some variables for the exe
    target = Target(
        script          = script,
        icon_resources  = [(1, icon_file)],
        dest_base       = dest_file,
        extra_modules   = extra_modules,
        version         = version,
        company_name    = company,
        author          = author,
        copyright       = copyright,
        name            = name
    )
    
    setup(
        options = {'py2exe':{
            'dist_dir':dest_dir,
            'dll_excludes':['_dotblas.pyd','_numpy.pyd'],
            
            'optimize':2,
            "compressed": 1,
            "bundle_files": 1,
#Specifying a level of 2 includes the .pyd and .dll files into the zip-archive or the executable. Thus, the dist directory will contain your exe file(s), the library.zip file (if you haven't specified 'zipfile=None'), and the python dll. The advantage of this scheme is that the application can still load extension modules from the file system if you extend sys.path at runtime.
#Using a level of 1 includes the .pyd and .dll files into the zip-archive or the executable itself, and does the same for pythonXY.dll. The advantage is that you only need to distribute one file per exe, which will however be quite large. The disadvantage of this scheme is that it is impossible to load other extensions from the file system, the application will crash with a fatal Python error if you try this. 
            "ignores": ['tcl','AppKit','Numeric','Foundation'],
            "includes": extra_modules,
            "excludes": lib_excludes,
            #'ascii': 1
        }},
        windows = [{
            "script": script,                       ### Main Python script    
            "icon_resources": [(0, icon_file)]      ### Icon to embed into the PE file
        }],
        console = [{
            "script": script,                       ### Main Python script    
            "icon_resources": [(0, icon_file)]      ### Icon to embed into the PE file
        }],
        data_files = [(".", [icon_file])],
        scripts = [script],
        name = name,
        zipfile = None, 
    )

###########################
### py2app setup script ###
###########################

if cmd == 'py2app':
    
    import py2app
    
    raise Exception
    dist_dir = os.path.join(dest_dir,name+'.app')
    data_dir = os.path.join(dist_dir,'Contents','Resources')
    from setuptools import setup

    src = PY_PROG
    dest = cfg['py2app.target']+'.py'
    shutil.copy(src,dest)

    APP = [dest]
    DATA_FILES = []
    OPTIONS = {'argv_emulation': True, 'iconfile':cfg['py2app.icon']}

    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )

    # from setuptools import setup

    # NAME = 'aliens'
    # VERSION = '0.1'

    # plist = dict(
        # CFBundleIconFile=NAME,
        # CFBundleName=NAME,
        # CFBundleShortVersionString=VERSION,
        # CFBundleGetInfoString=' '.join([NAME, VERSION]),
        # CFBundleExecutable=NAME,
        # CFBundleIdentifier='org.pygame.examples.aliens',
    # )

    # setup(
        # data_files=['English.lproj', 'data'],
        # app=[
            # dict(script="aliens_bootstrap.py", plist=plist),
        # ],
        # setup_requires=["py2app"],
    # )
    print
    
##############################
### cx_freeze setup script ###
##############################

if cmd == 'cx_freeze':
    import cx_freeze

    raise NotImplemented
    
    from cx_Freeze import setup, Executable
    setup(
        name        = name,
        version     = version,
        description = description,
        executables = [Executable(script)]
    )

########################
### Copy extra files ###
########################

# To fix font bug
pygamedir = os.path.split(pygame.base.__file__)[0]
#install_file(os.path.join(pygamedir, pygame.font.get_default_font()))

for d in extra_data:
    install_file(d)
    

# recursively make a bunch of folders
def make_dirs(dname_):
    parts = list(os.path.split(dname_))
    dname = None
    while len(parts):
        if dname == None:
            dname = parts.pop(0)
        else:
            dname = os.path.join(dname,parts.pop(0))
        if not os.path.isdir(dname):
            os.mkdir(dname)
    

# copy data into the binaries
if cmd in ('py2exe','cx_freeze','py2app'):
    dest = dest_dir
    for fname in data:
        dname = os.path.join(dest, os.path.dirname(fname))
        make_dirs(dname)
        if not os.path.isdir(fname):
            shutil.copy(fname,dname)

#clean up
if REMOVE_BUILD_ON_EXIT:
    shutil.rmtree(build_dir)

# If everything went okay, this should come up.
#raw_input('\n\nSuccessful! Press enter to exit')