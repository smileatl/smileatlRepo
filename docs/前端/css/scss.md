# scss

## scss配置文件介绍

**（1）config.scss**

 `config.scss` 文件主要用于定义全局的 SASS 变量和配置项，这些变量和配置项通常用于控制整个项目的样式行为。它可以包含颜色、字体大小、间距、布局等各种样式相关的变量。

```scss
// config.scss
$primary-color: #42b983;
$font-size-base: 16px;
$line-height-base: 1.6;
$border-radius: 4px;
```

在这个文件中，你可以定义任何你希望在整个项目中使用的 SASS 变量。这些变量可以在其他 SASS 文件中被引用，以保持样式的一致性和可维护性。

**（2）palette.scss**

 `palette.scss` 文件专注于定义颜色调色板和主题颜色变量。它通常只包含与颜色相关的变量，这些变量用于控制项目的配色方案。

```scss
// palette.scss
$background-color: #ffffff;
$text-color: #333333;
$link-color: #42b983;
$button-primary-bg: #42b983;
$button-primary-color: #ffffff;
```

在这个文件中，你可以定义项目中使用的所有颜色变量。这使得你可以轻松地调整整个项目的配色方案，只需修改这个文件中的变量即可。

- **`config.scss`**：
  - 用于定义各种全局样式变量，不仅限于颜色，还可以包括字体大小、间距、边框等。
  - 适用于定义项目中所有可能需要的样式配置项。
- **`palette.scss`**：
  - 专注于定义颜色变量，用于控制项目的配色方案。
  - 适用于定义与颜色相关的所有变量。

**（3）index.scss**

自定义样式文件，可以引入config.scss和palette.scss样式文件里的变量。可以使用`!important`将其中的规则置为最高优先级。