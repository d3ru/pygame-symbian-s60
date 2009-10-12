"""PyS60 SDK installer script for downloading the latest PyS60 release from Garage"""

import os
import sys
import urllib
import glob

import zipfile
import tarfile

GARAGE    = "https://garage.maemo.org"
PYS60_DOWNLOAD_PAGE = GARAGE + "/frs/?group_id=854"
TARGET    = "pys60_installer"
INSTALLED = "installed.txt"

def check():
    "Check that EPOCROOT is defined correctly"
    
    er = os.environ["EPOCROOT"]
    if not os.path.exists( er ): 
        raise SystemExit("Missing EPOCROOT")
    
    if not er.endswith("\\"):
        er += "\\"
    
    if not os.path.exists( er + "epoc32" ):
        raise SystemExit("Invalid EPOCROOT")
     
    os.environ["EPOCROOT"] = er.replace("\\", "/")

def update_installed(filename):
    
    if not is_installed(filename):
        f = open(TARGET + INSTALLED, 'a')
        f.write(filename + "\n")
        f.close()

def is_installed(filename):
    try:
        f = open(TARGET + INSTALLED)
    except IOError:
        return False
        
    lines = f.readlines()
    f.close()

    for line in lines:
        if filename in line:
            return True
            
    return False
    
def install(options):
    "Extract the downloaded archives to Symbian SDK"
    
    # Scan for latest PyS60 version in the archive folder
    latest = (0,0,0)
    for name in glob.glob(TARGET + "Python*SDK*.zip"):
        name = os.path.basename(name)
        
        parts = name.split("_")
        ver   = tuple( map(int, parts[1].split(".") ))
        if ver > latest:
            latest = ver
            
    if latest != (0,0,0):
        latest = ".".join( [str(x) for x in latest ] )
        print "Latest PyS60 version in local repository detected:", latest
    else:
        latest = "" # Install any
            
    
    # Extract files from archives.
    for name in glob.glob(TARGET + "*.*"):        
        archive = name
        name    = os.path.basename( name )
        if name.endswith(".zip"):
            zfile = zipfile.ZipFile(archive, "r")
            infolist = zfile.infolist()
            
            #import pdb;pdb.set_trace()
            if ( name.startswith("Python") and "SDK" in name) and ( latest not in name or options.sdk not in name):
                print archive, "skipped. Invalid SDK version."
                continue
            
        elif name.endswith(".tar.gz") and latest in name:
            tfile = tarfile.open(archive, 'r:gz')
            infolist = tfile.getmembers()
            
            
        else:
            print name, "skipped."
            continue
            
        if is_installed(archive):
            if not options.force_install: 
                print name, "skipped. Already installed."
                continue
            else:
                print name, "already installed but install forced."
        
        print "Extracting", archive
        
        erase    = ""
        counter  = 0.0
        prev     = 0.0
        total    = float(len( infolist ))
         
        for info in infolist:
        
            percent = int( counter / total * 100 )
            if percent != prev:
                
                # Write backspaces to erase previous progress
                sys.stdout.write(erase)
                
                percent = "%d\\%d(%d%%)" % ( counter, total, percent )
                prev = percent
                
                sys.stdout.write(percent)
                erase = len( percent ) * '\b'
                
            
            if type(info) == tarfile.TarInfo:
                #import pdb;pdb.set_trace()
                name = info.name
                file = tfile.extractfile(info)
                
            else:
                file = zfile
                name = info.filename
                        
            path = os.environ["EPOCROOT"] + name
            
            if "PythonForS60" in archive and options.tools_path:
                path = os.path.join( options.tools_path, name )
                
            if name.endswith("/") or file is None:
                if not os.path.exists(path):
                    os.mkdir(path)
                    #print "Dir created:", path
                continue
            
            #print path
            fout = open(path, "wb")
            
            if type(info) == tarfile.TarInfo:
                data = file.read( )
                while len(data) > 0:
                    fout.write(data)
                    data = file.read()
            else:
                data = zfile.read(name)
                fout.write(data)
            
            fout.close()
            
            counter += 1
            
        update_installed(archive)
        
        sys.stdout.write(erase)
        #print "Done"
    
def download(options):
    """Download PyS60 archives from Garage
    - Latest OpenC SDK
    - PyS60 headers and libraries
    - PyS60 packaging tool
    """
    f = urllib.urlopen( PYS60_DOWNLOAD_PAGE )
    data = f.read()
    f.close()
    
    # Find latest release
    key  = "shownotes.php"
    s    = data.index(key)
    e    = data.index("shownotes.php", s + len(key) )
    data = data[s:e]
    
    files = {}
    lines = data.split()
    
    for line in lines:
        if "href" not in line: continue
        
        #print line
        
        try: 
            url, name = line.split(">")[:2]
            url  = url.split('"')[1]
            name = name.split("<")[0]
        
            files[name] = GARAGE + url
        except ValueError: 
            # Done
            pass
        
    # Download FP2 SDK
    for name in files:
        
        downloadable = False
        if "OpenC" in name and "plugin" in name and options.openc:
            downloadable = True
            
        elif "PythonForS60" in name and name.endswith(".tar.gz"):
            downloadable = True

        elif options.sdk in name and "Python" in name and name.endswith(".zip"):
            downloadable = True
            
        if downloadable:
            filename = TARGET + name
            if os.path.exists(filename):
                if  not options.force_download:
                    print filename, "exists. Skipped."
                    continue
                else:
                    print filename, "exists, but download forced."
                
            print "Downloading", name, files[name]
            
            # Could use urlretrieve, but me wants progressinfo :b
            #urllib.urlretrieve( files[name], name )
            
            fout = open( filename , 'wb')
            
            f = urllib.urlopen( files[name] )
            
            fullsize = int( f.headers["Content-length"] )
            
            data = f.read(2048)
            size = len(data)
            while len(data):
                
                size += len( data )                
                fout.write( data )
                
                progress = "%d\\%d(%2d%%)" % ( size, fullsize, size / float(fullsize) * 100 )
                sys.stdout.write( progress )
                
                data = f.read(2048)
                sys.stdout.write( len(progress) * "\b" )
                
            f.close()
            fout.close()
    
def main():
    global TARGET
    
    check()
    
    TARGET = os.environ["EPOCROOT"] + TARGET + "/"
    
    from optparse import OptionParser
    parser = OptionParser() 
    
    parser.add_option("-s", "--sdk",
                  dest="sdk", default="FP2",
                  help="Download correct PyS60 SDK for S60 SDK:[%default]")
    
    parser.add_option("-t", "--target-dir",
                  dest="target_dir", default=TARGET,
                  help="Folder where the files are downloaded:[%default]")
    
    parser.add_option("", "--tools-path", default=None,
                  help="Folder where the PythonForS60 tools are installed:[%default]")
    
    parser.add_option("-f", "--force-download",
                      action="store_true", dest="force_download", default=False,
                      help="Download new files even if they exist.")
    
    parser.add_option("-F", "--force-install",
                      action="store_true", dest="force_install", default=False,
                      help="Install new files even if they are already installed.")
    
    parser.add_option("", "--no-download",
                      action="store_false", dest="download", default=True,
                      help="Don't download new files.")
    
    parser.add_option("", "--no-install",
                      action="store_false", dest="install", default=True,
                      help="Don't install the files.")
                      
    parser.add_option("", "--no-openc",
                      action="store_false", dest="openc", default=True,
                      help="Don't get new OpenC.")
    
    parser.add_option("-c", "--clean",
                      action="store_true", dest="clean", default=False,
                      help="Clean the archive folder and exit." )

                          
    (options, args) = parser.parse_args()
    
    
    TARGET = options.target_dir
    if not TARGET.endswith("\\"):
        TARGET += "\\"
    
    if options.clean:
        files = glob.glob(TARGET + "*.*")    
        for file in files:
            os.remove(file)
        os.remove(TARGET)
        return
        
    if not os.path.exists( TARGET ):
        os.mkdir(TARGET)
    
    if options.download:
        download(options)
    if options.install:
        install(options) 
   
main()

