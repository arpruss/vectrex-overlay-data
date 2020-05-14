import xml.etree.ElementTree as ET
import re
import sys
import os

def simplify(path):
    name = os.path.splitext(os.path.split(path)[1])[0]
    name = name.replace("II", "2").lower()
    name = re.sub(r'\s', '', name)
    name = re.sub(r'\(.*', '', name)
    return re.sub(r'[^a-zA-Z0-9]', '', name)
    
def find(name, names):
    name = simplify(name)
    if name in names:
        return names[name]
    for n in names:
        if name.startswith(n) or n.startswith(name):
            return names[n]
    return None
    
def fix(x):
    if x.startswith("--"):
        x = x[2:]
    if re.match(r'[0.]+$',x):
        return "0"
    else:
        return x

names = {simplify(arg):arg for arg in sys.argv[1:]}

root = ET.parse('configuration.xml').getroot()
for child in root:
    if child.tag == 'games':
        for game in child.findall('game'):
            name = game.attrib['name']
            for ov in game.findall('overlay'):
                s = find(name,names)
                if s:
                    out = os.path.splitext(s)[0]+".opt"
                    with open(out, "w") as f:
                        f.write('vecx_res_multi = "3"\n')
                        f.write('vecx_scale_x = "%s"\nvecx_scale_y = "%s"\nvecx_shift_x = "%s"\nvecx_shift_y = "%s"\n' % tuple(map(fix, (ov.attrib['sx'], ov.attrib['sy'], ov.attrib['tx'], '-'+ov.attrib['ty']))))
                else:
                    print("%s not found" % name)
