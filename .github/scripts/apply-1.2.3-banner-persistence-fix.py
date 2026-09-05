from pathlib import Path
import re
import xml.etree.ElementTree as ET

xml_path = Path('install.xml')
text = xml_path.read_text(encoding='utf-8')

if '<version>1.2.2</version>' not in text:
    raise SystemExit('Expected version 1.2.2 not found')
text = text.replace('<version>1.2.2</version>', '<version>1.2.3</version>', 1)

# Replace the two fragile add/edit SQL fragment operations with one generic operation.
model_ops_pattern = re.compile(
    r'''    <operation>\n      <search><!\[CDATA\[image = '\" \.  \$this->db->escape\(\$banner_image\['image'\]\) \. \"', sort_order = '\" \.  \(int\)\$banner_image\['sort_order'\]\]\]></search>\n      <add position=\"replace\"><!\[CDATA\[image = '\" \.  \$this->db->escape\(\$banner_image\['image'\]\) \. \"', mobile_image = '\" \. \$this->db->escape\(isset\(\$banner_image\['mobile_image'\]\) \? \$banner_image\['mobile_image'\] : ''\) \. \"', hide_title = '\" \. \(int\)\(isset\(\$banner_image\['hide_title'\]\) \? \$banner_image\['hide_title'\] : 0\) \. \"', sort_order = '\" \.  \(int\)\$banner_image\['sort_order'\]\]\]></add>\n    </operation>\n    <operation>\n      <search><!\[CDATA\[image = '\" \.  \$this->db->escape\(\$banner_image\['image'\]\) \. \"', sort_order = '\" \. \(int\)\$banner_image\['sort_order'\]\]\]></search>\n      <add position=\"replace\"><!\[CDATA\[image = '\" \.  \$this->db->escape\(\$banner_image\['image'\]\) \. \"', mobile_image = '\" \. \$this->db->escape\(isset\(\$banner_image\['mobile_image'\]\) \? \$banner_image\['mobile_image'\] : ''\) \. \"', hide_title = '\" \. \(int\)\(isset\(\$banner_image\['hide_title'\]\) \? \$banner_image\['hide_title'\] : 0\) \. \"', sort_order = '\" \. \(int\)\$banner_image\['sort_order'\]\]\]></add>\n    </operation>'''
)
replacement = '''    <operation>
      <search><![CDATA[, sort_order = '" .]]></search>
      <add position="replace"><![CDATA[, mobile_image = '" . $this->db->escape(isset($banner_image['mobile_image']) ? $banner_image['mobile_image'] : '') . "', hide_title = '" . (int)(isset($banner_image['hide_title']) ? $banner_image['hide_title'] : 0) . "', sort_order = '" .]]></add>
    </operation>'''
text, count = model_ops_pattern.subn(replacement, text, count=1)
if count != 1:
    raise SystemExit(f'Failed to replace fragile model SQL operations: {count}')

old_model_read = '''    <operation>
      <search><![CDATA['image'      => $banner_image['image'],]]></search>
      <add position="after"><![CDATA[
\t\t\t\t'mobile_image' => isset($banner_image['mobile_image']) ? $banner_image['mobile_image'] : '',
\t\t\t\t'hide_title'   => isset($banner_image['hide_title']) ? (int)$banner_image['hide_title'] : 0,]]></add>
    </operation>'''
new_model_read = '''    <operation>
      <search><![CDATA['sort_order' => $banner_image['sort_order']]]></search>
      <add position="before"><![CDATA[
\t\t\t\t'mobile_image' => isset($banner_image['mobile_image']) ? $banner_image['mobile_image'] : '',
\t\t\t\t'hide_title'   => isset($banner_image['hide_title']) ? (int)$banner_image['hide_title'] : 0,]]></add>
    </operation>'''
if old_model_read not in text:
    raise SystemExit('Old model read operation not found')
text = text.replace(old_model_read, new_model_read, 1)

old_controller_ops = '''    <operation>
      <search><![CDATA[\t\t\t\t} else {
\t\t\t\t\t$image = '';
\t\t\t\t\t$thumb = 'no_image.png';
\t\t\t\t}]]></search>
      <add position="after"><![CDATA[

\t\t\t\tif (!empty($banner_image['mobile_image']) && is_file(DIR_IMAGE . $banner_image['mobile_image'])) {
\t\t\t\t\t$mobile_image = $banner_image['mobile_image'];
\t\t\t\t\t$mobile_thumb = $banner_image['mobile_image'];
\t\t\t\t} else {
\t\t\t\t\t$mobile_image = '';
\t\t\t\t\t$mobile_thumb = 'no_image.png';
\t\t\t\t}]]></add>
    </operation>
    <operation>
      <search><![CDATA['thumb'      => $this->model_tool_image->resize($thumb, 100, 100),]]></search>
      <add position="after"><![CDATA[
\t\t\t\t\t'mobile_image' => $mobile_image,
\t\t\t\t\t'mobile_thumb' => $this->model_tool_image->resize($mobile_thumb, 100, 100),
\t\t\t\t\t'hide_title'   => !empty($banner_image['hide_title']) ? 1 : 0,]]></add>
    </operation>'''
new_controller_op = '''    <operation>
      <search><![CDATA['sort_order' => $banner_image['sort_order']]]></search>
      <add position="before"><![CDATA[
\t\t\t\t\t'mobile_image' => (!empty($banner_image['mobile_image']) && is_file(DIR_IMAGE . $banner_image['mobile_image'])) ? $banner_image['mobile_image'] : '',
\t\t\t\t\t'mobile_thumb' => $this->model_tool_image->resize((!empty($banner_image['mobile_image']) && is_file(DIR_IMAGE . $banner_image['mobile_image'])) ? $banner_image['mobile_image'] : 'no_image.png', 100, 100),
\t\t\t\t\t'hide_title'   => !empty($banner_image['hide_title']) ? 1 : 0,]]></add>
    </operation>'''
if old_controller_ops not in text:
    raise SystemExit('Old controller image-state operations not found')
text = text.replace(old_controller_ops, new_controller_op, 1)

xml_path.write_text(text, encoding='utf-8')
ET.parse(xml_path)

# Changelog
changelog = Path('CHANGELOG.md')
cl = changelog.read_text(encoding='utf-8')
marker = '## [1.2.2] - 2026-08-30\n'
entry = '''## [1.2.3] - 2026-09-05\n\n### fix\n\n- Fixed selected `Mobile Image` and enabled `Hide Title` values not being persisted reliably when creating or editing a Design → Banner entry.\n- Replaced two whitespace-sensitive `banner_image` INSERT matches with one generic `sort_order` insertion that applies to both `addBanner()` and `editBanner()`.\n- Made `getBannerImages()` restoration of `mobile_image` and `hide_title` independent of column alignment/formatting in the standard array.\n- Simplified Design → Banners form restoration so mobile image path, thumbnail, and hide-title state are derived directly from each `$banner_image` row.\n\n'''
if marker not in cl:
    raise SystemExit('CHANGELOG 1.2.2 marker not found')
cl = cl.replace(marker, entry + marker, 1)
changelog.write_text(cl, encoding='utf-8')

for filename in ('README.md', 'README_EN.md'):
    path = Path(filename)
    content = path.read_text(encoding='utf-8')
    if '**1.2.2**' not in content:
        raise SystemExit(f'Current version marker missing in {filename}')
    content = content.replace('**1.2.2**', '**1.2.3**', 1)
    path.write_text(content, encoding='utf-8')

# Structural checks
root = ET.parse(xml_path).getroot()
assert root.findtext('version') == '1.2.3'
model_file = next(f for f in root.findall('file') if f.get('path') == 'admin/model/design/banner.php')
searches = [(op.findtext('search') or '').strip() for op in model_file.findall('operation')]
assert ", sort_order = '\" ." in searches
assert "'sort_order' => $banner_image['sort_order']" in searches
controller_file = next(f for f in root.findall('file') if f.get('path') == 'admin/controller/design/banner.php')
controller_searches = [(op.findtext('search') or '').strip() for op in controller_file.findall('operation')]
assert "'sort_order' => $banner_image['sort_order']" in controller_searches
print('1.2.3 banner extra-field persistence fix applied')
