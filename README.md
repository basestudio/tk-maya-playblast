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

# Optional Configuration Fields

	  scale_options: [25, 100]

Configure a custom set of playblast resolution percentage, to be selected by user via UI.

	  temp_directory: "C:/Temp"

Configure a local path for playblast file creation before being copied into project folder. Path must be absolute.

# Added to Favourites menu
    menu_favourites:
    - {app_instance: tk-multi-workfiles, name: Shotgun File Manager...}
    - {app_instance: tk-multi-snapshot, name: Snapshot...}
    - {app_instance: tk-multi-workfiles, name: Shotgun Save As...}
    - {app_instance: tk-multi-publish, name: Publish...}
    - {app_instance: tk-maya-playblast, name: Maya Playblast...}
