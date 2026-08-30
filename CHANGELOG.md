# Changelog

All notable changes to **ProBG Banner Mobile & Title Control** are documented in this file.

The project uses the following change categories:

- `feat` — new functionality or a new capability;
- `fix` — bug fixes and corrections to existing functionality.

Every released version must have its own changelog entry. Versions follow Semantic Versioning:

- `PATCH` (`1.0.0` → `1.0.1`) for fixes only;
- `MINOR` (`1.0.0` → `1.1.0`) for backward-compatible new functionality;
- `MAJOR` (`1.x.x` → `2.0.0`) for breaking changes.

## [1.1.0] - 2026-08-30

### feat

- Added a conditional HTML `title` attribute to banner links using `banner.title`.
- The link `title` attribute is omitted automatically when **Hide Title** is enabled because `banner.title` is empty.
- Updated the custom-theme integration examples to use the same conditional link-title logic.

## [1.0.3] - 2026-08-30

### fix

- Added detailed manual integration instructions for OpenCart custom themes that override `extension/module/banner.twig`.
- Added ready-to-use responsive `<picture>` markup using `banner.mobile_image`, `banner.image`, and `banner.alt`.
- Documented manual `Hide Title` handling for custom themes that render visible banner captions.
- Added guidance for custom breakpoints, lazy-loading themes, cache refresh, and theme updates that may overwrite manual template changes.

## [1.0.1] - 2026-08-30

### fix

- Fixed `Unknown column 'mobile_image' in 'INSERT INTO'` when the OCMOD modification was active before the helper module install routine had created the database columns.
- Added a self-healing database schema check before `addBanner()` and `editBanner()` so `mobile_image` and `hide_title` are created automatically when missing.
- Removed the runtime dependency on manually running the helper module installation before editing or creating banners.

## [1.0.0] - 2026-08-15

### feat

- Added a separate mobile image field for every standard OpenCart banner image and language.
- Added configurable mobile width and mobile height to every standard Banner module instance.
- Added a `Hide Title` option for every banner image.
- Added responsive storefront output based on HTML `<picture>` and a mobile `<source>` for viewports up to `767px`.
- Added fallback to the desktop image when no mobile image is configured.
- Added fallback to desktop width and height when mobile dimensions are missing from an existing Banner module instance.
- Preserved the original banner title as image `alt` text when the visible title is hidden.
- Added installation logic for the `mobile_image` and `hide_title` fields in the standard `banner_image` table.
- Added Bulgarian and English administration language files.
- Added Bulgarian and English project documentation.
