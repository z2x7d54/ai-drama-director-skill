"""Validate concrete examples and portable reading copies, not generated film quality.

Run: python tools/validate_course.py [--final]
Requires PyMuPDF for the PDF check. No network access is performed.
"""
from pathlib import Path
from decimal import Decimal
from urllib.parse import urlparse, unquote
import re, json, sys, zipfile, hashlib

ROOT = Path(__file__).resolve().parents[1]
master = (ROOT/'ai短剧导演skill-8.1版.md').read_text(encoding='utf-8-sig')
native = (ROOT/'ai-drama-director-storyboard/SKILL.md').read_text(encoding='utf-8-sig')
errors=[]
def check(condition, message):
    if not condition: errors.append(message)

check('version: "8.1"' in master and '# AI短剧导演 Skill｜8.1' in master, 'Version mismatch')
check('ASSET_COMMIT_81' not in master or '--final' not in sys.argv, 'Unresolved image commit')
for forbidden in ['朱啸笛', 'C:/Users/', 'C:\\Users\\', 'D:/codex', 'D:\\codex', 'ASSET81/']:
    check(forbidden not in master, 'Unexpected private/placeholder text: '+forbidden)
check('每次制作分镜表之前都必须重新阅读本节' in master, 'Missing mandatory precheck')
check('角度切换和联合组边界不重置' in master, 'Missing continuous kiss accounting')
check('剧本可能经压缩' in master, 'Missing source-gap procedure')

tags=re.findall(r'<img src="([^"]+)" alt="([^"]+)"\s*/>',master)
check(len(tags)==14, f'Expected 14 images, got {len(tags)}')
image_names=[]
for src,alt in tags:
    name=Path(urlparse(src).path).name;image_names.append(name)
    check((ROOT/'ai-drama-director-storyboard/assets'/name).is_file(), 'Missing image: '+name)
    check(len(alt)>15, 'Uninformative image description: '+name)
    if '--final' in sys.argv:
        check(bool(re.search(r'/[0-9a-f]{40}/ai-drama-director-storyboard/assets/',src)), 'Unpinned image: '+name)
check(len(set(image_names))==14, 'Duplicate/missing diagram placement')
local=re.sub(r'https://raw\.githubusercontent\.com/z2x7d54/ai-drama-director-skill/[^/]+/ai-drama-director-storyboard/assets/', 'assets/',master)
def body_without_note(text):
    return re.sub(r'<!-- cross-device-reading:start -->.*?<!-- cross-device-reading:end -->|> 原生skill图片位于包内assets；完整文字教学在本文件。单文件跨设备阅读可用根目录8.1版MD或内置图片PDF/HTML。','',text,flags=re.S).strip()
check(body_without_note(local)==body_without_note(native),'Native/master teaching text differs')

groups_total=shots_total=0
dialogue_cases=[]
for block in re.findall(r'```text\n(.*?)\n```',master,re.S):
    headers=list(re.finditer(r'^联合镜头(\d+)（镜头(\d+)—(\d+)，时长(\d+)秒）$',block,re.M))
    if not headers:continue  # The X/N format template is intentionally non-executable.
    dialogue=[];last_shot=0
    for index,header in enumerate(headers):
        gid,first,last,total=map(int,header.groups());groups_total+=1
        check(gid==index+1,'Group numbering does not start/continue at 1')
        check(first==last_shot+1,'Shot numbering gap')
        check(1<=total<=30,'Group duration out of range')
        content=block[header.end():headers[index+1].start() if index+1<len(headers) else len(block)]
        for field in ['出场人物：','场景参考：','道具参考：']:
            check(field in content.split('\n镜头',1)[0], f'Group {gid}: missing {field}')
        shots=list(re.finditer(r'^镜头(\d+)$',content,re.M));check(len(shots)==last-first+1,'Shot range/count mismatch')
        clock=Decimal(0)
        for j,shot in enumerate(shots):
            num=int(shot[1]);shots_total+=1
            check(num==first+j,'Shot number mismatch')
            scene=content[shot.end():shots[j+1].start() if j+1<len(shots) else len(content)]
            for field in ['景别：','机位：','运镜：','画面内容：','台词／OS：']:
                check(len(re.findall(r'^'+field,scene,re.M))==1,f'Shot {num}: missing/duplicate {field}')
            interval=re.search(r'画面内容：(\d+(?:\.\d+)?)—(\d+(?:\.\d+)?)秒',scene)
            check(interval is not None,f'Shot {num}: no concrete interval')
            if interval:
                a,b=map(Decimal,interval.groups());check(a==clock and b>a,f'Shot {num}: discontinuous/empty interval');clock=b
            line=re.search(r'^台词／OS：(.*)$',scene,re.M)
            if line:dialogue.extend(re.findall(r'：“([^”]*)”',line[1]))
        check(clock==Decimal(total),f'Group {gid}: total mismatch {clock}!={total}')
        last_shot=last
    dialogue_cases.append(dialogue)
check(groups_total==6 and shots_total==15, f'Expected 6 groups/15 shots: {groups_total}/{shots_total}')
expected=[['你就再陪我一会儿嘛。','好，陪你。'],['这个，','交给你？','交给我。'],['我以为你不来了。','我答应过你。','车备好了。','走吧。']]
check(dialogue_cases==expected,'Fictional source dialogue is missing, changed, repeated, or reordered')

portable={}
if '--final' in sys.argv or '--portable' in sys.argv:
    h=ROOT/'AI短剧导演skill_8.1_离线图文阅读版.html'
    html=h.read_text(encoding='utf8')
    check(html.count('src="data:image/png;base64,')==14,'HTML does not embed all images')
    check('ASSET_COMMIT_81' not in html,'HTML has unresolved commit')
    import fitz
    doc=fitz.open(ROOT/'AI短剧导演skill_8.1_跨设备阅读版.pdf')
    pdf_text=''.join(page.get_text() for page in doc)
    image_placements=sum(len(page.get_image_info()) for page in doc)
    check(image_placements==14,f'PDF has {image_placements} images')
    for needle in ['8.1','第一课','动画衔接','联合镜头3','车备好了','迁移练习','mr zhu']:
        check(needle in pdf_text,'PDF missing text: '+needle)
    check('\ufffd' not in pdf_text,'PDF contains replacement characters')
    pdf_fonts={f[3] for p in doc for f in p.get_fonts()}
    bundle=ROOT/'AI短剧导演skill_8.1_图文完整版.zip'
    with zipfile.ZipFile(bundle) as z:
        check(z.testzip() is None,'ZIP failed integrity test')
        names=set(z.namelist());offline=z.read('ai短剧导演skill-8.1版.md').decode('utf8')
        for src in re.findall(r'<img src="([^"]+)"',offline):
            check(src in names,'ZIP missing local figure: '+src)
        for src in re.findall(r'<img src="([^"]+)"',z.read('ai-drama-director-storyboard/SKILL.md').decode('utf8')):
            check('ai-drama-director-storyboard/'+src in names,'Native ZIP image missing: '+src)
        check('https://raw.githubusercontent.com/' not in offline,'Offline Markdown still depends on remote images')
        check(not any(n.startswith(('/', '../')) or '/..' in n for n in names),'Unsafe ZIP paths')
    portable={'pdf_pages':len(doc),'pdf_images':image_placements,'pdf_fonts':sorted(pdf_fonts),'html_embedded_images':14,'zip_members':len(names)}
result={'passed':not errors,'groups':groups_total,'shots':shots_total,'images':len(tags),'portable':portable,'errors':errors}
print(json.dumps(result,ensure_ascii=False,indent=2))
if errors:sys.exit(1)
