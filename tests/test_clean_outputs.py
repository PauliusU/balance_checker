from p2p_balance_checker import clean_outputs


def test_get_float_from_html_string():

    # No number provided
    assert clean_outputs.get_float_from_html_string("") == 0
    assert clean_outputs.get_float_from_html_string("<h1>Heading with no numbers</h1>") == 0

    # Comma separated numbers
    assert clean_outputs.get_float_from_html_string("€1'958,86") == 1958.86
    assert clean_outputs.get_float_from_html_string("€1.958,86") == 1958.86

    # Viventor 1
    assert clean_outputs.get_float_from_html_string("€1'958.86") == 1958.86

    # Viventor 2
    assert clean_outputs.get_float_from_html_string('<th class="hlp--ar ng-binding"> €1\'152.37</th>') == 1152.37

    # Grupeer
    assert clean_outputs.get_float_from_html_string('<div class="block-value">&euro;3,147.95</div>') == 3147.95

    # Mintos
    assert clean_outputs.get_float_from_html_string(
        "<h2 data-v-caa3bf6e=\"\" class=\"m-u-fs-2 m-u-fw-4 m-u-color-1-80--text"
        " m-u-margin-bottom-none m-u-margin-bottom--lg-6\"><span title=\"EUR\">€</span> 7 727.76</h2>") == 7727.76