import csv, json, re

# ── 1. Load karuta main CSV ──────────────────────────────────────────────────
karuta = {}
with open('/sessions/elegant-serene-newton/mnt/uploads/20220325_Matubarairohakaruta-dataset_UTF-8.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        num = r['番号']
        schools = []
        for i in range(1, 8):
            k = f'関連小学校{i}_学校名' if i != 4 else '関連小学校4__学校名'
            s = r.get(k, '').strip()
            if s and s != '***':
                s2 = s.replace('松原市立', '').replace('小学校', '')
                if s2 not in schools:
                    schools.append(s2)
        kws = [r.get(f'キーワード{i}', '').strip() for i in range(1, 11)]
        kws = [x for x in kws if x and x != '***']
        karuta[num] = {
            'num': num, 'yomiku': r['読み句'], 'kana': r['読み句_カナ'],
            'letter': r['読み句頭文字'], 'desc': r['解説'],
            'lat': float(r['緯度']) if r['緯度'] else None,
            'lng': float(r['経度']) if r['経度'] else None,
            'schools': schools,
            'region': r.get('現在の地域名1', '').strip(),
            'keywords': kws, 'ndl_img': None
        }

# ── 2. Load NDL image CSV ────────────────────────────────────────────────────
with open('/sessions/elegant-serene-newton/mnt/uploads/20200325_Osakafuzenshi4_Matubarairohakaruta_UTF-8.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        num = r['まつばらいろはかるた番号'].strip()
        img = r['原資料画像URL'].strip()
        if num in karuta and img and karuta[num]['ndl_img'] is None:
            karuta[num]['ndl_img'] = img

# ── 3. City archive thumbnail URLs (extracted from Chrome) ────────────────────
city_imgs = {
    'd0000001': 'https://www.city.matsubara.lg.jp/fs/2/0/9/4/6/8/_/d0000001_tn.jpg',
    'd0000002': 'https://www.city.matsubara.lg.jp/fs/2/0/9/4/6/9/_/d0000002_tn.jpg',
    'd0000003': 'https://www.city.matsubara.lg.jp/fs/2/0/9/4/7/1/_/d0000003_tn.jpg',
    'd0000004': 'https://www.city.matsubara.lg.jp/fs/2/0/9/4/7/3/_/d0000004_tn.jpg',
    'd0000005': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/0/2/_/d0000005_tn.jpg',
    'd0000006': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/1/1/_/d0000006_tn.jpg',
    'd0000008': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/4/7/_/d0000008_tn.jpg',
    'd0000009': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/3/2/_/d0000009_tn.jpg',
    'd0000010': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/3/8/_/d0000010_tn.jpg',
    'd0000012': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/7/6/_/d0000012_tn.jpg',
    'd0000016': 'https://www.city.matsubara.lg.jp/fs/2/0/9/4/7/4/_/d0000016_tn.jpg',
    'd0000020': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/7/9/_/d0000020_tn.jpg',
    'd0000023': 'https://www.city.matsubara.lg.jp/fs/2/0/9/6/2/4/_/d0000023_tn.jpg',
    'd0000026': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/1/4/_/d0000026_tn.jpg',
    'd0000031': 'https://www.city.matsubara.lg.jp/fs/2/0/9/4/9/1/_/d0000031_tn.jpg',
    'd0000033': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/7/0/_/d0000033_tn.jpg',
    'd0000034': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/6/8/_/d0000034_tn.jpg',
    'd0000035': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/7/3/_/d0000035_tn.jpg',
    'd0000036': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/1/3/_/d0000036_tn.jpg',
    'd0000037': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/7/4/_/d0000037_tn.jpg',
    'd0000039': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/9/6/_/d0000039_tn.jpg',
    'd0000040': 'https://www.city.matsubara.lg.jp/fs/2/0/9/4/7/6/_/d0000040_tn.jpg',
    'd0000041': 'https://www.city.matsubara.lg.jp/fs/2/0/9/4/7/9/_/d0000041_tn.jpg',
    'd0000042': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/0/5/_/d0000042_tn.jpg',
    'd0000044': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/0/9/_/d0000044_tn.jpg',
    'd0000048': 'https://www.city.matsubara.lg.jp/fs/2/0/9/6/1/2/_/d0000048_tn.jpg',
    'd0000049': 'https://www.city.matsubara.lg.jp/fs/2/0/9/6/1/4/_/d0000049_tn.jpg',
    'd0000050': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/1/8/_/d0000050_tn.jpg',
    'd0000056': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/4/1/_/d0000056_tn.jpg',
    'd0000059': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/3/4/_/d0000059_tn.jpg',
    'd0000062': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/8/1/_/d0000062_tn.jpg',
    'd0000063': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/8/2/_/d0000063_tn.jpg',
    'd0000064': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/8/3/_/d0000064_tn.jpg',
    'd0000065': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/4/9/_/d0000065_tn.jpg',
    'd0000067': 'https://www.city.matsubara.lg.jp/fs/2/0/9/6/0/2/_/d0000067_tn.jpg',
    'd0000069': 'https://www.city.matsubara.lg.jp/fs/2/0/9/6/0/8/_/d0000069_tn.jpg',
    'd0000079': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/5/8/_/d0000079_tn.jpg',
    'd0000083': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/8/6/_/d0000083_tn.jpg',
    'd0000084': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/8/7/_/d0000084_tn.jpg',
    'd0000087': 'https://www.city.matsubara.lg.jp/fs/2/0/9/4/8/5/_/d0000087_tn.jpg',
    'd0000088': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/2/3/_/d0000088_tn.jpg',
    'd0000089': 'https://www.city.matsubara.lg.jp/fs/2/0/9/5/2/5/_/d0000089_tn.jpg',
}

# ── 4. Best image per karuta number ──────────────────────────────────────────
best_img = {
    'k01': city_imgs.get('d0000005'),       # map near 柴籬 area (no dedicated photo)
    'k02': city_imgs['d0000001'],
    'k03': city_imgs['d0000002'],
    'k04': city_imgs['d0000003'],
    'k05': city_imgs['d0000016'],
    'k06': None,                             # 準備中
    'k07': city_imgs['d0000040'],
    'k08': city_imgs['d0000087'],
    'k09': city_imgs['d0000064'],
    'k10': city_imgs['d0000031'],
    'k11': None,
    'k12': None,
    'k13': city_imgs['d0000005'],
    'k14': city_imgs['d0000042'],
    'k15': city_imgs['d0000006'],
    'k16': city_imgs['d0000036'],
    'k17': None,                             # 準備中
    'k18': city_imgs['d0000088'],
    'k19': city_imgs['d0000059'],
    'k20': city_imgs['d0000056'],
    'k21': city_imgs['d0000065'],
    'k22': city_imgs['d0000037'],
    'k23': city_imgs['d0000012'],
    'k24': city_imgs['d0000079'],
    'k25': None,                             # 準備中
    'k26': city_imgs['d0000020'],
    'k27': None,                             # 準備中
    'k28': city_imgs['d0000063'],
    'k29': city_imgs['d0000039'],
    'k30': None,
    'k31': None,
    'k32': city_imgs['d0000067'],
    'k33': None,
    'k34': None,
    'k35': None,
    'k36': None,
    'k37': None,
    'k38': None,
    'k39': city_imgs['d0000069'],
    'k40': city_imgs['d0000084'],
    'k41': city_imgs['d0000048'],
    'k42': None,
    'k43': None,
    'k44': None,
    'k45': None,
    'k46': city_imgs['d0000089'],
    'k47': city_imgs['d0000023'],
}
# Fill in NDL images where city image is missing
for num, k in karuta.items():
    if best_img.get(num) is None and k['ndl_img']:
        best_img[num] = k['ndl_img']

# ── 5. Name / category / url per karuta ──────────────────────────────────────
meta = {
    'k01': ('柴籬神社・柴籬宮址', '史跡', 'https://www.city.matsubara.lg.jp/soshiki/bunkazai/1/1/4/3008.html'),
    'k02': ('我堂八幡宮の力石', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k03': ('熱田神社のキリシタン灯籠', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k04': ('今池堤・西除川', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k05': ('安明寺の聖観音', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k06': ('布忍神社の扁額', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k07': ('立部の土師器・古墳群', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k08': ('ちちかみ橋道標', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k09': ('阿保親王社', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k10': ('大林寺の十一面観音', '美術・工芸', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k11': ('松原の印材産業', '美術・工芸', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k12': ('松原の金網産業', '美術・工芸', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k13': ('聖堂池・王仁博士ゆかりの地', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k14': ('立部遺跡・河内画師の地', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k15': ('追分地蔵・道標', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k16': ('丹南藩陣屋址', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k17': ('田坐神社', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k18': ('池内遺跡・弥生の水田', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k19': ('北山橘庵旧跡・一津屋', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k20': ('屯倉神社（天神様）', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k21': ('竹内街道・丹比道', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k22': ('来迎寺のいぶき', '天然記念物', 'https://www.city.matsubara.lg.jp/soshiki/bunkazai/1/1/4/3009.html'),
    'k23': ('高野街道の石標', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k24': ('長尾街道・大津道', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k25': ('弘法井戸', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k26': ('親王池址', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k27': ('大庄屋の門がまえ（西川家）', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k28': ('阿保神社の大楠', '天然記念物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k29': ('大和川付け替え跡', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k30': ('松原中央公園・市制施行の地', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k31': ('けんね塚（きつね山古墳）', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k32': ('河合の古池・だんじり', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k33': ('松原ジャンクション周辺', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k34': ('若林の古戦場', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k35': ('一津屋古墳・かねつき山', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k36': ('松原市セーフコミュニティ', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k37': ('西方寺', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k38': ('半夏生の風習・丹南地区', '美術・工芸', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k39': ('河内大塚山古墳', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k40': ('酒屋神社・屯倉神社の名水', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k41': ('三宅の木綿産業', '美術・工芸', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k42': ('天美小学校の二宮金次郎像', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k43': ('阿麻美許曾神社境外末社', '建造物', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k44': ('一津屋のトリキ', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k45': ('弁天池跡', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k46': ('河内鋳物師の遺跡', '史跡', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
    'k47': ('妻屋秀員・積翠集', '美術・工芸', 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'),
}

# ── 6. Simplified kids descriptions ──────────────────────────────────────────
def make_kids(desc, name, cat, keywords):
    # Extract first sentence or two, simplify
    sentences = re.split(r'[。！？]', desc)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    core = sentences[0] if sentences else desc[:80]
    # Add category-based hook
    hooks = {
        '史跡': '🗺️ むかし、ここには大切な場所がありました。',
        '建造物': '🏛️ このたてものには、むかしの人たちの知恵がつまっています。',
        '美術・工芸': '🎨 松原のじまん！むかしから続く職人の技です。',
        '天然記念物': '🌳 何百年もの時間を生きてきた、すごい自然の宝物！',
    }
    hook = hooks.get(cat, '📜 松原市の大切な文化財です。')
    # Add karuta connection
    return f'{hook}\n{core}。'

# ── 7. カナ reading for name ──────────────────────────────────────────────────
# We'll use the 読み句_カナ as the kana for the site
def extract_site_kana(yomiku_kana, name):
    # Just use empty for now, we'll use the yomiku_kana
    return ''

# ── 8. Build DATA array ──────────────────────────────────────────────────────
entries = []
archive_url = 'https://www.city.matsubara.lg.jp/docs/culturalheritage_digitalarchive_karuta.html'

for idx, num in enumerate(sorted(karuta.keys()), 1):
    k = karuta[num]
    name, cat, url = meta[num]
    img = best_img.get(num, '')
    school = k['schools'][0] if k['schools'] else ''
    desc = k['desc']
    kids = make_kids(desc, name, cat, k['keywords'])
    
    entry = {
        'id': idx,
        'karuta': num,
        'letter': k['letter'],
        'yomiku': k['yomiku'],
        'name': name,
        'kana': k['kana'][:20] if k['kana'] else '',
        'school': school,
        'cat': cat,
        'bunrui': f"まつばらいろはかるた {num}",
        'lat': k['lat'],
        'lng': k['lng'],
        'desc': desc,
        'kids': kids,
        'url': archive_url,
        'img': img or '',
    }
    entries.append(entry)

# ── 9. Output as JS ──────────────────────────────────────────────────────────
def js_str(s):
    if s is None:
        return '``'
    s = s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    return f'`{s}`'

lines = ['const DATA = [']
for e in entries:
    img = f'`{e["img"]}`' if e['img'] else '``'
    lines.append(f'  {{')
    lines.append(f'    id:{e["id"]}, karuta:{js_str(e["karuta"])}, letter:{js_str(e["letter"])},')
    lines.append(f'    yomiku:{js_str(e["yomiku"])},')
    lines.append(f'    name:{js_str(e["name"])},')
    lines.append(f'    kana:{js_str(e["kana"])},')
    lines.append(f'    school:{js_str(e["school"])}, cat:{js_str(e["cat"])},')
    lines.append(f'    bunrui:{js_str(e["bunrui"])},')
    lines.append(f'    lat:{e["lat"]}, lng:{e["lng"]},')
    lines.append(f'    desc:{js_str(e["desc"])},')
    lines.append(f'    kids:{js_str(e["kids"])},')
    lines.append(f'    url:{js_str(e["url"])},')
    lines.append(f'    img:{img},')
    lines.append(f'    sub:[]')
    lines.append(f'  }},')
lines.append('];')

js_output = '\n'.join(lines)
with open('/sessions/elegant-serene-newton/mnt/outputs/karuta_data.js', 'w', encoding='utf-8') as f:
    f.write(js_output)

print(f"Generated {len(entries)} entries")
print("Sample entry k22:")
e22 = next(e for e in entries if e['karuta'] == 'k22')
print(f"  name: {e22['name']}")
print(f"  school: {e22['school']}")
print(f"  img: {e22['img']}")
print(f"  desc[:80]: {e22['desc'][:80]}")
print(f"  kids: {e22['kids'][:100]}")
