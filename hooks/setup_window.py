# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import re

import maya.cmds as cmds
import pymel.core as pm
import traceback
from contextlib import contextmanager

import tank
from tank import Hook

PLAYBLAST_WINDOW = "Playblast Window"

DEFAULT_WIDTH = 720
DEFAULT_HEIGHT = 540

MODEL_EDITOR_PARAMS = {
    "activeView": True,
    "cameras": False,
    "controlVertices": False,
    "deformers": False,
    "dimensions": False,
    "displayAppearance": "smoothShaded",
    "displayLights": "default",
    "displayTextures": True,
    "dynamicConstraints": False,
    "fogging": False,
    "follicles": False,
    "grid": False,
    "handles": False,
    "headsUpDisplay": True,
    "hulls": False,
    "ignorePanZoom": False,
    "ikHandles": False,
    "imagePlane": False,
    "joints": False,
    "lights": False,
    "locators": False,
    "manipulators": False,
    "nurbsCurves": False,
    "nurbsSurfaces": False,
    "pivots": False,
    "planes": False,
    "selectionHiliteDisplay": False,
    "shadows": False,
    "sortTransparent": True,
    "strokes": True,
    "textures": True,
    "useDefaultMaterial": False,
    "wireframeOnShaded": False,
    }

PLAYBLAST_PARAMS = {
    "forceOverwrite": True,
    "format": "qt",
    "framePadding": 4,
    "compression": "H.264",
    "offScreen": True,
    "percent": 100,
    "showOrnaments": True,
    "viewer": False,
    "sequenceTime": 0,
    "clearCache": True,
    "quality": 70,
    }

class SetupWindow(Hook):
    """
    Hook called when creating playblast
    """
    
    def execute(self, action='', data=[], **kwargs):
        """
        Main hook entry point
        
        :action:        String
                        hud_set             -> set required HUDs
                        hud_unset           -> removed added HUDs, restoring back to original setup
                        playblast_params    -> read playblast parameters
                        create_window       -> return function to create playblast window
        """
        if action == 'hud_set':
            visibleHUDs = [f for f in pm.headsUpDisplay(listHeadsUpDisplays=True)
                                   if pm.headsUpDisplay(f, query=True, visible=True)]
            # hide all visible HUDs
            map(lambda f: pm.headsUpDisplay(f, edit=True, visible=False), visibleHUDs)
            
            # Add required HUD
            # User name
            editExistingHUD = 'HUDUserName' in pm.headsUpDisplay( listHeadsUpDisplays=True )
            pm.headsUpDisplay( 'HUDUserName', edit=editExistingHUD,
                               command=lambda: os.getenv("USERNAME", "unknown.user"),
                               event='playblasting', section=1, block=1 )
            pm.headsUpDisplay( 'HUDUserName', edit=True, visible=True, label="User:" )
            # Scene name
            editExistingHUD = 'HUDSceneName' in pm.headsUpDisplay( listHeadsUpDisplays=True )
            pm.headsUpDisplay( 'HUDSceneName', edit=editExistingHUD,
                               command=lambda: cmds.file(query=True, location=True, shortName=True).rsplit(".", 1)[0],
                               event='playblasting', section=6, block=1 )
            pm.headsUpDisplay( 'HUDSceneName', edit=True, visible=True, label="Shot:" )
            # Focal length            
            pm.headsUpDisplay( 'HUDFocalLength', edit=True, visible=True, section=3, block=1 )
            pm.headsUpDisplay( 'HUDCurrentFrame', edit=True, visible=True, dataFontSize="large", section=8, block=1 )

            return visibleHUDs
            
        elif action == 'hud_unset':
            # restore HUD state
            map(lambda f: pm.headsUpDisplay(f, edit=True, visible=False), pm.headsUpDisplay(listHeadsUpDisplays=True))
            map(lambda f: pm.headsUpDisplay(f, edit=True, visible=True), data)
            return None
            
        elif action == "playblast_params":
            PLAYBLAST_PARAMS["filename"] = data
            # include audio if available
            audioList = pm.ls(type="audio")
            if audioList:
                PLAYBLAST_PARAMS["sound"] = audioList[0]
            return PLAYBLAST_PARAMS
            
        elif action == "create_window":
            # setting up context window for playblast
            @contextmanager
            def createWindow():
                """ try to get data from shotgun project fields
                    need to get context's project
                                context's shotgun instance
                """
                app = self.parent
                project = app.context.project
                sg = app.context.tank.shotgun
                # set filters and search fields for entity type "Project"
                filters=[["id", "is", project['id']],]
                fields=["sg_width", "sg_height"]
                result=sg.find_one("Project", filters, fields)
                # with result, set parameters accordingly or use default otherwise
                if result:
                    videoWidth = result.get("sg_width", DEFAULT_WIDTH)
                    videoHeight = result.get("sg_height", DEFAULT_HEIGHT)

                # Find first camera matching pattern and set as active camera
                # if not use default current active camera
                camera_name_pattern = app.get_setting( "camera_name_pattern", "persp" )
                cameraList = [c.name() for c in pm.ls(type="camera", r=True) if re.search( camera_name_pattern, c.name() )]
                if not "cam" in MODEL_EDITOR_PARAMS.keys() and cameraList:
                    MODEL_EDITOR_PARAMS["cam"] = cameraList[0]
                    
                # Give Viewport 2.0 renderer only for Maya 2015++
                # mayaVersionString = cmds.about(version=True)
                # mayaVersion = int(mayaVersionString[:4]) if len(mayaVersionString) >= 4 else 0
                # if mayaVersion >= 2015:
                #     params[ "rendererName" ] = "vp2Renderer"

                # Create window
                if pm.windowPref( PLAYBLAST_WINDOW, exists=True ):
                    pm.windowPref( PLAYBLAST_WINDOW, remove=True )
                window = pm.window( PLAYBLAST_WINDOW, titleBar=True, iconify=True,
                                      leftEdge = 100, topEdge = 100,
                                      width = videoWidth, height = videoHeight,
                                      sizeable = False)
                # Create editor area
                layout = pm.formLayout()
                editor = pm.modelEditor( **MODEL_EDITOR_PARAMS )
                pm.setFocus( editor )
                pm.formLayout( layout, edit=True,
                               attachForm = ( ( editor, "left", 0 ),
                                              ( editor, "top", 0 ),
                                              ( editor, "right", 0 ),
                                              ( editor, "bottom", 0 ) ) )
                # Show window
                pm.setFocus( editor )
                pm.showWindow( window )
                pm.refresh()
                try:
                    yield True
                except:
                    traceback.print_exc()
                finally:
                    pm.deleteUI(window)

            return createWindow
        else:
            self._app.log_info("nothing to work on")
