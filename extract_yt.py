import re

path = r"C:\Users\fores\.gemini\antigravity\brain\03dfae24-11f2-4e27-81ca-ebbfd9ce783f\.system_generated\steps\281\content.md"
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

title_m = re.search(r'<title>(.*?)</title>', text)
if title_m:
    print("PAGE TITLE:", title_m.group(1))

meta_title = re.search(r'<meta name="title" content="(.*?)">', text)
if meta_title:
    print("META TITLE:", meta_title.group(1))

meta_desc = re.search(r'<meta name="description" content="(.*?)">', text)
if meta_desc:
    print("META DESC:", meta_desc.group(1))

og_title = re.search(r'<meta property="og:title" content="(.*?)">', text)
if og_title:
    print("OG TITLE:", og_title.group(1))

og_desc = re.search(r'<meta property="og:description" content="(.*?)">', text)
if og_desc:
    print("OG DESC:", og_desc.group(1))
