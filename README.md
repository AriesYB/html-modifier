# MCP HTML修改

## MCP工具接口说明

本项目作为MCP工具提供HTML精准修改能力(支持含vue语法的HTML)，包含以下工具函数，可通过MCP框架直接调用：

### 1. 修改HTML内容 `modify_html`

**功能**：直接接收HTML字符串和修改指令，返回修改后的HTML

**请求参数**：

```json
{
  "html": "<!DOCTYPE html><html lang=\"zh-CN\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>企业级管理后台 - 项目构建</title><link rel=\"stylesheet\" href=\"https://unpkg.com/element-ui/lib/theme-chalk/index.css\"><script src=\"https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.js\"></script><script src=\"https://unpkg.com/element-ui/lib/index.js\"></script><div class=\"container\">原始HTML内容</div></body></html>",
  "modifications": [
    {
      "description": "替换容器类名",
      "xpath": "//div[@class='container']",
      "new_html": "<section class=\"main-content\" @click=\"modifyContent\" :active>新内容</section>"
    }
  ]
}
```

**原页面**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>企业级管理后台 - 项目构建</title>
    <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
    <script src="https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.js"></script>
    <script src="https://unpkg.com/element-ui/lib/index.js"></script>
    <div class="container">原始HTML内容</div>
    </body>
</html>
```

**响应结果**：

```html

<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>企业级管理后台 - 项目构建</title>
    <link rel="stylesheet" href="https://unpkg.com/element-ui/lib/theme-chalk/index.css">
    <script src="https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.js"></script>
    <script src="https://unpkg.com/element-ui/lib/index.js"></script>
</head>
<body>
<div>
    <section class="main-content" @click="modifyContent" :active>新内容</section>
</div>
</body>
</html>

```

### 2. 存储HTML内容 `save_html`

**功能**：临时存储HTML内容并关联唯一标识key，避免大模型重复传递大型HTML字符串消耗token

**请求参数**：

```json
{
  "html": "<div>原始HTML内容</div>",
  "key": "unique_identifier"
}
```

**响应结果**：

```json
"unique_identifier"
```

### 3. 通过key修改HTML `modify_html_by_key`

**功能**：使用已存储的HTML内容（通过key引用）进行修改，适合多次修改场景

**请求参数**：

```json
{
  "key": "unique_identifier",
  "modifications": [
    {
      "description": "添加样式",
      "xpath": "//section",
      "new_html": "<section style='color:red'></section>"
    }
  ]
}
```

**响应结果**：

```json
"修改成功"
```

### 4. 导出HTML到文件 `export_html_to_file`

**功能**：将存储的HTML内容导出为本地文件，减少token消耗

**请求参数**：

```json
{
  "key": "unique_identifier",
  "path": "/output/path/result.html"
}
```

**响应结果**：

```json
true
```

## 参数详细说明

### 通用参数说明

#### modifications数组元素结构

| 参数名         | 类型     | 必选 | 说明              | 示例                                 |
|-------------|--------|----|-----------------|------------------------------------|
| description | string | 否  | 修改操作描述（调试用）     | "替换容器类名"                           |
| xpath       | string | 是  | XML路径表达式，用于定位元素 | "//div[@class='container']"        |
| new_html    | string | 是  | 替换后的HTML片段      | "<section class='main'></section>" |

### 各工具专用参数

#### save_html

| 参数名  | 类型     | 必选 | 说明            | 示例                   |
|------|--------|----|---------------|----------------------|
| html | string | 是  | 原始HTML字符串     | "<div>需要存储的内容</div>" |
| key  | string | 是  | 唯一标识，用于后续操作引用 | "page_content_123"   |

#### modify_html

| 参数名           | 类型     | 必选 | 说明            | 示例                        |
|---------------|--------|----|---------------|---------------------------|
| html          | string | 是  | 待修改的原始HTML字符串 | "<div class='old'></div>" |
| modifications | array  | 是  | 修改任务数组        | 见通用参数说明中的modifications结构  |

#### modify_html_by_key

| 参数名           | 类型     | 必选 | 说明         | 示例                       |
|---------------|--------|----|------------|--------------------------|
| key           | string | 是  | 已存储HTML的标识 | "page_content_123"       |
| modifications | array  | 是  | 修改任务数组     | 见通用参数说明中的modifications结构 |

#### export_html_to_file

| 参数名  | 类型     | 必选 | 说明         | 示例                         |
|------|--------|----|------------|----------------------------|
| key  | string | 是  | 已存储HTML的标识 | "page_content_123"         |
| path | string | 是  | 目标文件路径     | "/data/output/result.html" |

## 注意事项

1. Vue模板语法只是简单字符串替换
2. 给HTML元素id，大模型生成的XPath会更准确

## DEBUG

```bash
npx @modelcontextprotocol/inspector uvx .
```
