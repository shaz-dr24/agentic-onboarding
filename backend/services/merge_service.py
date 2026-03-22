def merge_data(existing, new_data):
    """
    Merge extracted data from multiple documents
    """

    if not isinstance(new_data, dict):
        return existing

    for key, value in new_data.items():
        if value and key not in existing:
            existing[key] = value

    return existing