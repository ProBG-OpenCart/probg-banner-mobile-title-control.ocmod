# ProBG Banner Mobile & Title Control

OCMOD extension for OpenCart 3 that enhances the standard banner system with a separate mobile image, mobile image dimensions, and per-banner title visibility control.

Bulgarian documentation: [README.md](README.md)

## Version

Current version: **1.2.1**

Release history is maintained in [CHANGELOG.md](CHANGELOG.md).

## Compatibility

The extension is designed for OpenCart 3 and follows the standard banner structure used by:

- OpenCart 3.0.2.0
- OpenCart 3.0.3.7
- OpenCart 3.0.3.8
- OpenCart 3.0.3.9

No core files are modified directly. All standard-file changes are applied through OCMOD.

## Main features

### Mobile image for every banner

A new **Mobile Image** field is added to every banner row in **Design → Banners**.

Each banner can therefore have:

- a desktop image;
- a mobile image;
- separate images for every language version.

If no mobile image is selected, the desktop image is used as a fallback.

### Mobile image dimensions

Each instance of the standard OpenCart **Banner** module receives two additional settings:

- **Mobile Width**;
- **Mobile Height**.

Desktop dimensions continue to use OpenCart's standard Width and Height settings.

For existing Banner module instances without mobile dimensions, the desktop Width/Height values are used as fallback values.

### Hide banner title

Every banner row in **Design → Banners** receives a **Hide Title** checkbox.

When enabled:

- the title is not exposed as visible title data to the storefront template;
- the original title remains available as the image `alt` text for accessibility and SEO.

This allows custom themes that render `banner.title` to suppress it for individual banners.

### Responsive storefront output

The standard OpenCart Banner template is changed to use HTML `<picture>` markup:

- up to `767px`, the mobile image is loaded;
- above `767px`, the desktop image is loaded.

The browser chooses the appropriate source without JavaScript device detection.

## Database changes

The extension uses the following additional fields in the standard `banner_image` table:

```text
mobile_image VARCHAR(255)
hide_title TINYINT(1)
```

Starting with version **1.0.1**, the schema is checked automatically before a banner is created or edited. If either column is missing, it is created before the banner data is written. This prevents the `Unknown column 'mobile_image' in 'INSERT INTO'` error even when the OCMOD modification becomes active before the helper module install method has run.

These columns are intentionally preserved during uninstall so mobile-image selections and title-visibility settings are not lost during reinstall or upgrade.

## Installation

1. Download the ready-to-install `.ocmod.zip` package for the current version.
2. In OpenCart admin, open **Extensions → Installer**.
3. Upload the OCMOD package.
4. Open **Extensions → Extensions** and select **Modules**.
5. Installing **ProBG Banner Mobile & Title Control** is still recommended so the DB migration runs immediately.
6. Open **Extensions → Modifications** and click **Refresh**.
7. If required, clear the Theme/SASS cache from Developer Settings.

Starting with version 1.0.1, missing DB columns are also created automatically on the first banner create/edit operation.

## Usage

### Configure banner images

Open **Design → Banners** and edit a banner.

For every language and banner row, the following fields are available:

- Title;
- Link;
- standard Image;
- Mobile Image;
- Hide Title;
- Sort Order.

### Configure dimensions

Open **Extensions → Extensions → Modules → Banner** and edit the required Banner module instance.

Set:

- Width;
- Height;
- Mobile Width;
- Mobile Height.

## Fallback logic

The extension uses the following fallback rules:

1. If a valid mobile image exists, it is used for the mobile viewport.
2. If no mobile image exists, the desktop image is resized to the mobile dimensions.
3. If an older Banner module instance has no mobile dimensions, desktop Width/Height are used.
4. If Hide Title is enabled, `banner.title` is empty while `banner.alt` retains the original title.

## File structure

```text
install.xml
CHANGELOG.md
upload/
  admin/
    controller/extension/module/probg_banner_mobile.php
    language/bg-bg/extension/module/
    language/en-gb/extension/module/
    view/template/extension/module/probg_banner_mobile.twig
```

`install.xml` contains the OCMOD operations for the standard OpenCart banner model, controller, and template files.

## Standard components modified through OCMOD

The extension virtually modifies:

```text
admin/model/design/banner.php
admin/controller/design/banner.php
admin/view/template/design/banner_form.twig
admin/controller/extension/module/banner.php
admin/view/template/extension/module/banner.twig
catalog/controller/extension/module/banner.php
catalog/view/theme/default/template/extension/module/banner.twig
```

The original files are not overwritten.

## Custom themes

The storefront OCMOD template operation targets only the default theme:

```text
catalog/view/theme/default/template/extension/module/banner.twig
```

If the active theme provides its own Banner template, OpenCart loads that file instead and the modification applied to the `default` theme will not be visible. The custom template is usually located at:

```text
catalog/view/theme/THEME-NAME/template/extension/module/banner.twig
```

The module storefront controller already provides all required data regardless of the active theme:

- `banner.image` — desktop image;
- `banner.mobile_image` — mobile image;
- `banner.title` — visible title; empty when **Hide Title** is enabled;
- `banner.alt` — original banner title used for image `alt` text;
- `banner.hide_title` — `1` when **Hide Title** is enabled.

### Manual custom-theme modification

Open:

```text
catalog/view/theme/THEME-NAME/template/extension/module/banner.twig
```

Find the markup that renders each banner image. In a standard or near-standard theme it usually looks similar to:

```twig
<div class="swiper-slide">
  {% if banner.link %}
    <a href="{{ banner.link }}">
      <img src="{{ banner.image }}" alt="{{ banner.title }}" class="img-responsive" />
    </a>
  {% else %}
    <img src="{{ banner.image }}" alt="{{ banner.title }}" class="img-responsive" />
  {% endif %}
</div>
```

Replace only the image portion with a responsive `<picture>` implementation:

```twig
<div class="swiper-slide">
  {% if banner.link %}<a href="{{ banner.link }}"{% if banner.title %} title="{{ banner.title }}"{% endif %}>{% endif %}

  <picture style="display:block">
    {% if banner.mobile_image %}
      <source media="(max-width: 767px)" srcset="{{ banner.mobile_image }}" />
    {% endif %}
    <img src="{{ banner.image }}" alt="{{ banner.alt }}" class="img-responsive" />
  </picture>

  {% if banner.link %}</a>{% endif %}
</div>
```

With this markup:

- up to `767px`, the browser uses `banner.mobile_image`;
- above `767px`, it uses `banner.image`;
- when no separate mobile image exists, the controller already provides the desktop image as fallback;
- `banner.alt` remains available even when the visible title is hidden.

### When the theme renders a visible title/caption

Some custom themes render a visible caption such as:

```twig
<h3>{{ banner.title }}</h3>
```

To support **Hide Title**, wrap it in a condition:

```twig
{% if banner.title and not banner.hide_title %}
  <h3>{{ banner.title }}</h3>
{% endif %}
```

Because the module already sends an empty `banner.title` when **Hide Title** is enabled, checking only `banner.title` is sufficient in most themes:

```twig
{% if banner.title %}
  <h3>{{ banner.title }}</h3>
{% endif %}
```

### Themes using lazy loading or custom markup

If the theme uses `data-src`, `data-srcset`, `loading="lazy"`, `img-fluid`, custom slider classes, or a JavaScript lazy loader, do not mechanically replace the entire `<div class="swiper-slide">`. Preserve the theme's markup and classes, and add only the required data logic for:

```twig
banner.mobile_image
banner.image
banner.alt
banner.hide_title
```

A minimal `<picture>` integration can look like:

```twig
<picture>
  {% if banner.mobile_image %}
    <source media="(max-width: 767px)" srcset="{{ banner.mobile_image }}" />
  {% endif %}
  <img src="{{ banner.image }}" alt="{{ banner.alt }}" />
</picture>
```

If the custom theme uses a different responsive breakpoint such as `576px`, `768px`, or `992px`, adjust `(max-width: 767px)` to match the theme's layout.

### After the manual modification

1. Save the active theme's `banner.twig` file.
2. Open **Extensions → Modifications** and click **Refresh**.
3. Clear the Theme cache from Developer Settings.
4. Clear any additional cache provided by the custom theme.
5. Test the home page on desktop and below the configured mobile breakpoint.

Important: a custom-theme update may overwrite manually edited `banner.twig` files. Recheck the template after updating the theme.

## Upgrade notes

When upgrading:

1. upload the updated OCMOD package;
2. refresh the modification cache;
3. reinstall the helper module when you want the migration to run immediately.

Starting with 1.0.1, missing `mobile_image` and `hide_title` columns are also checked and created automatically before a banner write.

Mobile-image and Hide Title data are preserved.

## Changelog and versioning

Every released version must have its own entry in [CHANGELOG.md](CHANGELOG.md).

The following categories are used:

- `feat` — new functionality or capability;
- `fix` — a bug fix or correction to existing functionality.

The same prefixes are used for commit messages, for example:

```text
feat: add configurable mobile breakpoint
fix: preserve mobile image when editing a banner
```

Versions follow Semantic Versioning:

- PATCH — fixes only, for example `1.0.0` → `1.0.1`;
- MINOR — backward-compatible new functionality, for example `1.0.0` → `1.1.0`;
- MAJOR — breaking changes, for example `1.x.x` → `2.0.0`.

## Author

**ProBG**  
https://probg.com/

## Support development

If this module is useful to you, you can support its development through Revolut:

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-Revolut-0075EB?style=for-the-badge&logo=revolut&logoColor=white)](https://revolut.me/vtotev)
