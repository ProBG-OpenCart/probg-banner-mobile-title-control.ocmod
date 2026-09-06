from pathlib import Path

xml = Path('install.xml')
s = xml.read_text(encoding='utf-8')

if '<version>1.2.3</version>' not in s:
    raise SystemExit('Expected version 1.2.3')
s = s.replace('<version>1.2.3</version>', '<version>1.2.4</version>', 1)

old = '''    <operation>
      <search><![CDATA[\t\t\t\t\t'title' => $result['title'],
\t\t\t\t\t'link'  => $result['link'],
\t\t\t\t\t'image' => $this->model_tool_image->resize($result['image'], $setting['width'], $setting['height'])]]></search>
      <add position="replace"><![CDATA[\t\t\t\t\t'title'        => !empty($result['hide_title']) ? '' : $result['title'],
\t\t\t\t\t'alt'          => $result['title'],
\t\t\t\t\t'hide_title'   => !empty($result['hide_title']) ? 1 : 0,
\t\t\t\t\t'link'         => $result['link'],
\t\t\t\t\t'image'        => $this->model_tool_image->resize($result['image'], $setting['width'], $setting['height']),
\t\t\t\t\t'mobile_image' => $mobile_image]]></add>
    </operation>'''

new = '''    <operation>
      <search><![CDATA['title' => $result['title'],]]></search>
      <add position="replace"><![CDATA['title'      => !empty($result['hide_title']) ? '' : $result['title'],
\t\t\t\t\t'alt'        => $result['title'],
\t\t\t\t\t'hide_title' => !empty($result['hide_title']) ? 1 : 0,]]></add>
    </operation>
    <operation>
      <search><![CDATA['image' => $this->model_tool_image->resize($result['image'], $setting['width'], $setting['height'])]]></search>
      <add position="replace"><![CDATA['image'        => $this->model_tool_image->resize($result['image'], $setting['width'], $setting['height']),
\t\t\t\t\t'mobile_image' => $mobile_image]]></add>
    </operation>'''

count = s.count(old)
if count != 3:
    raise SystemExit(f'Expected 3 frontend array operations, found {count}')
s = s.replace(old, new)
xml.write_text(s, encoding='utf-8')

cl = Path('CHANGELOG.md')
c = cl.read_text(encoding='utf-8')
marker = '## [1.2.3] - 2026-09-05\n'
entry = '''## [1.2.4] - 2026-09-06\n\n### fix\n\n- Fixed `mobile_image`, `hide_title`, and `alt` not reaching custom Banner/Carousel/Slideshow Twig templates when another theme or OCMOD changes the standard frontend banner array formatting.\n- Replaced the fragile three-line `title/link/image` array replacement with independent `title` and `image` operations.\n- Custom themes can now reliably use `banner.mobile_image`, `banner.hide_title`, and `banner.alt` without requiring the default OpenCart Twig template.\n- Applied the same frontend data fix to Banner, Carousel, and Slideshow.\n\n'''
if marker not in c:
    raise SystemExit('CHANGELOG marker not found')
c = c.replace(marker, entry + marker, 1)
cl.write_text(c, encoding='utf-8')

for name in ('README.md', 'README_EN.md'):
    p = Path(name)
    t = p.read_text(encoding='utf-8')
    if '**1.2.3**' not in t:
        raise SystemExit(f'Version marker missing in {name}')
    t = t.replace('**1.2.3**', '**1.2.4**', 1)
    p.write_text(t, encoding='utf-8')

print('Applied 1.2.4 frontend data fix')