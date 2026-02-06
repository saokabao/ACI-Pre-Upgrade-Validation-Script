import os
import pytest
import logging
import importlib
from helpers.utils import read_data

script = importlib.import_module("aci-preupgrade-validation-script")

log = logging.getLogger(__name__)
dir = os.path.dirname(os.path.abspath(__file__))

test_function = "nutanix_microsegmentation_custom_epg_name_check"

compeppd_api = 'compEpPD.json'
compeppd_api += '?query-target-filter=and(wcard(compEpPD.dn,"Nutanix"),ne(compEpPD.customEpgName,""),eq(compEpPD.configFlags,""))'

fvesg_api = 'fvESg.json'
fvesg_api += '?query-target-filter=and(ne(fvESg.customTagValue,""))'


@pytest.mark.parametrize(
    "icurl_outputs, cversion, tversion, expected_result",
    [
        (
            {
                compeppd_api: read_data(dir, "compEpPD_neg.json"),
                fvesg_api: read_data(dir, "fvESg_neg.json"),
            },
            script.AciVersion("6.2(2a)"),
            script.AciVersion("6.1(2a)"),
            script.PASS,
        ),
        (
            {
                compeppd_api: read_data(dir, "compEpPD_pos.json"),
                fvesg_api: read_data(dir, "fvESg_neg.json"),
            },
            script.AciVersion("6.2(2a)"),
            script.AciVersion("6.1(2a)"),
            script.FAIL_O,
        ),
        (
            {
                compeppd_api: read_data(dir, "compEpPD_neg.json"),
                fvesg_api: read_data(dir, "fvESg_pos.json"),
            },
            script.AciVersion("6.2(2a)"),
            script.AciVersion("6.1(2a)"),
            script.FAIL_O,
        ),
        (
            {
                compeppd_api: read_data(dir, "compEpPD_pos.json"),
                fvesg_api: read_data(dir, "fvESg_pos.json"),
            },
            script.AciVersion("6.2(2a)"),
            script.AciVersion("6.1(2a)"),
            script.FAIL_O,
        ),
    ],
)
def test_logic(run_check, mock_icurl, cversion, tversion, expected_result):
    result = run_check(cversion=cversion, tversion=tversion)
    assert result.result == expected_result