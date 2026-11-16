"""Refresh the statistics card while keeping the displayed school email correct."""
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET

URL = "https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username=LinX-Wang&theme=github"
EMAIL = "shuai_wang@mail.nwpu.edu.cn"
ROOT = Path(__file__).resolve().parents[1]


def corrected_svg(svg):
    root = ET.fromstring(svg)
    assert root.tag.endswith("svg"), "Expected an SVG statistics card"
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    assert re.search(pattern, svg), "Statistics card has no email field"
    svg = re.sub(pattern, EMAIL, svg)
    svg = re.sub(r'font-size: 14px;(?=[^"]*">' + re.escape(EMAIL) + ')', 'font-size: 12px;', svg)
    assert EMAIL in svg and "qq.com" not in svg
    ET.fromstring(svg)
    return svg


if __name__ == "__main__":
    request = urllib.request.Request(URL, headers={"User-Agent": "LinX-profile-card"})
    with urllib.request.urlopen(request, timeout=45) as response:
        svg = corrected_svg(response.read().decode("utf-8"))
    (ROOT / "assets/profile-details-school.svg").write_text(svg, encoding="utf-8")
