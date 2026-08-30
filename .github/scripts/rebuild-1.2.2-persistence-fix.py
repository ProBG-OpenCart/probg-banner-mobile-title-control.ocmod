from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

FILES_TO_RESTORE = ['install.xml', 'CHANGELOG.md', 'README.md', 'README_EN.md']
for filename in FILES_TO_RESTORE:
    content = subprocess.check_output(['git', 'show', f'origin/main:{filename}'])
    Path(filename).write_bytes(content)

xml_path = Path('install.xml')
text = xml_path.read_text(encoding='utf-8')
if '<version>1.2.1</version>' not in text:
    raise SystemExit('Expected 1.2.1 in main install.xml')
text = text.replace('<version>1.2.1</version>', '<version>1.2.2</version>', 1)

controller_paths = [
    'admin/controller/extension/module/banner.php',
    'admin/controller/extension/module/carousel.php',
    'admin/controller/extension/module/slideshow.php',
]

operation_re = re.compile(
    r'(<operation>\s*<search><!\[CDATA\[)(.*?)(\]\]></search>\s*<add position=")(after|before)("><!\[CDATA\[)(.*?)(\]\]></add>\s*</operation>)',
    re.S,
)

for path in controller_paths:
    file_re = re.compile(
        rf'(<file path="{re.escape(path)}">)(.*?)(</file>)',
        re.S,
    )
    file_match = file_re.search(text)
    if not file_match:
        raise SystemExit(f'Controller file block not found: {path}')

    body = file_match.group(2)
    flags = {'errors': False, 'values': False, 'validation': False}

    def replace_operation(match):
        search_text = match.group(2)
        position = match.group(4)
        new_search = search_text
        new_position = position

        if "if (isset($this->error['height']))" in search_text:
            new_search = "$data['breadcrumbs'] = array();"
            new_position = 'before'
            flags['errors'] = True
        elif "if (isset($this->request->post['status']))" in search_text:
            new_search = "$data['header'] = $this->load->controller('common/header');"
            new_position = 'before'
            flags['values'] = True
        elif "if (!$this->request->post['height'])" in search_text:
            new_search = 'return !$this->error;'
            new_position = 'before'
            flags['validation'] = True

        return ''.join([
            match.group(1), new_search, match.group(3), new_position,
            match.group(5), match.group(6), match.group(7)
        ])

    new_body = operation_re.sub(replace_operation, body)
    if not all(flags.values()):
        raise SystemExit(f'Not all controller operations patched for {path}: {flags}')

    text = text[:file_match.start()] + file_match.group(1) + new_body + file_match.group(3) + text[file_match.end():]

xml_path.write_text(text, encoding='utf-8')

# Changelog and docs.
changelog = Path('CHANGELOG.md')
cl = changelog.read_text(encoding='utf-8')
marker = '## [1.2.1] - 2026-08-30\n'
entry = '''## [1.2.2] - 2026-08-30\n\n### fix\n\n- Fixed `Mobile Width` and `Mobile Height` values appearing not to persist after saving Banner, Carousel, or Slideshow module instances.\n- Reworked the admin-controller OCMOD anchors used to restore saved mobile dimensions from module settings.\n- Mobile dimension values are now populated immediately before rendering the module form, using POST values first, then saved module settings, then desktop dimensions as fallback.\n- Made mobile-dimension error mapping and validation anchors more tolerant of other OpenCart OCMOD/admin customizations.\n\n'''
if marker not in cl:
    raise SystemExit('CHANGELOG 1.2.1 marker not found')
changelog.write_text(cl.replace(marker, entry + marker, 1), encoding='utf-8')

for filename in ('README.md', 'README_EN.md'):
    p = Path(filename)
    s = p.read_text(encoding='utf-8')
    if '**1.2.1**' not in s:
        raise SystemExit(f'Current version marker not found in {filename}')
    p.write_text(s.replace('**1.2.1**', '**1.2.2**', 1), encoding='utf-8')

# Validate without rewriting XML, so CDATA and formatting stay untouched.
root = ET.parse(xml_path).getroot()
if root.findtext('version') != '1.2.2':
    raise SystemExit('Version validation failed')

seen = set()
for file_el in root.findall('file'):
    path = file_el.get('path')
    if path not in controller_paths:
        continue
    searches = [(op.findtext('search') or '').strip() for op in file_el.findall('operation')]
    required = {
        "$data['breadcrumbs'] = array();",
        "$data['header'] = $this->load->controller('common/header');",
        'return !$this->error;',
    }
    if not required.issubset(set(searches)):
        raise SystemExit(f'Structural validation failed for {path}')
    seen.add(path)

if seen != set(controller_paths):
    raise SystemExit(f'Missing controller validation: {seen}')

print('Minimal 1.2.2 persistence fix rebuilt successfully')
