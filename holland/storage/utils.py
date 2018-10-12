import os
import json


def record(data, **storage_options):
    """
    Records data to a file

    :param data: the data to write to the file
    :type data: list/dict

    :param storage_options: options for writing the data to a file, specifically ``format`` (options: ``'json'``, ``'csv'``), ``file_name``, and ``path`` are relevant; see :ref:`fitness-storage-options` and :ref:`genome-storage-options`
    :type storage_options: dict


    :returns: ``None``


    Dependencies:
        * :func:`~holland.storage.utils.record_to_csv`
        * :func:`~holland.storage.utils.record_to_json`
    """
    storage_format = storage_options.get("format")
    if storage_format == "csv":
        record_to_csv(data, **storage_options)
    elif storage_format == "json":
        record_to_json(data, **storage_options)


def record_to_csv(data, **storage_options):
    """
    Writes data to a file CSV format; appends a row to an existing file; a file is created if none exists yet

    :param data: the data to write to the file (with column names as keys)
    :type data: dict

    :param storage_options: options for writing the data to a file, specifically ``file_name`` and ``path`` are relevant; see :ref:`fitness-storage-options` and :ref:`genome-storage-options`
    :type storage_options: dict


    :returns: ``None``


    :raises AssertionError: if storage_options["file_name"] is not specified
    :raises AssertionError: if storage_options["path"] is not specified
    :raises ValueError: if not all values are of type int or float
    """
    assert storage_options.get("file_name") is not None and storage_options.get("path") is not None

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
    """
    Writes data to a file JSON format; overwrites contents if the file already exists

    :param data: the data to write to the file (must be valid JSON format)
    :type data: list/dict

    :param storage_options: options for writing the data to a file, specifically ``file_name`` and ``path`` are relevant; see :ref:`fitness-storage-options` and :ref:`genome-storage-options`
    :type storage_options: dict


    :returns: ``None``


    :raises AssertionError: if storage_options["file_name"] is not specified
    :raises AssertionError: if storage_options["path"] is not specified
    """
    assert storage_options.get("file_name") is not None and storage_options.get("path") is not None

    file_name = storage_options["file_name"]
    file_path = storage_options["path"]
    full_path = os.path.join(file_path, file_name)

    stringified_data = json.dumps(data)
    with open(full_path, "w") as f:
        f.write(stringified_data)
