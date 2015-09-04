@echo off
rem The path to output all built .py files to: 
set UI_PYTHON_PATH=../python/tk_maya_playblast/ui

call pyside-uic --from-imports playblast_dialog.ui -o playblast_dialog.py
sed -i "" -e "s/from PySide import/from tank.platform.qt import/g" -e "/# Created:/d" playblast_dialog.py
move playblast_dialog.py %UI_PYTHON_PATH%

pyside-rcc resources.qrc > resources_rc.py
sed -i "" -e "s/from PySide import/from tank.platform.qt import/g" -e "/# Created:/d" resources_rc.py
move resources_rc.py %UI_PYTHON_PATH%

set UI_PYTHON_PATH=
