"""OpenProject Projects - Project management operations."""

from .projects import (
    list_projects,
    get_project,
    create_project,
    update_project,
    delete_project,
    copy_project,
    get_versions,
    get_categories,
    get_types,
    toggle_favorite,
)

__all__ = [
    "list_projects",
    "get_project",
    "create_project",
    "update_project",
    "delete_project",
    "copy_project",
    "get_versions",
    "get_categories",
    "get_types",
    "toggle_favorite",
]
