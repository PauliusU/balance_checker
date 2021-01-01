import re
import bs4 as bs


def get_html_tag_from_inner_html(inner_html: str, tag_selector: str) -> str:
    if inner_html:
        soup: bs.BeautifulSoup = bs.BeautifulSoup(inner_html, 'lxml')
        html_tag: bs.element.Tag = soup.select_one(tag_selector)

        return str(html_tag)

    print("inner_HTML string is empty")
    return ""


def get_float_from_html_tag(html_string: str) -> float:
    """ Extract float from HTML string"""

    # remove all spaces
    html_string: str = html_string.replace(" ", "")

    contained_numbers: list = re.findall(r"\d+", html_string)

    if not contained_numbers:
        print("html_string does not have any number in it")
        return 0

    r"""Get <list> of <strings> with thousand separator ["1'152.37", "1,234.5"]
        
    \d+     1 or more digits
    [',.]   apostrophe, comma or dot (THOUSANDS SEPARATOR). No space because they are replaced earlier
    \d+     1 or more digits
    [.,]    dot or comma (DECIMAL SEPARATOR)
    \d+     1 or more digits
    
    E.g. 1'234.5 
     """
    thousand_separated_numbers: list = re.findall(r"\d+[',.]\d+[.,]\d+", html_string)

    if thousand_separated_numbers:
        comma_separated_decimals = re.findall(r"\d+,\d{1,2}$", html_string)

        if comma_separated_decimals:
            comma_number: str = re.sub(r"[^\d,]", "", thousand_separated_numbers[0])
            dot_number: str = comma_number.replace(",", ".")
            return float(dot_number)

        # If decimals are separated by dot:
        # Anything matching (that isn't a number or a decimal point (dot)) is replaced with "",
        # i.e. remains only numbers and decimal points a.k.a remove comma and other symbols
        filtered_string: str = re.sub(r"[^\d\.]", "", thousand_separated_numbers[0])
        return float(filtered_string)

    decimal_only_separated_numbers: list = re.findall(r"\d+[.,]\d+", html_string)

    if decimal_only_separated_numbers:
        return float(decimal_only_separated_numbers[0])

    integers: list = re.findall(r"\d+", html_string)

    if integers:
        # E.g. <h1>Heading with no numbers</h1> has integers, but no balance
        print(f"{integers} doe's not contain valid balance value")
        return 0
