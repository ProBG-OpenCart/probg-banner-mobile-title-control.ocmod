from pathlib import Path
import xml.etree.ElementTree as ET

xml_path = Path('install.xml')
text = xml_path.read_text(encoding='utf-8')
text = text.replace('<version>1.1.0</version>', '<version>1.2.0</version>', 1)

old_banner_template = '''  <file path="admin/view/template/extension/module/banner.twig">
    <operation>
      <search><![CDATA[          <div class="form-group">
            <label class="col-sm-2 control-label" for="input-status">{{ entry_status }}</label>]]></search>
      <add position="before"><![CDATA[          <div class="form-group required">
            <label class="col-sm-2 control-label" for="input-mobile-width">{{ entry_mobile_width }}</label>
            <div class="col-sm-10">
              <input type="text" name="mobile_width" value="{{ mobile_width }}" placeholder="{{ entry_mobile_width }}" id="input-mobile-width" class="form-control" />
              {% if error_mobile_width %}
              <div class="text-danger">{{ error_mobile_width }}</div>
              {% endif %}
            </div>
          </div>
          <div class="form-group required">
            <label class="col-sm-2 control-label" for="input-mobile-height">{{ entry_mobile_height }}</label>
            <div class="col-sm-10">
              <input type="text" name="mobile_height" value="{{ mobile_height }}" placeholder="{{ entry_mobile_height }}" id="input-mobile-height" class="form-control" />
              {% if error_mobile_height %}
              <div class="text-danger">{{ error_mobile_height }}</div>
              {% endif %}
            </div>
          </div>
]]></add>
    </operation>
  </file>
'''

height_search = '''          <div class="form-group">
            <label class="col-sm-2 control-label" for="input-height">{{ entry_height }}</label>
            <div class="col-sm-10">
              <input type="text" name="height" value="{{ height }}" placeholder="{{ entry_height }}" id="input-height" class="form-control" />
              {% if error_height %}
              <div class="text-danger">{{ error_height }}</div>
              {% endif %}
            </div>
          </div>'''

mobile_fields = '''          <div class="form-group required">
            <label class="col-sm-2 control-label" for="input-mobile-width">{{ entry_mobile_width }}</label>
            <div class="col-sm-10">
              <input type="text" name="mobile_width" value="{{ mobile_width }}" placeholder="{{ entry_mobile_width }}" id="input-mobile-width" class="form-control" />
              {% if error_mobile_width %}
              <div class="text-danger">{{ error_mobile_width }}</div>
              {% endif %}
            </div>
          </div>
          <div class="form-group required">
            <label class="col-sm-2 control-label" for="input-mobile-height">{{ entry_mobile_height }}</label>
            <div class="col-sm-10">
              <input type="text" name="mobile_height" value="{{ mobile_height }}" placeholder="{{ entry_mobile_height }}" id="input-mobile-height" class="form-control" />
              {% if error_mobile_height %}
              <div class="text-danger">{{ error_mobile_height }}</div>
              {% endif %}
            </div>
          </div>'''

new_banner_template = f'''  <file path="admin/view/template/extension/module/banner.twig">
    <operation>
      <search><![CDATA[{height_search}]]></search>
      <add position="after"><![CDATA[
{mobile_fields}
]]></add>
    </operation>
  </file>
'''

if old_banner_template not in text:
    raise SystemExit('Existing Banner admin template OCMOD block was not found')
text = text.replace(old_banner_template, new_banner_template, 1)

def admin_controller(module):
    return f'''  <file path="admin/controller/extension/module/{module}.php">
    <operation>
      <search><![CDATA[$this->load->language('extension/module/{module}');]]></search>
      <add position="after"><![CDATA[
\t\t$this->load->language('extension/module/probg_banner_mobile_fields');]]></add>
    </operation>
    <operation>
      <search><![CDATA[\t\tif (isset($this->error['height'])) {{
\t\t\t$data['error_height'] = $this->error['height'];
\t\t}} else {{
\t\t\t$data['error_height'] = '';
\t\t}}]]></search>
      <add position="after"><![CDATA[

\t\tif (isset($this->error['mobile_width'])) {{
\t\t\t$data['error_mobile_width'] = $this->error['mobile_width'];
\t\t}} else {{
\t\t\t$data['error_mobile_width'] = '';
\t\t}}

\t\tif (isset($this->error['mobile_height'])) {{
\t\t\t$data['error_mobile_height'] = $this->error['mobile_height'];
\t\t}} else {{
\t\t\t$data['error_mobile_height'] = '';
\t\t}}]]></add>
    </operation>
    <operation>
      <search><![CDATA[\t\tif (isset($this->request->post['status'])) {{]]></search>
      <add position="before"><![CDATA[
\t\tif (isset($this->request->post['mobile_width'])) {{
\t\t\t$data['mobile_width'] = $this->request->post['mobile_width'];
\t\t}} elseif (!empty($module_info) && !empty($module_info['mobile_width'])) {{
\t\t\t$data['mobile_width'] = $module_info['mobile_width'];
\t\t}} else {{
\t\t\t$data['mobile_width'] = $data['width'];
\t\t}}

\t\tif (isset($this->request->post['mobile_height'])) {{
\t\t\t$data['mobile_height'] = $this->request->post['mobile_height'];
\t\t}} elseif (!empty($module_info) && !empty($module_info['mobile_height'])) {{
\t\t\t$data['mobile_height'] = $module_info['mobile_height'];
\t\t}} else {{
\t\t\t$data['mobile_height'] = $data['height'];
\t\t}}

]]></add>
    </operation>
    <operation>
      <search><![CDATA[\t\tif (!$this->request->post['height']) {{
\t\t\t$this->error['height'] = $this->language->get('error_height');
\t\t}}]]></search>
      <add position="after"><![CDATA[

\t\tif (empty($this->request->post['mobile_width']) || (int)$this->request->post['mobile_width'] < 1) {{
\t\t\t$this->error['mobile_width'] = $this->language->get('error_mobile_width');
\t\t}}

\t\tif (empty($this->request->post['mobile_height']) || (int)$this->request->post['mobile_height'] < 1) {{
\t\t\t$this->error['mobile_height'] = $this->language->get('error_mobile_height');
\t\t}}]]></add>
    </operation>
  </file>

'''

def admin_template(module):
    return f'''  <file path="admin/view/template/extension/module/{module}.twig">
    <operation>
      <search><![CDATA[{height_search}]]></search>
      <add position="after"><![CDATA[
{mobile_fields}
]]></add>
    </operation>
  </file>

'''

admin_marker = '  <!-- Build both desktop and mobile URLs and make hidden titles empty for custom themes. -->\n'
if admin_marker not in text:
    raise SystemExit('Catalog Banner marker was not found')

extra_admin = ''
for module in ('carousel', 'slideshow'):
    if f'<file path="admin/controller/extension/module/{module}.php">' not in text:
        extra_admin += admin_controller(module)
    if f'<file path="admin/view/template/extension/module/{module}.twig">' not in text:
        extra_admin += admin_template(module)
text = text.replace(admin_marker, extra_admin + admin_marker, 1)

def catalog_controller(module):
    return f'''  <!-- Responsive image data for the standard {module.capitalize()} module. -->
  <file path="catalog/controller/extension/module/{module}.php">
    <operation>
      <search><![CDATA[\t\tforeach ($results as $result) {{]]></search>
      <add position="before"><![CDATA[
\t\t$mobile_width = !empty($setting['mobile_width']) ? (int)$setting['mobile_width'] : (int)$setting['width'];
\t\t$mobile_height = !empty($setting['mobile_height']) ? (int)$setting['mobile_height'] : (int)$setting['height'];

]]></add>
    </operation>
    <operation>
      <search><![CDATA[\t\t\tif (is_file(DIR_IMAGE . $result['image'])) {{]]></search>
      <add position="after"><![CDATA[
\t\t\t\tif (!empty($result['mobile_image']) && is_file(DIR_IMAGE . $result['mobile_image'])) {{
\t\t\t\t\t$mobile_image = $this->model_tool_image->resize($result['mobile_image'], $mobile_width, $mobile_height);
\t\t\t\t}} else {{
\t\t\t\t\t$mobile_image = $this->model_tool_image->resize($result['image'], $mobile_width, $mobile_height);
\t\t\t\t}}
]]></add>
    </operation>
    <operation>
      <search><![CDATA[\t\t\t\t\t'title' => $result['title'],
\t\t\t\t\t'link'  => $result['link'],
\t\t\t\t\t'image' => $this->model_tool_image->resize($result['image'], $setting['width'], $setting['height'])]]></search>
      <add position="replace"><![CDATA[\t\t\t\t\t'title'        => !empty($result['hide_title']) ? '' : $result['title'],
\t\t\t\t\t'alt'          => $result['title'],
\t\t\t\t\t'hide_title'   => !empty($result['hide_title']) ? 1 : 0,
\t\t\t\t\t'link'         => $result['link'],
\t\t\t\t\t'image'        => $this->model_tool_image->resize($result['image'], $setting['width'], $setting['height']),
\t\t\t\t\t'mobile_image' => $mobile_image]]></add>
    </operation>
  </file>

'''

frontend_search = '<div class="swiper-slide text-center">{% if banner.link %}<a href="{{ banner.link }}"><img src="{{ banner.image }}" alt="{{ banner.title }}" class="img-responsive" /></a>{% else %}<img src="{{ banner.image }}" alt="{{ banner.title }}" class="img-responsive" />{% endif %}</div>'

def catalog_template(module):
    return f'''  <file path="catalog/view/theme/default/template/extension/module/{module}.twig">
    <operation>
      <search><![CDATA[{frontend_search}]]></search>
      <add position="replace"><![CDATA[<div class="swiper-slide text-center">
{{% if banner.link %}}<a href="{{{{ banner.link }}}}"{{% if banner.title %}} title="{{{{ banner.title }}}}"{{% endif %}}>{{% endif %}}
<picture style="display:block">
  {{% if banner.mobile_image %}}<source media="(max-width: 767px)" srcset="{{{{ banner.mobile_image }}}}" />{{% endif %}}
  <img src="{{{{ banner.image }}}}" alt="{{{{ banner.alt }}}}" class="img-responsive" />
</picture>
{{% if banner.link %}}</a>{{% endif %}}
</div>]]></add>
    </operation>
  </file>

'''

extra_catalog = ''
for module in ('carousel', 'slideshow'):
    if f'<file path="catalog/controller/extension/module/{module}.php">' not in text:
        extra_catalog += catalog_controller(module)
    if f'<file path="catalog/view/theme/default/template/extension/module/{module}.twig">' not in text:
        extra_catalog += catalog_template(module)
text = text.replace('</modification>', extra_catalog + '</modification>', 1)
text = text.replace('<!-- Extend the standard Banner module settings with mobile dimensions. -->', '<!-- Extend Banner, Carousel and Slideshow module settings with mobile dimensions. -->', 1)
xml_path.write_text(text, encoding='utf-8')
ET.parse(xml_path)

changelog = Path('CHANGELOG.md')
c = changelog.read_text(encoding='utf-8')
entry = '''## [1.2.0] - 2026-08-30

### feat

- Added `Mobile Width` and `Mobile Height` settings to the standard OpenCart Carousel module.
- Added `Mobile Width` and `Mobile Height` settings to the standard OpenCart Slideshow module.
- Added responsive mobile-image generation and `<picture>` output for the default Carousel and Slideshow storefront templates.
- Extended `Hide Title`, `alt`, and conditional link `title` handling to Carousel and Slideshow.

### fix

- Made the Banner admin-template modification more robust on OpenCart 3.0.3.8 by inserting the mobile dimension fields directly after the standard Height field instead of relying on the Status block.

'''
if '## [1.2.0]' not in c:
    c = c.replace('## [1.1.0]', entry + '## [1.1.0]', 1)
changelog.write_text(c, encoding='utf-8')

readme = Path('README.md')
r = readme.read_text(encoding='utf-8')
r = r.replace('Текуща версия: **1.1.0**', 'Текуща версия: **1.2.0**', 1)
r = r.replace('В настройките на всяка инстанция на стандартния модул **Banner** се добавят:', 'В настройките на всяка инстанция на стандартните модули **Banner**, **Carousel** и **Slideshow** се добавят:', 1)
r = r.replace('Отворете **Extensions → Extensions → Modules → Banner** и редактирайте съответната Banner инстанция.', 'Отворете **Extensions → Extensions → Modules** и редактирайте съответната инстанция на **Banner**, **Carousel** или **Slideshow**.', 1)
custom_note = '''
### Carousel и Slideshow при custom тема

От версия **1.2.0** responsive mobile изображенията се поддържат и от стандартните **Carousel** и **Slideshow** модули. Ако custom темата има собствени шаблони, приложете същата `<picture>` логика и в:

```text
catalog/view/theme/ИМЕ-НА-ТЕМАТА/template/extension/module/carousel.twig
catalog/view/theme/ИМЕ-НА-ТЕМАТА/template/extension/module/slideshow.twig
```

Използвайте `banner.mobile_image` за mobile source, `banner.image` за desktop изображението и `banner.alt` за `alt`. При линк добавяйте `title="{{ banner.title }}"` само когато `banner.title` не е празно.
'''
if '### Carousel и Slideshow при custom тема' not in r:
    r = r.replace('\n### След ръчната промяна\n', custom_note + '\n### След ръчната промяна\n', 1)
readme.write_text(r, encoding='utf-8')

readme_en = Path('README_EN.md')
e = readme_en.read_text(encoding='utf-8')
e = e.replace('Current version: **1.1.0**', 'Current version: **1.2.0**', 1)
e = e.replace('Each standard **Banner** module instance gets:', 'Each standard **Banner**, **Carousel**, and **Slideshow** module instance gets:', 1)
en_note = '''
### Carousel and Slideshow with a custom theme

Since **1.2.0**, responsive mobile images are also supported by the standard **Carousel** and **Slideshow** modules. If the active theme overrides their templates, apply the same `<picture>` logic to:

```text
catalog/view/theme/YOUR-THEME/template/extension/module/carousel.twig
catalog/view/theme/YOUR-THEME/template/extension/module/slideshow.twig
```

Use `banner.mobile_image` for the mobile source, `banner.image` for desktop, and `banner.alt` for the image alt text. For linked banners, add `title="{{ banner.title }}"` only when `banner.title` is not empty.
'''
if '### Carousel and Slideshow with a custom theme' not in e:
    e = e.replace('\n### After the manual change\n', en_note + '\n### After the manual change\n', 1)
readme_en.write_text(e, encoding='utf-8')
