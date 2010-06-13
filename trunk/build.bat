@echo off

"C:\python26\python" "source/setup.py" py2exe
"C:\Program Files\Inno Setup 5\Compil32.exe" /cc "source/pyge.iss"
'"C:\python26\python" "source/setup.py" py2app