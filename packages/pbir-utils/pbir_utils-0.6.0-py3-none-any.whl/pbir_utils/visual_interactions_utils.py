import json
import os

from .json_utils import _load_json, _write_json


def _get_visuals(visuals_folder: str) -> tuple:
    """
    Retrieves visual IDs and their types from the visuals folder.

    Args:
        visuals_folder (str): Path to the folder containing visual JSON files.

    Returns:
        Tuple[list, dict]: A tuple containing a list of visual IDs and a dictionary mapping visual IDs to their types.
    """
    visual_ids = []
    visual_types = {}

    for visual_folder in os.listdir(visuals_folder):
        visual_folder_path = os.path.join(visuals_folder, visual_folder)
        visual_file_path = os.path.join(visual_folder_path, "visual.json")

        if not os.path.isfile(visual_file_path):
            continue

        # Load the visual JSON data
        visual_json = _load_json(visual_file_path)

        visual_id = visual_json.get("name")

        # Skip visuals with a visualGroup
        if "visualGroup" in visual_json:
            continue

        visual_type = visual_json.get("visual", {}).get("visualType", "Unknown")
        if visual_id:
            visual_ids.append(visual_id)
            visual_types[visual_id] = visual_type

    return visual_ids, visual_types


def _update_interactions(
    existing_interactions: list,
    source_ids: list,
    target_ids: list,
    update_type: str = "Upsert",
    interaction_type: str = "NoFilter",
) -> list:
    """
    Updates visual interactions based on the update type and interaction type.

    Args:
        existing_interactions (list[dict]): List of existing visual interactions.
        source_ids (list[str]): List of source visual IDs.
        target_ids (list[str]): List of target visual IDs.
        update_type (str): Determines how interactions are handled. Options are "Upsert", "Insert", "Overwrite".
        interaction_type (str): Type of interaction to apply. Default is "NoFilter".

    Returns:
        list[dict]: Updated list of visual interactions.
    """
    if update_type == "Overwrite":
        new_interactions = [
            {"source": source_id, "target": target_id, "type": interaction_type}
            for source_id in source_ids
            for target_id in target_ids
            if source_id != target_id
        ]
        return new_interactions

    interactions_dict = {
        (item["source"], item["target"]): item for item in existing_interactions
    }

    if update_type in ["Upsert", "Insert"]:
        for source_id in source_ids:
            for target_id in target_ids:
                if source_id != target_id:
                    if (
                        update_type == "Upsert"
                        or (source_id, target_id) not in interactions_dict
                    ):
                        interactions_dict[(source_id, target_id)] = {
                            "source": source_id,
                            "target": target_id,
                            "type": interaction_type,
                        }

    return list(interactions_dict.values())


def _filter_ids_by_type(ids: set, types: list, visual_types: dict) -> set:
    """
    Filters a set of visual IDs by their types.

    Args:
        ids (set[str]): Set of visual IDs to filter.
        types (list[str] or None): List of allowed visual types. If None, no filtering is done.
        visual_types (dict[str, str]): Dictionary mapping visual IDs to their types.

    Returns:
        set[str]: Filtered set of visual IDs.
    """
    return {vid for vid in ids if not types or visual_types.get(vid) in types}


def _process_page(
    page_json_path: str,
    visuals_folder: str,
    source_ids: list,
    source_types: list,
    target_ids: list,
    target_types: list,
    update_type: str,
    interaction_type: str,
):
    """
    Processes and updates visual interactions for a specific page.

    Args:
        page_json_path (str): Path to the page JSON file.
        visuals_folder (str): Path to the folder containing visual JSON files.
        source_ids (list[str] or None): List of source visual IDs.
        source_types (list[str] or None): List of source visual types.
        target_ids (list[str] or None): List of target visual IDs.
        target_types (list[str] or None): List of target visual types.
        update_type (str): Determines how interactions are handled. Options are "Upsert", "Insert", "Overwrite".
        interaction_type (str): Type of interaction to apply. Default is "NoFilter".
    """
    page_json = _load_json(page_json_path)
    visual_ids, visual_types = _get_visuals(visuals_folder)

    target_ids = _filter_ids_by_type(
        set(target_ids or visual_ids), target_types, visual_types
    )
    source_ids = _filter_ids_by_type(
        set(source_ids or visual_ids), source_types, visual_types
    )

    updated_interactions = _update_interactions(
        page_json.get("visualInteractions", []),
        list(source_ids),
        list(target_ids),
        update_type,
        interaction_type,
    )
    page_json["visualInteractions"] = updated_interactions
    _write_json(page_json_path, page_json)


def _process_all_pages(
    report_path: str,
    pages: list = None,
    source_ids: list = None,
    source_types: list = None,
    target_ids: list = None,
    target_types: list = None,
    update_type: str = "Upsert",
    interaction_type: str = "NoFilter",
):
    """
    Processes all pages or specific pages based on provided parameters.

    Args:
        report_path (str): Path to the report folder.
        pages (list[str], optional): List of page names to process. If None, all pages are processed.
        source_ids (list[str], optional): List of source visual IDs.
        source_types (list[str], optional): List of source visual types.
        target_ids (list[str], optional): List of target visual IDs.
        target_types (list[str], optional): List of target visual types.
        update_type (str): Determines how interactions are handled. Options are "Upsert", "Insert", "Overwrite".
        interaction_type (str): Type of interaction to apply. Default is "NoFilter".
    """
    pages_folder = os.path.join(report_path, "definition", "pages")

    for root, _, files in os.walk(pages_folder):
        for file_name in files:
            if file_name.endswith("page.json"):
                file_path = os.path.join(root, file_name)
                page_json = _load_json(file_path)

                # Process the page if it's in the list or if all pages should be processed
                if not pages or page_json.get("displayName") in pages:
                    visuals_folder = os.path.join(os.path.dirname(file_path), "visuals")
                    if os.path.isdir(visuals_folder):
                        _process_page(
                            file_path,
                            visuals_folder,
                            source_ids,
                            source_types,
                            target_ids,
                            target_types,
                            update_type,
                            interaction_type,
                        )


def disable_visual_interactions(
    report_path: str,
    pages: list = None,
    source_visual_ids: list = None,
    source_visual_types: list = None,
    target_visual_ids: list = None,
    target_visual_types: list = None,
    update_type: str = "Upsert",
) -> None:
    """
    Main function to disable visual interactions based on provided parameters.

    Args:
        report_path (str): Path to the report folder.
        pages (list, optional): List of page names to process. If None, all pages are processed.
        source_visual_ids (list, optional): List of specific source visual IDs. If None, all visuals are used as sources.
        source_visual_types (list, optional): List of source visual types. If None, all visuals are used as sources.
        target_visual_ids (list, optional): List of specific target visual IDs. If None, all visuals are used as targets.
        target_visual_types (list, optional): List of target visual types. If None, all visuals are used as targets.
        update_type (str, optional): Determines how interactions are handled. Options are "Upsert", "Insert", "Overwrite". Default is "Upsert".

    Raises:
        ValueError: If any of the provided parameters are not lists when expected.
    """
    # Validate that parameters are lists if they are not None
    for param_name, param_value in {
        "pages": pages,
        "source_visual_ids": source_visual_ids,
        "source_visual_types": source_visual_types,
        "target_visual_ids": target_visual_ids,
        "target_visual_types": target_visual_types,
    }.items():
        if param_value is not None and not isinstance(param_value, list):
            raise ValueError(f"{param_name} must be a list")

    # Proceed with processing all pages
    _process_all_pages(
        report_path,
        pages,
        source_visual_ids,
        source_visual_types,
        target_visual_ids,
        target_visual_types,
        update_type,
        interaction_type="NoFilter",
    )
