Maya Playblast app for Shotgun Toolkit
======================================

This tool is meant to do the playblast, save the file in the directory and submit it to shotgun. We create a simple UI for it, and an interface to be used by other apps.

To enable the apps, additional lines added to environment config shot_step.yml under maya engine

    tk-maya-playblast:
      hook_post_playblast: default
      hook_setup_window: default
      location: {name: tk-maya-playblast, type: manual, version: v0.1.0}
      template_work: maya_shot_work
      template_shot: maya_shot_playblast
      template_sequence: maya_sequence_playblast

# added to favorite menu
    menu_favourites:
    - {app_instance: tk-multi-workfiles, name: Shotgun File Manager...}
    - {app_instance: tk-multi-snapshot, name: Snapshot...}
    - {app_instance: tk-multi-workfiles, name: Shotgun Save As...}
    - {app_instance: tk-multi-publish, name: Publish...}
    - {app_instance: tk-maya-playblast, name: Maya Playblast...}
