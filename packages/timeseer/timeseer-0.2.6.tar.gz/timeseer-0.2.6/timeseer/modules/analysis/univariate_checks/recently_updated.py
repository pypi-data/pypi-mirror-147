"""Last updated point should not be longer than 24 hours.

<p>This check finds the last time a value was archived. If no value has been recorded in the last
24 hours, the tag might no longer be in use.</p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>
A series that no longer puts out any measurements might be faulty or could indicate a network failure.
Failing to detect this could lead to wrong process operation when attempting to obtain a particular
interval of operation.
</p>
</div>
"""

from datetime import timedelta

import timeseer

_CHECK_NAME = "Recently updated"

META: dict = {
    "checks": [{"name": _CHECK_NAME, "kpi": "Timeliness", "data_type": "bool"}],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 1,
        }
    ],
    "signature": "univariate",
}


def _is_last_point_old(analysis_input) -> bool:
    last_recorded_time = analysis_input.data.index[-1]
    last_evaluation_date = analysis_input.evaluation_time_range.end_date
    cutoff_date = last_evaluation_date - timedelta(days=1)
    return last_recorded_time <= cutoff_date


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    if len(analysis_input.data) == 0:
        return timeseer.AnalysisResult(condition_message="No data")

    is_too_old = _is_last_point_old(analysis_input)
    check = timeseer.CheckResult(_CHECK_NAME, float(is_too_old))
    return timeseer.AnalysisResult([check])
