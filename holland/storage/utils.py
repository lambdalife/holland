import os
import json


def record(data, **storage_options):
    storage_format = storage_options.get("format")
    if storage_format == "csv":
        record_to_csv(data, **storage_options)
    elif storage_format == "json":
        record_to_json(data, **storage_options)


def record_to_csv(data, **storage_options):
    assert (
        storage_options.get("file_name") is not None
        and storage_options.get("path") is not None
    )

    if not all(type(value) in [int, float] for value in data.values()):
        raise ValueError("Data values must be of type int or float.")

    file_name = storage_options["file_name"]
    file_path = storage_options["path"]
    full_path = os.path.join(file_path, file_name)

    sorted_data = sorted(list(data.items()), key=lambda x: x[0])

    if not os.path.exists(full_path):
        with open(full_path, "w") as f:
            f.write(",".join([k for k, v in sorted_data]))
            f.write("\n")

    with open(full_path, "a") as f:
        f.write(",".join([str(v) for k, v in sorted_data]))
        f.write("\n")


def record_to_json(data, **storage_options):
    assert (
        storage_options.get("file_name") is not None
        and storage_options.get("path") is not None
    )

    file_name = storage_options["file_name"]
    file_path = storage_options["path"]
    full_path = os.path.join(file_path, file_name)

    stringified_data = json.dumps(data)
    with open(full_path, "w") as f:
        f.write(stringified_data)
