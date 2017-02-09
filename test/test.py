from powerview_api.helpers.powerview_base import PowerViewBase


def test_sanitize_shades():
    pv_base = PowerViewBase('')
    shade_data = {"shadeData": [{}]}
    pv_base.sanitize_shades(shade_data)
    assert shade_data["shadeData"][0]["name"] == ''
