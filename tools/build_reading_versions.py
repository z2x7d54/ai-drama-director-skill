"""Build standalone HTML/PDF reading copies and refresh the illustrated ZIP.

Run from any location: python tools/build_reading_versions.py
Dependencies: pip install markdown reportlab
The main Markdown remains the canonical agent input; native skill assets stay local.
"""
from pathlib import Path
import base64
import html
from html.parser import HTMLParser
import io
import re
from urllib.parse import quote, urlparse
import zipfile

import markdown
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable
from PIL import Image as PILImage

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / 'ai短剧导演skill-8.0版.md'
HTML_NAME = 'AI短剧导演skill_8.0_离线图文阅读版.html'
PDF_NAME = 'AI短剧导演skill_8.0_跨设备阅读版.pdf'
ASSETS = ROOT / 'ai-drama-director-storyboard' / 'assets'
IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

def local_image(url):
    name = Path(urlparse(url).path).name
    path = ASSETS / name
    if not path.is_file() or path.suffix != '.png':
        raise ValueError(f'Unexpected teaching image: {url}')
    return path

source = MASTER.read_text(encoding='utf-8-sig')
body = re.sub(r'\A---\n.*?\n---\n', '', source, count=1, flags=re.S)
# Reading-copy links are unnecessary inside the reading copy itself.
body = re.sub(r'<!-- cross-device-reading:start -->.*?<!-- cross-device-reading:end -->\n*', '', body, flags=re.S)
embedded = IMAGE_RE.sub(lambda m: f'![{m[1]}](data:image/png;base64,{base64.b64encode(local_image(m[2]).read_bytes()).decode("ascii")})', body)
rendered = markdown.markdown(embedded, extensions=['tables', 'fenced_code', 'toc'])
document = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI短剧导演 Skill 8.0 — mr zhu</title>
<style>
:root{color-scheme:light}body{margin:0;background:#f4f6fa;color:#182b43;font:17px/1.85 system-ui,-apple-system,"Microsoft YaHei",sans-serif}
main{max-width:920px;margin:auto;padding:26px 22px 70px;background:white}h1,h2,h3,h4{line-height:1.5;scroll-margin-top:20px}h2{margin-top:2.2em;border-bottom:1px solid #dae2ec;padding-bottom:.35em}
img{max-width:100%;height:auto;display:block;margin:20px auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f5f8;padding:16px;border-radius:8px;font-size:.9em}code{font-family:ui-monospace,"Microsoft YaHei",monospace}
blockquote{margin:18px 0;padding:10px 16px;border-left:4px solid #5680b0;background:#f5f8fc}table{border-collapse:collapse;width:100%;font-size:.92em;table-layout:fixed}th,td{border:1px solid #d8e0ea;padding:9px;vertical-align:top;overflow-wrap:anywhere}th{background:#edf3fa}a{color:#235f9c}header{padding:16px;background:#edf5fb;border-radius:8px}
@media(max-width:600px){body{font-size:16px}main{padding:18px 14px}th,td{padding:6px;font-size:14px}}
@media print{main{max-width:none;padding:0}body{background:white}img,table{break-inside:avoid}}
</style></head><body><main><header><strong>图片已内置的离线阅读版 · mr zhu</strong><br>本文件包含全部规则、教学正文及17张图片，无需图片文件夹或联网。若聊天软件不预览HTML，请下载后用浏览器打开，或使用配套PDF。给智能体制作分镜时优先发送完整版MD。</header>
''' + rendered + '</main></body></html>'
(ROOT / HTML_NAME).write_text(document, encoding='utf-8', newline='\n')

# Parse Markdown-generated HTML into a small DOM for the PDF flowables.
class Node:
    def __init__(self, tag, attrs=()):
        self.tag, self.attrs, self.children = tag, dict(attrs), []

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root')
        self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in {'img', 'br', 'hr', 'meta', 'input'}:
            self.stack.append(node)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break
    def handle_data(self, data):
        self.stack[-1].children.append(data)

font_paths = [Path('C:/Windows/Fonts/simsun.ttc'), Path('/usr/share/fonts/truetype/arphic/uming.ttc')]
font = next((path for path in font_paths if path.is_file()), None)
if font:
    pdfmetrics.registerFont(TTFont('ReadingCJK', str(font), subfontIndex=0))
else:
    # CID fallback remains readable; a local TrueType font embeds better across devices.
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
font_name = 'ReadingCJK' if font else 'STSong-Light'
pdfmetrics.registerFontFamily(font_name,normal=font_name,bold=font_name,italic=font_name,boldItalic=font_name)
normal = ParagraphStyle('Body', fontName=font_name, fontSize=10.5, leading=17, wordWrap='CJK', spaceAfter=8, textColor=colors.HexColor('#182b43'))
small = ParagraphStyle('Small', parent=normal, fontSize=8.4, leading=13, spaceAfter=3)
code = ParagraphStyle('Code', parent=normal, fontSize=9.0, leading=14, backColor=colors.HexColor('#f2f5f9'), borderPadding=9, spaceBefore=7, spaceAfter=10)
headings = {i: ParagraphStyle(f'H{i}', parent=normal, fontSize={1:21,2:16,3:13,4:11.5,5:11,6:10.5}[i], leading={1:29,2:24,3:20,4:18,5:17,6:17}[i], spaceBefore=18, spaceAfter=10, keepWithNext=True) for i in range(1,7)}
page_w, page_h = A4
width = page_w - 84
available_h = page_h - 90

def text_content(node):
    return node if isinstance(node,str) else ''.join(text_content(child) for child in node.children)

def inline(node):
    if isinstance(node,str):
        return html.escape(node)
    content = ''.join(inline(child) for child in node.children)
    if node.tag == 'br': return '<br/>'
    if node.tag in {'strong','b'}: return f'<b>{content}</b>'
    if node.tag in {'em','i'}: return f'<i>{content}</i>'
    if node.tag == 'a':
        href = node.attrs.get('href','')
        if href.startswith(('https://','http://')):
            return f'<a href="{html.escape(quote(href, safe=":/?&=#%"), quote=True)}" color="#235f9c">{content}</a>'
    return content

def figure(node):
    path = local_image(node.attrs['src'])
    with PILImage.open(path) as im: w,h = im.size
    scale = min(width/w, (available_h-42)/h)
    image = Image(str(path), width=w*scale, height=h*scale)
    image.hAlign='CENTER'
    return [Spacer(1,8), image, Paragraph(html.escape(node.attrs.get('alt','')), small), Spacer(1,10)]

def descend(node, tag):
    if isinstance(node,str): return []
    found = [node] if node.tag == tag else []
    for child in node.children: found.extend(descend(child,tag))
    return found

def flows(node):
    if isinstance(node,str): return []
    if node.tag in {'root','blockquote','div'}:
        return [flow for child in node.children for flow in flows(child)]
    if re.fullmatch(r'h[1-6]', node.tag):
        return [Paragraph(inline(node), headings[int(node.tag[1])])]
    if node.tag == 'img': return figure(node)
    if node.tag == 'p':
        images = [child for child in node.children if isinstance(child,Node) and child.tag=='img']
        if images: return [flow for child in images for flow in figure(child)]
        return [Paragraph(inline(node), normal)]
    if node.tag == 'pre':
        lines = text_content(node).rstrip().split('\n')
        return [Paragraph('<br/>'.join(html.escape(line).replace('  ','&#160;&#160;') or '&#160;' for line in lines), code)]
    if node.tag in {'ul','ol'}:
        result=[]
        for i,child in enumerate((c for c in node.children if isinstance(c,Node) and c.tag=='li'),1):
            marker=f'{i}. ' if node.tag=='ol' else '• '
            result.append(Paragraph(marker+inline(child),normal))
        return result
    if node.tag == 'table':
        rows=[]
        for tr in descend(node,'tr'):
            cells=[c for c in tr.children if isinstance(c,Node) and c.tag in {'th','td'}]
            rows.append([Paragraph(inline(cell),small) for cell in cells])
        columns=max(map(len,rows))
        table=Table(rows,colWidths=[width/columns]*columns,repeatRows=1,hAlign='LEFT',splitByRow=1,splitInRow=1)
        table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#edf3fa')),('GRID',(0,0),(-1,-1),.45,colors.HexColor('#cdd8e6')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
        return [table,Spacer(1,10)]
    if node.tag == 'hr': return [HRFlowable(width='100%',color=colors.HexColor('#cdd8e6')),Spacer(1,8)]
    return [flow for child in node.children for flow in flows(child)]

parser = Parser()
parser.feed(markdown.markdown(body,extensions=['tables','fenced_code']))
story = [Paragraph('跨设备图文阅读版 · 图片已内置 · mr zhu',headings[2]),Paragraph('本PDF包含完整版规则、三份教学附录和全部讲解图片。手机或电脑单独打开即可阅读，无需联网获取图片。制作分镜时优先给智能体发送完整版MD。',normal)] + flows(parser.root)

def footer(canvas,doc):
    canvas.saveState()
    canvas.setFont(font_name,8)
    canvas.setFillColor(colors.HexColor('#64748b'))
    canvas.drawString(42,24,'AI短剧导演 Skill 8.0 · mr zhu')
    canvas.drawRightString(page_w-42,24,str(doc.page))
    canvas.restoreState()

pdf=SimpleDocTemplate(str(ROOT/PDF_NAME),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=42,bottomMargin=42,title='AI短剧导演 Skill 8.0 — 跨设备图文阅读版',author='mr zhu',pageCompression=1)
pdf.build(story,onFirstPage=footer,onLaterPages=footer)

bundle=ROOT/'AI短剧导演skill_8.0_图文完整版.zip'
members=['ai短剧导演skill-8.0版.md','8.0启动指令.txt','分镜自检系统_8.0独立版.md','8.0升级说明与验证记录.md',HTML_NAME,PDF_NAME]
with zipfile.ZipFile(bundle,'w',compression=zipfile.ZIP_DEFLATED) as archive:
    for name in members:
        if name == MASTER.name:
            offline = IMAGE_RE.sub(lambda m:f'![{m[1]}](ai-drama-director-storyboard/assets/{local_image(m[2]).name})',source)
            offline = re.sub(r'<!-- cross-device-reading:start -->.*?<!-- cross-device-reading:end -->', '<!-- cross-device-reading:start -->\n> **ZIP离线版：**请完整解压并保留图片目录。本MD使用包内图片；只发送一个文件阅读时，请发送配套PDF或HTML。制作分镜时使用本MD，图片不可见时以完整文字教学为依据，不声称已看见图片。\n<!-- cross-device-reading:end -->',offline,flags=re.S)
            archive.writestr(name,offline.encode('utf-8'))
        else:
            archive.write(ROOT/name,name)
    for path in sorted((ROOT/'ai-drama-director-storyboard').rglob('*')):
        if path.is_file(): archive.write(path,path.relative_to(ROOT).as_posix())
with zipfile.ZipFile(bundle) as archive:
    assert archive.testzip() is None
print(f'Built {HTML_NAME}, {PDF_NAME}, and {bundle.name}; {len(IMAGE_RE.findall(body))} image placements.')
