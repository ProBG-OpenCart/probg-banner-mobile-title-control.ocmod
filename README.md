# ProBG Banner Mobile & Title Control

OCMOD разширение за OpenCart 3, което надгражда стандартната система за банери с отделно мобилно изображение, мобилни размери и контрол върху показването на заглавието.

English documentation: [README_EN.md](README_EN.md)

## Версия

Текуща версия: **1.0.3**

Историята на промените по версии се поддържа в [CHANGELOG.md](CHANGELOG.md).

## Съвместимост

Разширението е разработено за OpenCart 3 и е съобразено със стандартната структура на:

- OpenCart 3.0.2.0
- OpenCart 3.0.3.7
- OpenCart 3.0.3.8
- OpenCart 3.0.3.9

Не се променят директно core файлове. Промените се прилагат чрез OCMOD.

## Основни възможности

### Мобилно изображение за всеки банер

В **Дизайн → Банери** към всеки ред на банера се добавя отделно поле **Мобилно изображение**.

Така за един и същ банер могат да се зададат:

- desktop изображение;
- mobile изображение;
- отделни изображения за всяка езикова версия.

Ако няма избрано мобилно изображение, за mobile версията се използва desktop изображението.

### Размери за мобилното изображение

В настройките на всяка инстанция на стандартния модул **Banner** се добавят:

- **Ширина на мобилното изображение**;
- **Височина на мобилното изображение**.

Desktop размерите продължават да използват стандартните полета Width и Height на OpenCart.

При съществуващи Banner модули без въведени mobile размери се използват стандартните desktop размери като fallback.

### Скриване на заглавието

Към всеки банер в **Дизайн → Банери** се добавя отметка **Скрий заглавие**.

Когато е включена:

- заглавието не се подава като видим title към frontend темплейта;
- оригиналното заглавие се запазва като `alt` текст на изображението за accessibility и SEO.

Това позволява custom теми, които визуализират `banner.title`, да спрат показването му за конкретен банер.

### Responsive frontend

Стандартният OpenCart Banner template се променя да използва HTML `<picture>`:

- при ширина до `767px` се зарежда mobile изображението;
- при по-голяма ширина се зарежда desktop изображението.

Изборът се прави от браузъра без JavaScript device detection.

## Промени в базата данни

Разширението използва следните допълнителни колони в стандартната таблица `banner_image`:

```text
mobile_image VARCHAR(255)
hide_title TINYINT(1)
```

От версия **1.0.1** схемата се проверява автоматично преди създаване или редакция на банер. Ако една от колоните липсва, тя се създава автоматично преди записването на данните. Това предотвратява грешката `Unknown column 'mobile_image' in 'INSERT INTO'`, дори ако OCMOD модификацията е активирана преди изпълнение на install метода на helper модула.

При деинсталиране колоните не се изтриват умишлено, за да не се губят избраните mobile изображения и настройките за заглавията при повторна инсталация или обновяване.

## Инсталация

1. Изтеглете готовия `.ocmod.zip` пакет за текущата версия.
2. В администрацията на OpenCart отворете **Extensions → Installer**.
3. Качете OCMOD пакета.
4. Отворете **Extensions → Extensions** и изберете тип **Modules**.
5. Препоръчително е да инсталирате **ProBG Banner Mobile & Title Control**, за да се изпълни DB migration веднага.
6. Отворете **Extensions → Modifications** и натиснете **Refresh**.
7. При необходимост изчистете Theme/SASS cache от Developer Settings.

От версия 1.0.1 липсващите DB колони ще бъдат създадени и автоматично при първото създаване или редактиране на банер.

## Използване

### Настройване на изображенията

Отворете **Design → Banners** и редактирайте банер.

За всеки език и всеки ред вече са налични:

- Title;
- Link;
- стандартно Image;
- Mobile Image;
- Hide Title;
- Sort Order.

### Настройване на размерите

Отворете **Extensions → Extensions → Modules → Banner** и редактирайте съответната Banner инстанция.

Задайте:

- Width;
- Height;
- Mobile Width;
- Mobile Height.

## Fallback логика

Разширението използва следната логика:

1. Ако има валидно mobile изображение, то се използва за mobile viewport.
2. Ако няма mobile изображение, desktop изображението се resize-ва до mobile размерите.
3. Ако няма зададени mobile размери в стара Banner инстанция, използват се desktop Width/Height.
4. Ако Hide Title е включено, `banner.title` е празен, но `banner.alt` запазва оригиналното заглавие.

## Файлова структура

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

`install.xml` съдържа OCMOD промените за стандартните OpenCart banner model/controller/template файлове.

## Променяни стандартни компоненти чрез OCMOD

Разширението модифицира виртуално следните OpenCart файлове:

```text
admin/model/design/banner.php
admin/controller/design/banner.php
admin/view/template/design/banner_form.twig
admin/controller/extension/module/banner.php
admin/view/template/extension/module/banner.twig
catalog/controller/extension/module/banner.php
catalog/view/theme/default/template/extension/module/banner.twig
```

Оригиналните файлове не се презаписват.

## Custom теми

OCMOD промяната на storefront шаблона е насочена само към стандартната тема:

```text
catalog/view/theme/default/template/extension/module/banner.twig
```

Ако активната тема има собствен Banner template, OpenCart зарежда него и промяната по `default` темата няма да се вижда. Най-често файлът е:

```text
catalog/view/theme/ИМЕ-НА-ТЕМАТА/template/extension/module/banner.twig
```

Frontend контролерът на модула вече подава необходимите данни независимо коя тема е активна:

- `banner.image` — desktop изображение;
- `banner.mobile_image` — mobile изображение;
- `banner.title` — заглавие за визуализиране; празно е при включено **Hide Title**;
- `banner.alt` — оригиналното заглавие, използвано за `alt` текста;
- `banner.hide_title` — `1`, когато **Hide Title** е включено.

### Ръчна корекция на custom тема

Отворете:

```text
catalog/view/theme/ИМЕ-НА-ТЕМАТА/template/extension/module/banner.twig
```

Намерете HTML кода, който визуализира изображението на всеки банер. При стандартна или близка до стандартната тема той обикновено изглежда подобно на:

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

Заменете само частта за изображението с responsive `<picture>` вариант:

```twig
<div class="swiper-slide">
  {% if banner.link %}<a href="{{ banner.link }}">{% endif %}

  <picture style="display:block">
    {% if banner.mobile_image %}
      <source media="(max-width: 767px)" srcset="{{ banner.mobile_image }}" />
    {% endif %}
    <img src="{{ banner.image }}" alt="{{ banner.alt }}" class="img-responsive" />
  </picture>

  {% if banner.link %}</a>{% endif %}
</div>
```

Така:

- до `767px` браузърът използва `banner.mobile_image`;
- над `767px` използва `banner.image`;
- ако няма мобилно изображение, контролерът вече подава desktop изображението като fallback;
- `alt` остава наличен чрез `banner.alt`, дори когато заглавието е скрито.

### Ако темата показва заглавието като текст

Някои custom теми добавят видим caption, например:

```twig
<h3>{{ banner.title }}</h3>
```

За да работи **Скрий заглавие**, използвайте условие:

```twig
{% if banner.title and not banner.hide_title %}
  <h3>{{ banner.title }}</h3>
{% endif %}
```

Тъй като модулът подава празен `banner.title` при включено **Hide Title**, при повечето теми е достатъчна и проверка само за `banner.title`:

```twig
{% if banner.title %}
  <h3>{{ banner.title }}</h3>
{% endif %}
```

### Теми с lazy loading или различен HTML

Ако темата използва `data-src`, `data-srcset`, `loading="lazy"`, `img-fluid`, собствени slider класове или JavaScript lazy loader, не заменяйте механично целия `<div class="swiper-slide">`. Запазете markup-а и класовете на темата и добавете само логиката за:

```twig
banner.mobile_image
banner.image
banner.alt
banner.hide_title
```

При `<picture>` mobile source може да се добави по следния начин:

```twig
<picture>
  {% if banner.mobile_image %}
    <source media="(max-width: 767px)" srcset="{{ banner.mobile_image }}" />
  {% endif %}
  <img src="{{ banner.image }}" alt="{{ banner.alt }}" />
</picture>
```

Ако custom темата използва собствен breakpoint, например `576px`, `768px` или `992px`, можете да промените `(max-width: 767px)` според responsive логиката на темата.

### След ръчната промяна

1. Запазете `banner.twig` на активната тема.
2. Отворете **Extensions → Modifications** и натиснете **Refresh**.
3. Изчистете Theme cache от Developer Settings.
4. Ако темата има собствен cache, изчистете и него.
5. Проверете началната страница на desktop и при viewport под зададения mobile breakpoint.

Важно: при обновяване на custom тема ръчно направената промяна в нейния `banner.twig` може да бъде презаписана. След update на темата проверете отново файла.

## Обновяване

При обновяване:

1. качете новия OCMOD пакет;
2. обновете modification cache;
3. при необходимост преинсталирайте helper модула, за да се изпълни migration веднага.

От версия 1.0.1 липсващите `mobile_image` и `hide_title` се проверяват и създават автоматично преди запис на банер.

Данните за mobile изображенията и Hide Title се запазват.

## Changelog и версии

Всяка публикувана версия трябва да има отделен запис в [CHANGELOG.md](CHANGELOG.md).

Използват се следните категории:

- `feat` — нова възможност или функционалност;
- `fix` — корекция на грешка или съществуваща функционалност.

Същите префикси се използват и в commit съобщенията, например:

```text
feat: add configurable mobile breakpoint
fix: preserve mobile image when editing a banner
```

Версиите следват Semantic Versioning:

- PATCH — само корекции, например `1.0.0` → `1.0.1`;
- MINOR — нови обратно съвместими възможности, например `1.0.0` → `1.1.0`;
- MAJOR — несъвместими промени, например `1.x.x` → `2.0.0`.

## Автор

**ProBG**  
https://probg.com/

## Подкрепете разработката

Ако модулът ви е полезен, можете да подкрепите неговата разработка чрез Revolut:

[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-Revolut-0075EB?style=for-the-badge&logo=revolut&logoColor=white)](https://revolut.me/vtotev)
