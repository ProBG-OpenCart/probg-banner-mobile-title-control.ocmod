from pathlib import Path
import xml.etree.ElementTree as ET

xml_path = Path('install.xml')
tree = ET.parse(xml_path)
root = tree.getroot()

version = root.find('version')
if version is None or version.text != '1.2.1':
    raise SystemExit(f'Unexpected version: {None if version is None else version.text}')
version.text = '1.2.2'

controller_paths = {
    'admin/controller/extension/module/banner.php',
    'admin/controller/extension/module/carousel.php',
    'admin/controller/extension/module/slideshow.php',
}

changed = {}
for file_el in root.findall('file'):
    path = file_el.get('path')
    if path not in controller_paths:
        continue

    flags = {'errors': False, 'values': False, 'validation': False}

    for operation in file_el.findall('operation'):
        search = operation.find('search')
        add = operation.find('add')
        if search is None or add is None:
            continue
        text = search.text or ''

        if "if (isset($this->error['height']))" in text:
            search.text = "$data['breadcrumbs'] = array();"
            add.set('position', 'before')
            flags['errors'] = True
        elif "if (isset($this->request->post['status']))" in text:
            search.text = "$data['header'] = $this->load->controller('common/header');"
            add.set('position', 'before')
            flags['values'] = True
        elif "if (!$this->request->post['height'])" in text:
            search.text = 'return !$this->error;'
            add.set('position', 'before')
            flags['validation'] = True

    changed[path] = flags

for path in controller_paths:
    flags = changed.get(path)
    if not flags or not all(flags.values()):
        raise SystemExit(f'Failed to update all controller anchors for {path}: {flags}')

ET.indent(tree, space='  ')
tree.write(xml_path, encoding='utf-8', xml_declaration=True)

text = xml_path.read_text(encoding='utf-8')
text = text.replace("<?xml version='1.0' encoding='utf-8'?>", '<?xml version="1.0" encoding="utf-8"?>', 1)
xml_path.write_text(text, encoding='utf-8')

changelog = Path('CHANGELOG.md')
cl = changelog.read_text(encoding='utf-8')
marker = '## [1.2.1] - 2026-08-30\n'
entry = '''## [1.2.2] - 2026-08-30\n\n### fix\n\n- Fixed `Mobile Width` and `Mobile Height` values appearing not to persist after saving Banner, Carousel, or Slideshow module instances.\n- Reworked the admin-controller OCMOD anchors used to restore saved mobile dimensions from module settings.\n- Mobile dimension values are now populated immediately before rendering the module form, using POST values first, then saved module settings, then desktop dimensions as fallback.\n- Made mobile-dimension error mapping and validation anchors more tolerant of other OpenCart OCMOD/admin customizations.\n\n'''
if marker not in cl:
    raise SystemExit('CHANGELOG 1.2.1 marker not found')
cl = cl.replace(marker, entry + marker, 1)
changelog.write_text(cl, encoding='utf-8')

for filename in ('README.md', 'README_EN.md'):
    p = Path(filename)
    s = p.read_text(encoding='utf-8')
    if '**1.2.1**' not in s:
        raise SystemExit(f'Current version marker not found in {filename}')
    s = s.replace('**1.2.1**', '**1.2.2**', 1)
    p.write_text(s, encoding='utf-8')

# Reparse after serialization. Detailed anchor validation is performed by the workflow
# against parsed XML elements, avoiding false failures from XML escaping.
ET.parse(xml_path)
if '<version>1.2.2</version>' not in xml_path.read_text(encoding='utf-8'):
    raise SystemExit('Version update was not serialized')

print('1.2.2 persistence fix applied and validated')
