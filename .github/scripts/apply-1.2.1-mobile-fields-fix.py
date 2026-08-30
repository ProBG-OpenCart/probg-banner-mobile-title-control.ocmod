from pathlib import Path
import re
import xml.etree.ElementTree as ET

xml_path = Path('install.xml')
text = xml_path.read_text(encoding='utf-8')
text = text.replace('<version>1.2.0</version>', '<version>1.2.1</version>', 1)

for module in ('banner', 'carousel', 'slideshow'):
    pattern = re.compile(
        r'(<file path="admin/view/template/extension/module/' + module + r'\.twig">\s*<operation>\s*)'
        r'<search><!\[CDATA\[.*?\]\]></search>\s*'
        r'<add position="after">',
        re.S,
    )
    replacement = (
        r'\1<search><![CDATA[</form>]]></search>\n'
        r'      <add position="before">'
    )
    text, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise SystemExit(f'Could not replace admin template anchor for {module}')

xml_path.write_text(text, encoding='utf-8')
ET.parse(xml_path)

changelog = Path('CHANGELOG.md')
changelog_text = changelog.read_text(encoding='utf-8')
entry = '''## [1.2.1] - 2026-08-30

### fix

- Fixed `Mobile Width` and `Mobile Height` fields not appearing in the Banner, Carousel, and Slideshow administration forms on some OpenCart 3 installations.
- Replaced fragile admin-template OCMOD anchors based on the full Height/Status markup with a stable insertion immediately before the module form closing tag.
- Improved compatibility with OpenCart 3.0.3.8 installations where another OCMOD or admin customization has already changed the standard module form markup.

'''
if '## [1.2.1]' not in changelog_text:
    marker = '## [1.2.0]'
    if marker not in changelog_text:
        raise SystemExit('Could not find 1.2.0 changelog marker')
    changelog_text = changelog_text.replace(marker, entry + marker, 1)
    changelog.write_text(changelog_text, encoding='utf-8')

readme = Path('README.md')
readme_text = readme.read_text(encoding='utf-8')
readme_text = readme_text.replace('Текуща версия: **1.2.0**', 'Текуща версия: **1.2.1**', 1)
needle_bg = 'При съществуващи Banner модули без въведени mobile размери се използват стандартните desktop размери като fallback.\n'
note_bg = '\nОт версия **1.2.1** полетата за mobile размери се добавят непосредствено преди края на формата на Banner, Carousel и Slideshow. Това избягва конфликт с други OCMOD модификации или admin теми, които променят стандартния HTML около полетата Width/Height/Status.\n'
if note_bg.strip() not in readme_text and needle_bg in readme_text:
    readme_text = readme_text.replace(needle_bg, needle_bg + note_bg, 1)
readme.write_text(readme_text, encoding='utf-8')

readme_en = Path('README_EN.md')
readme_en_text = readme_en.read_text(encoding='utf-8')
readme_en_text = readme_en_text.replace('Current version: **1.2.0**', 'Current version: **1.2.1**', 1)
needle_en = 'Existing Banner modules without mobile dimensions fall back to the standard desktop dimensions.\n'
note_en = '\nSince **1.2.1**, the mobile dimension fields are injected immediately before the end of the Banner, Carousel, and Slideshow admin forms. This avoids conflicts with other OCMOD modifications or admin customizations that change the standard Width/Height/Status markup.\n'
if note_en.strip() not in readme_en_text and needle_en in readme_en_text:
    readme_en_text = readme_en_text.replace(needle_en, needle_en + note_en, 1)
readme_en.write_text(readme_en_text, encoding='utf-8')

# Final structural assertions.
final_text = xml_path.read_text(encoding='utf-8')
if final_text.count('<search><![CDATA[</form>]]></search>') < 3:
    raise SystemExit('Expected three robust admin form anchors')
if '<version>1.2.1</version>' not in final_text:
    raise SystemExit('Version bump missing')

print('1.2.1 mobile dimension field visibility fix prepared successfully')
