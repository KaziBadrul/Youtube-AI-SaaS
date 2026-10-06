"""Application service layer."""
from alpha.services.projects import (
    autosave_project_settings,
    create_project,
    get_project,
    rename_project,
    reopen_project,
)
from alpha.services.script_projection import (
    compute_projection_payload,
    create_script_version,
    get_active_scenes,
    get_current_script_projection,
    get_current_script_text,
    get_scene,
    get_script_version,
    initialize_scenes_from_script,
    remove_scene_from_active_order,
    reorder_scenes,
    restore_scene_narration,
    update_scene_narration,
    update_scene_visuals,
)

__all__ = [
    "create_project",
    "get_project",
    "rename_project",
    "reopen_project",
    "autosave_project_settings",
    "create_script_version",
    "initialize_scenes_from_script",
    "update_scene_narration",
    "update_scene_visuals",
    "reorder_scenes",
    "remove_scene_from_active_order",
    "restore_scene_narration",
    "get_active_scenes",
    "get_scene",
    "get_current_script_projection",
    "get_script_version",
    "get_current_script_text",
    "compute_projection_payload",
]
