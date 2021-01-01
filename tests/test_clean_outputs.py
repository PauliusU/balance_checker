from p2p_balance_checker import clean_outputs


def test_get_float_from_html_tag():
    # No number provided
    assert clean_outputs.get_float_from_html_tag("") == 0
    assert clean_outputs.get_float_from_html_tag("<h1>Heading with no numbers</h1>") == 0

    # Comma separated decimals
    assert clean_outputs.get_float_from_html_tag("€1'958,86") == 1958.86
    assert clean_outputs.get_float_from_html_tag("€1.958,86") == 1958.86

    # Viventor 1
    assert clean_outputs.get_float_from_html_tag("€1'958.86") == 1958.86

    # Viventor 2
    assert clean_outputs.get_float_from_html_tag('<th class="hlp--ar ng-binding"> €1\'152.37</th>') == 1152.37

    # Grupeer
    assert clean_outputs.get_float_from_html_tag('<div class="block-value">&euro;3,147.95</div>') == 3147.95

    # Mintos
    assert clean_outputs.get_float_from_html_tag(
        "<h2 data-v-caa3bf6e=\"\" class=\"m-u-fs-2 m-u-fw-4 m-u-color-1-80--text"
        " m-u-margin-bottom-none m-u-margin-bottom--lg-6\"><span title=\"EUR\">€</span> 7 727.76</h2>") == 7727.76

    # RoboCash - small number
    assert clean_outputs.get_float_from_html_tag(
        '<div class="white-block-body"> <div class="left value digit"><span><!----> <!---->'
        ' <span class="value_roundings"> € 1.08 </span></span></div>'
        ' <div class="row"> <div class="col-sm-11 description">'
        'Includes investor’s balance, balance of portfolios and purchased loans. </div> </div> </div>') == 1.08

    assert clean_outputs.get_float_from_html_tag(
        "<h2 data-v-20e2179e=\"\" class=\"m-u-fs-2 m-u-fw-4 m-u-color-1-80--text m-u-margin-bottom-none "
        "m-u-margin-bottom--lg-6\">\n<span title=\"EUR\">â‚¬</span> 991.38</h2>") == 991.38


def test_get_html_tag_from_inner_html():
    # get one tag of many
    assert clean_outputs.get_html_tag_from_inner_html(
        "<span id=\"current\">EUR</span>"
        "<div data-v-caa3bf6e=\"\" class=\"m-u-fs-2 m-u-fw-4 m-u-color-1-80--text"
        " m-u-margin-bottom-none m-u-margin-bottom--lg-6\"><span title=\"EUR\">€</span> 7 727.76</div>"
        "<div id=\"amount\">7727.76</div>",
        "div#amount"
    ) == "<div id=\"amount\">7727.76</div>"
