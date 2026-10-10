"""One-time helper: turn the Weebly page bodies in the snapshot into plain Markdown.

Paragraph breaks come from <br>, </p> and </div>. Links are kept as [text](url).
Whitespace is normalised; wording is not changed.
Usage: python migration/extract.py <snapshot-file.html>
"""
import html, re, sys

def weebly_to_md(src: str) -> str:
    m = re.search(r'<div id="wsite-content".*', src, re.S)
    s = m.group(0) if m else src
    s = re.split(r'<div class="footer-wrap|<div id="footer|class="wsite-footer', s)[0]
    s = re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S)
    s = re.sub(r'<(strong|b)\b[^>]*>(.*?)</\1>', r'**\2**', s, flags=re.S)
    s = re.sub(r'<(em|i)\b[^>]*>(.*?)</\1>', r'*\2*', s, flags=re.S)
    s = re.sub(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>',
               lambda m: f'[{re.sub(r"<[^>]+>", "", m.group(2)).strip()}]({html.unescape(m.group(1))})', s, flags=re.S)
    s = re.sub(r'<br\s*/?>|</p>|</div>|</h\d>|</li>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s).replace('​', '').replace('\xa0', ' ')
    lines = [re.sub(r'[ \t]+', ' ', l).strip() for l in s.split('\n')]
    lines = [l for l in lines if l and 'dataLayer' not in l and 'gtag(' not in l and l != '}']
    return '\n\n'.join(lines).replace('** **', ' ')

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    print(weebly_to_md(open(sys.argv[1], encoding='utf-8', errors='ignore').read()))
