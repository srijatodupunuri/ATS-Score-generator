import json
import os

REPORT_FILE = "data/analysis_results.json"
HISTORY_FILE = "data/report_history.json"


def save_reports(results):

    os.makedirs(
        "data",
        exist_ok=True
    )

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )


def load_reports():

    if not os.path.exists(
        REPORT_FILE
    ):
        return []

    try:

        with open(
            REPORT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:  # noqa: BLE001
        return []
def save_report_history(results):

    history = load_report_history()

    from datetime import datetime, timezone

    history.append({

        "analysis_date":
        datetime.now(tz=timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S %Z"
        ),

        "candidates":
        results

    })

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            history,
            file,
            indent=4
        )


def load_report_history():

    if not os.path.exists(
        HISTORY_FILE
    ):
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:  # noqa: BLE001
        return []
