# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
An app that syncs the frame range between a scene and a shot in Shotgun.

"""
import tank
import traceback

class BasePlayblast(tank.platform.Application):
    playblastManager = None

    def init_app(self):
        """
        Called as the application is being initialized
        """
        self.engine.register_command("Playblast...", self.run_app)

    def destroy_app(self):
        """
        App teardown
        """
        self.log_debug("Destroying playblast app")
        
    def run_app(self):
        """
        Start doing playblast
        """
        try:
            playblastManager = self.get_playblast_manager()
            playblastManager.showDialog()
        except:
            traceback.print_exc()

    def get_playblast_manager(self):
        """
        Create a singleton PlayblastManager object to be used by any app.
        """
        if self.playblastManager is None:
            tk_maya_playblast = self.import_module("tk_maya_playblast")            
            self.playblastManager = tk_maya_playblast.PlayblastManager(self)
        return self.playblastManager
        
        
