# AstrBot AI 使用理解文档

来源: https://docs.astrbot.app (保留简介首段 + 使用/开发)

## AstrBot

来源: https://docs.astrbot.app/what-is-astrbot.html

### 什么是 AstrBot？

AstrBot 致力于成为一个开源、一站式的 Agentic 聊天机器人平台及开发框架。你可以灵活将 AstrBot 配置为理想的 AI 伴侣、高效的 智能客服，或专业的企业知识库。通过 AstrBot，你能够轻松地在各种主流消息平台上部署和开发支持大语言模型（LLM）的智能聊天机器人。

- 完善的 Agentic 能力：支持多轮工具调用、内置沙盒代码执行、网页搜索，实现高阶任务处理。
- LLM 对话引擎： 接入多种大模型，支持多模态、工具调用、原生知识库和人设定制。
- 广泛平台支持： 一键部署至 QQ、企业微信、微信公众号、飞书、Telegram、钉钉、Discord 等主流平台，提供安全与稳定保障。
- 插件与 WebUI： 深度优化插件扩展机制，以及可视化 WebUI 进行配置和管理。

## 管理面板

来源: https://docs.astrbot.app/use/webui.html

AstrBot 管理面板具有管理插件、查看日志、可视化配置、查看统计信息等功能。

![image](/source/images/webui/image-4.png)

### 管理面板的访问

当启动 AstrBot 之后，你可以通过浏览器访问 `http://localhost:6185` 来访问管理面板。

> [!TIP]
> - 如果你正在云服务器上部署 AstrBot，需要将 `localhost` 替换为你的服务器 IP 地址。

### 登录

默认用户名和密码是 `astrbot` 和 `astrbot`。

### 可视化配置

在管理面板中，你可以通过可视化配置来配置 AstrBot 的插件。点击左栏 `配置` 即可进入配置页面。

![image](/source/images/webui/image-3.png)

当修改完配置后，你需要点击右下角 `保存` 按钮才能成功保存配置。

使用右下角第一个圆形按钮可以切换至 `代码编辑配置`。在 `代码编辑配置` 中，你可以直接编辑配置文件。

编辑完后首先点击`应用此配置`，此时配置将应用到可视化配置中，然后再点击右下角`保存`按钮来保存配置。如果你不点击`应用此配置`，那么你的修改将不会生效。

![alt text](/source/images/webui/image-5.png)

### 插件

在管理面板中，你可以通过左栏的 `插件` 来查看已安装的插件，以及安装新插件。

点击插件市场标签栏，你可以浏览由 AstrBot 官方上架的插件。

![image](/source/images/webui/image-1.png)

你也可以点击右下角 + 按钮，以 URL / 文件上传的方式手动安装插件。

> 由于插件更新机制，AstrBot Team 无法完全保证插件市场中插件的安全性，请您仔细甄别。因为插件原因造成损失的，AstrBot Team 不予负责。

### 更新管理面板

在 AstrBot 启动时，会自动检查管理面板是否需要更新，如果需要，第一条日志（黄色）会进行提示。

使用 `/dashboard_update` 命令可以手动更新管理面板（管理员指令）。

管理面板文件在 data/dist 目录下。如果需要手动替换，请在 https://github.com/AstrBotDevs/AstrBot/releases/ 下载 `dist.zip` 然后解压到 data 目录下。

### 自定义 WebUI 端口

修改 data/cmd_config.json 文件内 `dashboard` 配置中的 `port`。

### 忘记密码

修改 data/cmd_config.json 文件内 `dashboard` 配置中的 `password`，将 password 整个键值对删除。

## AstrBot Star

来源: https://docs.astrbot.app/use/plugin.html

在 `3.4.0` 版本之后，AstrBot 将插件命名为 `Star`。AstrBot 是一个高度模块化的项目，通过插件可以发挥这种模块化的能力，实现各种功能。

使用 `/plugin` 可以看到所有插件。在管理面板中也可管理已经安装的插件。

如果想自己开发插件，详见 [几行代码实现一个插件](/dev/star/plugin)。

## 内置指令

来源: https://docs.astrbot.app/use/command.html

AstrBot 具有很多内置指令，它们通过插件的形式被导入。位于 `packages/astrbot` 目录下。

使用 `/help` 可以查看所有内置指令。

## 函数调用（Function-calling）

来源: https://docs.astrbot.app/use/function-calling.html

### 简介

函数调用旨在提供大模型**调用外部工具的能力**，以此实现 Agentic 的一些功能。

比如，问大模型：帮我搜索一下关于“猫”的信息，大模型会调用用于搜索的外部工具，比如搜索引擎，然后返回搜索结果。

目前，支持的模型包括但不限于

- gpt-4 系列（效果最好）
- gemini 2.0 系列（不包含 thinking 类的模型）（效果最好）
- deepseek v3(deepseek-chat)
- llama3 系列（本地部署参数量较小时效果不好）

等等。

不支持的模型比较常见的有 deepseek-r1, gemini 2.0 的 thinking 类模型等。

在 AstrBot 中，默认提供了网页搜索、待办提醒、代码执行器这些工具。很多插件，如:

- astrbot_plugin_cloudmusic
- astrbot_plugin_bilibili
- ...

等在提供传统的指令调用的基础上，也提供了函数调用的功能。

相关指令:

- `/tool ls` 查看当前具有的工具列表
- `/tool on` 开启某个工具
- `/tool off` 关闭某个工具
- `/tool off_all` 关闭所有工具

某些模型可能不支持函数调用，会返回诸如 `tool call is not supported`, `function calling is not supported`, `tool use is not supported` 等错误。在大多数情况下，AstrBot 能够检测到这种错误并自动帮您去除函数调用工具。如果你发现某个模型不支持函数调用，也可使用 `/tool off_all` 命令关闭所有工具，然后再次尝试。或者更换为支持函数调用的模型。


下面是一些常见的工具调用 Demo：

![image](/source/images/function-calling/image.png)

![image](/source/images/function-calling/image-1.png)


### MCP

请前往此文档 [AstrBot - MCP](/use/mcp) 查看。

## MCP

来源: https://docs.astrbot.app/use/mcp.html

MCP(Model Context Protocol，模型上下文协议) 是一种新的开放标准协议，用来在大模型和数据源之间建立安全双向的链接。简单来说，它将函数工具单独抽离出来作为一个独立的服务，AstrBot 通过 MCP 协议远程调用函数工具，函数工具返回结果给 AstrBot。

![image](/source/images/function-calling/image3.png)

AstrBot v3.5.0 支持 MCP 协议，可以添加多个 MCP 服务器、使用 MCP 服务器的函数工具。

![image](/source/images/function-calling/image2.png)

### 初始状态配置

MCP 服务器一般使用 `uv` 或者 `npm` 来启动，因此您需要安装这两个工具。

对于 `uv`，您可以直接通过 pip 来安装。可在 AstrBot WebUI 快捷安装：

![image](image.png)

输入 `uv` 即可。

如果您使用 Docker 部署 AstrBot，也可以执行以下指令快捷安装。

```bash
docker exec astrbot python -m pip install uv
```

如果您通过源码部署 AstrBot，请在创建的虚拟环境内安装。

对于 `npm`，您需要安装 `node`。

如果您通过源码/一键安装部署 AstrBot，请参考 [Download Node.js](https://nodejs.org/en/download) 下载到您的本机。

如果您使用 Docker 部署 AstrBot，您需要在容器中安装 `node`（后期 AstrBot Docker 镜像将自带 `node`），请参考执行以下指令：

```bash
sudo docker exec -it astrbot /bin/bash
apt update && apt install curl -y
export NVM_NODEJS_ORG_MIRROR=http://nodejs.org/dist
# Download and install nvm:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash
\. "$HOME/.nvm/nvm.sh"
nvm install 22
# Verify version:
node -v
nvm current
npm -v
npx -v
```

安装好 `node` 之后，需要重启 `AstrBot` 以应用新的环境变量。

### 安装 MCP 服务器

如果您使用 Docker 部署 AstrBot，请将 MCP 服务器安装在 data 目录下。

#### 一个例子

我想安装一个查询 Arxiv 上论文的 MCP 服务器，发现了这个 Repo: [arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server)，参考它的 README，

我们抽取出需要的信息：

```json
{
    "command": "uv",
    "args": [
        "tool",
        "run",
        "arxiv-mcp-server",
        "--storage-path", "data/arxiv"
    ]
}
```

在 AstrBot WebUI 中设置:

![image](image-2.png)

即可。

参考链接：

1. 在这里了解如何使用 MCP: [Model Context Protocol](https://modelcontextprotocol.io/introduction)
2. 在这里获取常用的 MCP 服务器: [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers/blob/main/README-zh.md#what-is-mcp), [Model Context Protocol servers](https://github.com/modelcontextprotocol/servers), [MCP.so](https://mcp.so)

## 网页搜索

来源: https://docs.astrbot.app/use/websearch.html

网页搜索功能旨在提供大模型调用 Google，Bing，搜狗等搜索引擎以获取世界最近信息的能力，一定程度上能够提高大模型的回复准确度，减少幻觉。

AstrBot 内置的网页搜索功能依赖大模型提供 `函数调用` 能力。如果你不了解函数调用，请参考：[函数调用](/use/websearch)。

在使用支持函数调用的大模型且开启了网页搜索功能的情况下，您可以试着说：

- `帮我搜索一下 xxx`
- `帮我总结一下这个链接：https://soulter.top`
- `查一下 xxx`
- `最近 xxxx`

等等带有搜索意味的提示让大模型触发调用搜索工具。

v4.0.0 版本以后，AstrBot 支持 2 种网页搜索源接入方式：`默认` 和 `Tavily`。前者使用 AstrBot 内置的网页搜索请求器请求 Google、Bing、搜狗搜索引擎。在能够使用 Google 的网络环境下表现最佳。推荐使用 Tavily。

![image](/source/images/websearch/image.png)

进入 `配置`，下拉找到网页搜索，您可选择 `default`（默认） 或 `Tavily`。

#### default

如果您的设备在国内并且有代理，可以开启代理并在 `管理面板-其他配置-HTTP代理` 填入 HTTP 代理地址以应用代理。

#### Tavily

前往 [Tavily](https://app.tavily.com/home) 得到 API Key，然后填写在相应的配置项。

## AstrBot 知识库

来源: https://docs.astrbot.app/use/knowledge-base.html

> [!TIP]
> 需要 AstrBot 版本 >= 4.5.0。
>
> 我们在 4.5.0 版本中重新设计了全新的知识库系统，AstrBot 将原生支持知识库功能。下文介绍的是新版知识库的使用方法。如果您使用的是之前的版本，请参考[旧版知识库使用文档](https://docs.astrbot.app/zh/use/knowledge-base-old), 我们建议您升级到最新版以获得更好的体验。

![知识库预览](image-3.png)

### 配置嵌入模型

打开服务提供商页面，点击新增服务提供商，选择 Embedding。

目前 AstrBot 支持兼容 OpenAI API 和 Gemini API 的嵌入向量服务。

点击上面的提供商卡片进入配置页面，填写配置。

配置完成后，点击保存。

### 配置重排序模型（可选）

重排序模型可以一定程度上提高最终召回结果的精度。

和嵌入模型的配置类似，打开服务提供商页面，点击新增服务提供商，选择重排序。有关重排序模型的更多信息请参考网络。

### 创建知识库

AstrBot 支持多知识库管理。在聊天时，您可以**自由指定知识库**。

进入知识库页面，点击创建知识库，如下图所示：

![image](/source/images/knowledge-base/image.png)

填写相关信息。在嵌入模型下拉菜单中您将看到刚刚创建好的嵌入模型和重排序模型（重排序模型可选）。

> [!TIP]
> 一旦选择了一个知识库的嵌入模型，请不要再修改该提供商的**模型**或者**向量维度信息**，否则将**严重影响**该知识库的召回率甚至**报错**。

### 上传文件

创建好知识库之后，可以为知识库上传文档。支持同时上传最多 10 个文件，单个文件大小不超过 128 MB。

![上传文件](image-4.png)

### 使用知识库

在配置文件中，可以为不同的配置文件指定不同的知识库。

### 附录 2：高性价比的嵌入模型申请

#### ModelStack

1. 打开 [ModelStack 官网](https://modelstack.app/)，并注册账户，新用户赠送 `2` 元人民币。
2. 进入 [模型广场](https://modelstack.app/pricing)，选择 `嵌入模型`，选择自己想要使用的模型，例如 `bge-m3`。
3. 点击上方控制台，令牌管理，添加令牌，然后复制生成的 API Key。
4. 填写 AstrBot OpenAI Embedding 模型提供商配置：
   1. API Key 为刚刚申请的 ModelStack 的 API Key
   2. API Base URL 填写 `https://modelstack.app/v1`
   3. model 填写你选择的模型名称，此例子中为 `bge-m3`。
   4. 点击「保存」按钮，完成创建。

## 自定义规则

来源: https://docs.astrbot.app/use/custom-rules.html

> [!NOTE]
> 下文的「消息会话来源」指的是 UMO。一个 UMO 唯一指定了一个消息平台下的具体的某个会话。

在 v4.7.0 版本之后，我们重构了 AstrBot 原来的「会话管理」功能为「自定义规则」功能。以减少和配置文件的冲突。

你可以把自定义规则理解为对指定消息来源更加灵活的自定义强制处理规则，其优先级高于配置文件。

例如，原本一个消息平台使用配置文件 “default”，这个消息平台下的所有会话都按照配置文件中的规则进行处理。如果你希望对某个会话来源 A 进行特殊处理，在原来，你需要单独创建一个配置文件，然后将 A 绑定到这个配置文件中。而现在，你只需要在 WebUI 的自定义规则页中创建一个自定义规则，然后选择消息来源 A 即可。你可以定义如下规则：

1. 是否启用该消息会话来源的消息处理。如果不启用，其效果相当于将该消息会话来源拉入黑名单。
2. 是否对该消息会话来源的消息启用 LLM。如果不启用，则不会使用 AI 能力。
3. 是否对该消息会话来源的消息启用 TTS。如果不启用，则不会使用 TTS 能力。
4. 对该消息会话来源配置特定的聊天模型、语音识别模型（STT）、语音合成模型（TTS）。
5. 对该消息会话来源配置特定的人格。

## Agent 执行器

来源: https://docs.astrbot.app/use/agent-runner.html

Agent 执行器是 AstrBot 中用于执行 Agent 的组件。

在 v4.7.0 版本之后，我们将 Dify、Coze、阿里云百炼应用这三个提供商迁移到了 Agent 执行器层面，减少了与 AstrBot 目前功能的一些冲突。请放心，如果您从旧版本升级到 v4.7.0 版本，您无需进行任何操作，AstrBot 会自动为您迁移。

AstrBot 目前内置了四种 Agent 执行器：

- AstrBot 内置 Agent 执行器
- Dify Agent 执行器
- Coze Agent 执行器
- 阿里云百炼应用 Agent 执行器

默认情况下，AstrBot 内置 Agent 执行器为默认执行器。

### 为什么需要抽象出 Agent 执行器

在早期版本中，Dify、Coze、阿里云百炼应用这类「自带 Agent 能力」的平台，是作为普通 Chat Provider 集成进 AstrBot 的。实践下来会发现，它们和传统「只负责补全文本」的 Chat Provider 有本质差异，强行放在同一层会带来很多设计和使用上的冲突。因此，从 v4.7.0 起，我们将它们抽象为独立的 Agent 执行器（Agent Runner）。

从架构上看，可以理解为：

- Chat Provider 负责「说话」；
- Agent 执行器负责「思考 + 做事」。

Agent 执行器会调用 Chat Provider 的接口，并根据 Chat Provider 的回复，进行多轮「感知 → 规划 → 执行动作 → 观察结果 → 再规划」的循环。

Chat Provider 本质上是一个 `单轮补全接口`，输入 prompt + 历史对话 + 工具列表，输出模型回复（文本、工具调用指令等）。

而 Agent Runner 通常是一个 `循环（Loop）`，接收用户意图、上下文与环境状态，基于策略 / 模型做出规划（Plan），选择并调用工具（Act），从环境中读取结果（Observe），再次理解结果、更新内部状态，决定下一步动作，重复上述过程，直到任务完成或超时。

![image](/source/images/use/agent-runner/agent-arch.svg)

Dify、Coze、百炼应用等 LLMOpes 平台已经内置了这个循环，如果把它们当成普通 Chat Provider，会和 AstrBot 的内置 Agent 执行器功能冲突。

### 使用

默认情况下，AstrBot 内置 Agent 执行器为默认执行器。使用默认执行器已经可以满足大部分需求，并且可以使用 AstrBot 的 MCP、知识库、网页搜索等功能。

如果你需要使用 Dify、Coze、百炼应用等 LLMOpes 平台的能力，可以创建一个 Agent 执行器，并选择相应的提供商。

### 创建 Agent 执行器

![image](/source/images/use/agent-runner/image-1.png)

在 WebUI 中，点击「模型提供商」->「新增提供商」，选择「Agent 执行器」，选择你想接入的 LLMOpes 平台，填写相关信息即可。

### 更换默认 Agent 执行器

![image](/source/images/use/agent-runner/image.png)

在 WebUI 中，点击「配置」->「Agent 执行方式」，将执行器类型更换为你刚刚创建的 Agent 执行器类型，然后选择 `XX Agent 执行器提供商 ID` 为你刚刚创建的 Agent 执行器提供商的 ID，点击保存即可。

## 统一 Webhook 模式

来源: https://docs.astrbot.app/use/unified-webhook.html

在 v4.8.0 版本开始，AstrBot 支持统一 Webhook 模式 (unified_webhook_mode)。开启该模式后，所有支持该模式的平台适配器都将使用同一个 Webhook 回调接口，从而简化了反向代理和域名配置，不再需要给每一个机器人适配器单独配置端口、域名和反向代理。

支持统一 Webhook 模式的平台适配器包括：

- Slack Webhook 模式
- 微信公众平台
- 企业微信客服机器人
- 企业微信智能机器人
- 微信客服机器人
- QQ 官方机器人 Webhook 模式
- ...

### 如何使用统一 Webhook 模式

1. 拥有一个域名（如 example.com）和公网 IP 服务器
2. 配置 DNS 解析（如 astrbot.example.com）
3. 配置反向代理，将域名的 80 或 443 端口请求转发到 AstrBot 的 WebUI 端口（默认为 6185）
4. 前往 AstrBot `配置文件` 页，点击 `系统`，将 `对外可达的回调接口地址` 为配置的 URL 地址。（如 https://astrbot.example.com），点击保存，等待重启。


在之后配置各个平台适配器时，选择开启 `统一 Webhook 模式 (unified_webhook_mode)`。

> [!TIP]
> 如果您正在尝试更新 v4.8.0 之前配置的机器人适配器，你可能无法看到 `统一 Webhook 模式 (unified_webhook_mode)` 选项。请重新创建一个新的适配器实例，即可看到该选项。

![unified_webhook](/source/images/use/unified-webhook-config.png)

开启该模式后，AstrBot 会为你生成一个唯一的 Webhook 回调链接，你只需要将该链接填写到各个平台的回调地址处即可。

![unified_webhook](/source/images/use/unified-webhook.png)

## 基于 Docker 的代码执行器

来源: https://docs.astrbot.app/use/code-interpreter.html

在 `v3.4.2` 版本及之后，AstrBot 支持代码执行器以强化 LLM 的能力，并实现一些自动化的操作。

> [!TIP]
> 此功能目前处于实验阶段，可能会有一些问题。如果您遇到了问题，请在 [GitHub](https://github.com/AstrBotDevs/AstrBot/issues) 上提交 issue。欢迎加群讨论：[322154837](https://qm.qq.com/cgi-bin/qm/qr?k=EYGsuUTfe00_iOu9JTXS7_TEpMkXOvwv&jump_from=webapi&authKey=uUEMKCROfsseS+8IzqPjzV3y1tzy4AkykwTib2jNkOFdzezF9s9XknqnIaf3CDft)。

如果您要使用此功能，请确保您的机器安装了 `Docker`。因为此功能需要启动专用的 Docker 沙箱环境以执行代码，以防止 LLM 生成恶意代码对您的机器造成损害。


### Linux Docker 启动 AstrBot

如果您使用 Docker 部署了 AstrBot，需要多做一些工作。

1. 您需要在启动 Docker 容器时，请将 `/var/run/docker.sock` 挂载到容器内部。这样 AstrBot 才能够启动沙箱容器。

```bash
sudo docker run -itd -p 6180-6200:6180-6200 -p 11451:11451 -v $PWD/data:/AstrBot/data -v /var/run/docker.sock:/var/run/docker.sock --name astrbot soulter/astrbot:latest
```

2. 在聊天时使用 `/pi absdir <绝对路径地址>` 设置您宿主机上 AstrBot 的 data 目录的所在目录的绝对路径。

例子：

![image](/source/images/code-interpreter/image-4.png)

### Linux 手动源码 启动 AstrBot

**如果你的 Docker 指令需要 sudo 权限来执行**，那么你需要在启动 AstrBot 时，使用 `sudo` 来启动，否则代码执行器会因为权限不足而无法调用 Docker。

```bash
sudo —E python3 main.py
```

### 使用

本功能使用的镜像是 `soulter/astrbot-code-interpreter-sandbox`，您可以在 [Docker Hub](https://hub.docker.com/r/soulter/astrbot-code-interpreter-sandbox) 上查看镜像的详细信息。

镜像中提供了常用的 Python 库：

- Pillow
- requests
- numpy
- matplotlib
- scipy
- scikit-learn
- beautifulsoup4
- pandas
- opencv-python
- python-docx
- python-pptx
- pymupdf
- mplfonts

基本上能够实现的任务：

- 图片编辑
- 网页抓取等
- 数据分析、简单的机器学习
- 文档处理，如读写 Word、PPT、PDF 等
- 数学计算，如画图、求解方程等

由于中国大陆无法访问 docker hub，因此如果您的环境在中国大陆，请使用 `/pi mirror` 来查看/设置镜像源。比如，截至本文档编写时，您可以使用 `cjie.eu.org` 作为镜像源。即设置 `/pi mirror cjie.eu.org`。

在第一次触发代码执行器时，AstrBot 会自动拉取镜像，这可能需要一些时间。请耐心等待。

镜像可能会不定时间更新以提供更多的功能，因此请定期查看镜像的更新。如果需要更新镜像，可以使用 `/pi repull` 命令重新拉取镜像。

> [!TIP]
> 如果一开始没有正常启动此功能，在启动成功之后，需要执行 `/tool on python_interpreter` 来开启此功能。
> 您可以通过 `/tool ls` 查看所有的工具以及它们的启用状态。

![image](/source/images/code-interpreter/image-3.png)

### 图片和文件的输入

代码执行器除了能够识别和处理图片、文字任务，还能够识别您发送的文件，并且能够发送文件。

v3.4.34 后，使用 `/pi file` 指令开始上传文件。上传文件后，您可以使用 `/pi list` 查看您上传的文件，使用 `/pi clean` 清空您上传的文件。

上传的文件将会用于代码执行器的输入。

比如您希望对一张图片添加圆角，您可以使用 `/pi file` 上传图片，然后再提问：`请运行代码，对这张图片添加圆角`。

### Demo

![image](/source/images/code-interpreter/a3cd3a0e-aca5-41b2-aa52-66b568bd955b.png)

![alt text](/source/images/code-interpreter/image.png)

![image](/source/images/code-interpreter/image-1.png)

![image](/source/images/code-interpreter/image-2.png)

## AstrBot 插件开发指南 🌠

来源: https://docs.astrbot.app/dev/star/plugin-new.html

欢迎来到 AstrBot 插件开发指南！本章节将引导您如何开发 AstrBot 插件。在我们开始之前，希望你能具备以下基础知识：

1. 有一定的 Python 编程经验。
2. 有一定的 Git、GitHub 使用经验。

欢迎加入我们的开发者专用 QQ 群: `975206796`。

### 环境准备

#### 获取插件模板

1. 打开 AstrBot 插件模板: [helloworld](https://github.com/Soulter/helloworld)
2. 点击右上角的 `Use this template`
3. 然后点击 `Create new repository`。
4. 在 `Repository name` 处填写您的插件名。插件名格式:
   - 推荐以 `astrbot_plugin_` 开头；
   - 不能包含空格；
   - 保持全部字母小写；
   - 尽量简短。
5. 点击右下角的 `Create repository`。

#### 克隆项目到本地

克隆 AstrBot 项目本体和刚刚创建的插件仓库到本地。

```bash
git clone https://github.com/AstrBotDevs/AstrBot
mkdir -p AstrBot/data/plugins
cd AstrBot/data/plugins
git clone 插件仓库地址
```

然后，使用 `VSCode` 打开 `AstrBot` 项目。找到 `data/plugins/<你的插件名字>` 目录。

更新 `metadata.yaml` 文件，填写插件的元数据信息。

> [!WARNING]
> 请务必修改此文件，AstrBot 识别插件元数据依赖于 `metadata.yaml` 文件。

#### 设置插件 Logo（可选）

可以在插件目录下添加 `logo.png` 文件作为插件的 Logo。请保持长宽比为 1:1，推荐尺寸为 256x256。

![插件 logo 示例](/source/images/plugin/plugin_logo.png)

#### 插件展示名（可选）

可以修改(或添加) `metadata.yaml` 文件中的 `display_name` 字段，作为插件在插件市场等场景中的展示名，以方便用户阅读。

#### 调试插件

AstrBot 采用在运行时注入插件的机制。因此，在调试插件时，需要启动 AstrBot 本体。

您可以使用 AstrBot 的热重载功能简化开发流程。

插件的代码修改后，可以在 AstrBot WebUI 的插件管理处找到自己的插件，点击右上角 `...` 按钮，选择 `重载插件`。

#### 插件依赖管理

目前 AstrBot 对插件的依赖管理使用 `pip` 自带的 `requirements.txt` 文件。如果你的插件需要依赖第三方库，请务必在插件目录下创建 `requirements.txt` 文件并写入所使用的依赖库，以防止用户在安装你的插件时出现依赖未找到(Module Not Found)的问题。

> `requirements.txt` 的完整格式可以参考 [pip 官方文档](https://pip.pypa.io/en/stable/reference/requirements-file-format/)。

### 开发原则

感谢您为 AstrBot 生态做出贡献，开发插件请遵守以下原则，这也是良好的编程习惯。

- 功能需经过测试。
- 需包含良好的注释。
- 持久化数据请存储于 `data` 目录下，而非插件自身目录，防止更新/重装插件时数据被覆盖。
- 良好的错误处理机制，不要让插件因一个错误而崩溃。
- 在进行提交前，请使用 [ruff](https://docs.astral.sh/ruff/) 工具格式化您的代码。
- 不要使用 `requests` 库来进行网络请求，可以使用 `aiohttp`, `httpx` 等异步网络请求库。
- 如果是对某个插件进行功能扩增，请优先给那个插件提交 PR 而不是单独再写一个插件（除非原插件作者已经停止维护）。

## 最小实例

来源: https://docs.astrbot.app/dev/star/guides/simple.html

插件模版中的 `main.py` 是一个最小的插件实例。

```python
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger # 使用 astrbot 提供的 logger 接口

@register("helloworld", "author", "一个简单的 Hello World 插件", "1.0.0", "repo url")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        '''这是一个 hello world 指令''' # 这是 handler 的描述，将会被解析方便用户了解插件内容。非常建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 获取消息的纯文本内容
        logger.info("触发hello world指令!")
        yield event.plain_result(f"Hello, {user_name}!") # 发送一条纯文本消息

    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''
```

解释如下：

- 插件需要继承 `Star` 类。
- `Context` 类用于插件与 AstrBot Core 交互，可以由此调用 AstrBot Core 提供的各种 API。
- 具体的处理函数 `Handler` 在插件类中定义，如这里的 `helloworld` 函数。
- `AstrMessageEvent` 是 AstrBot 的消息事件对象，存储了消息发送者、消息内容等信息。
- `AstrBotMessage` 是 AstrBot 的消息对象，存储了消息平台下发的消息的具体内容。可以通过 `event.message_obj` 获取。

> [!TIP]
>
> `Handler` 一定需要在插件类中注册，前两个参数必须为 `self` 和 `event`。如果文件行数过长，可以将服务写在外部，然后在 `Handler` 中调用。
>
> 插件类所在的文件名需要命名为 `main.py`。

所有的处理函数都需写在插件类中。为了精简内容，在之后的章节中，我们可能会忽略插件类的定义。

## 处理消息事件

来源: https://docs.astrbot.app/dev/star/guides/listen-message-event.html

事件监听器可以收到平台下发的消息内容，可以实现指令、指令组、事件监听等功能。

事件监听器的注册器在 `astrbot.api.event.filter` 下，需要先导入。请务必导入，否则会和 python 的高阶函数 filter 冲突。

```py
from astrbot.api.event import filter, AstrMessageEvent
```

### 消息与事件

AstrBot 接收消息平台下发的消息，并将其封装为 `AstrMessageEvent` 对象，传递给插件进行处理。

![message-event](message-event.svg)

#### 消息事件

`AstrMessageEvent` 是 AstrBot 的消息事件对象，其中存储了消息发送者、消息内容等信息。

#### 消息对象

`AstrBotMessage` 是 AstrBot 的消息对象，其中存储了消息平台下发的消息具体内容，`AstrMessageEvent` 对象中包含一个 `message_obj` 属性用于获取该消息对象。

```py{11}
class AstrBotMessage:
    '''AstrBot 的消息对象'''
    type: MessageType  # 消息类型
    self_id: str  # 机器人的识别id
    session_id: str  # 会话id。取决于 unique_session 的设置。
    message_id: str  # 消息id
    group_id: str = "" # 群组id，如果为私聊，则为空
    sender: MessageMember  # 发送者
    message: List[BaseMessageComponent]  # 消息链。比如 [Plain("Hello"), At(qq=123456)]
    message_str: str  # 最直观的纯文本消息字符串，将消息链中的 Plain 消息（文本消息）连接起来
    raw_message: object
    timestamp: int  # 消息时间戳
```

其中，`raw_message` 是消息平台适配器的**原始消息对象**。

#### 消息链

![message-chain](message-chain.svg)

`消息链`描述一个消息的结构，是一个有序列表，列表中每一个元素称为`消息段`。

常见的消息段类型有：

- `Plain`：文本消息段
- `At`：提及消息段
- `Image`：图片消息段
- `Record`：语音消息段
- `Video`：视频消息段
- `File`：文件消息段

大多数消息平台都支持上面的消息段类型。

此外，OneBot v11 平台（QQ 个人号等）还支持以下较为常见的消息段类型：

- `Face`：表情消息段
- `Node`：合并转发消息中的一个节点
- `Nodes`：合并转发消息中的多个节点
- `Poke`：戳一戳消息段

在 AstrBot 中，消息链表示为 `List[BaseMessageComponent]` 类型的列表。

### 指令

![message-event-simple-command](message-event-simple-command.svg)

```python
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

@register("helloworld", "Soulter", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("helloworld") # from astrbot.api.event.filter import command
    async def helloworld(self, event: AstrMessageEvent):
        '''这是 hello world 指令'''
        user_name = event.get_sender_name()
        message_str = event.message_str # 获取消息的纯文本内容
        yield event.plain_result(f"Hello, {user_name}!")
```

> [!TIP]
> 指令不能带空格，否则 AstrBot 会将其解析到第二个参数。可以使用下面的指令组功能，或者也使用监听器自己解析消息内容。

### 带参指令

![command-with-param](command-with-param.svg)

AstrBot 会自动帮你解析指令的参数。

```python
@filter.command("add")
def add(self, event: AstrMessageEvent, a: int, b: int):
    # /add 1 2 -> 结果是: 3
    yield event.plain_result(f"Wow! The anwser is {a + b}!")
```

### 指令组

指令组可以帮助你组织指令。

```python
@filter.command_group("math")
def math(self):
    pass

@math.command("add")
async def add(self, event: AstrMessageEvent, a: int, b: int):
    # /math add 1 2 -> 结果是: 3
    yield event.plain_result(f"结果是: {a + b}")

@math.command("sub")
async def sub(self, event: AstrMessageEvent, a: int, b: int):
    # /math sub 1 2 -> 结果是: -1
    yield event.plain_result(f"结果是: {a - b}")
```

指令组函数内不需要实现任何函数，请直接 `pass` 或者添加函数内注释。指令组的子指令使用 `指令组名.command` 来注册。

当用户没有输入子指令时，会报错并，并渲染出该指令组的树形结构。

![image](/source/images/plugin/image-1.png)

![image](/source/images/plugin/898a169ae7ed0478f41c0a7d14cb4d64.png)

![image](/source/images/plugin/image-2.png)

理论上，指令组可以无限嵌套！

```py
'''
math
├── calc
│   ├── add (a(int),b(int),)
│   ├── sub (a(int),b(int),)
│   ├── help (无参数指令)
'''

@filter.command_group("math")
def math():
    pass

@math.group("calc") # 请注意，这里是 group，而不是 command_group
def calc():
    pass

@calc.command("add")
async def add(self, event: AstrMessageEvent, a: int, b: int):
    yield event.plain_result(f"结果是: {a + b}")

@calc.command("sub")
async def sub(self, event: AstrMessageEvent, a: int, b: int):
    yield event.plain_result(f"结果是: {a - b}")

@calc.command("help")
def calc_help(self, event: AstrMessageEvent):
    # /math calc help
    yield event.plain_result("这是一个计算器插件，拥有 add, sub 指令。")
```

### 指令别名

> v3.4.28 后

可以为指令或指令组添加不同的别名：

```python
@filter.command("help", alias={'帮助', 'helpme'})
def help(self, event: AstrMessageEvent):
    yield event.plain_result("这是一个计算器插件，拥有 add, sub 指令。")
```

#### 事件类型过滤

##### 接收所有

这将接收所有的事件。

```python
@filter.event_message_type(filter.EventMessageType.ALL)
async def on_all_message(self, event: AstrMessageEvent):
    yield event.plain_result("收到了一条消息。")
```

##### 群聊和私聊

```python
@filter.event_message_type(filter.EventMessageType.PRIVATE_MESSAGE)
async def on_private_message(self, event: AstrMessageEvent):
    message_str = event.message_str # 获取消息的纯文本内容
    yield event.plain_result("收到了一条私聊消息。")
```

`EventMessageType` 是一个 `Enum` 类型，包含了所有的事件类型。当前的事件类型有 `PRIVATE_MESSAGE` 和 `GROUP_MESSAGE`。

##### 消息平台

```python
@filter.platform_adapter_type(filter.PlatformAdapterType.AIOCQHTTP | filter.PlatformAdapterType.QQOFFICIAL)
async def on_aiocqhttp(self, event: AstrMessageEvent):
    '''只接收 AIOCQHTTP 和 QQOFFICIAL 的消息'''
    yield event.plain_result("收到了一条信息")
```

当前版本下，`PlatformAdapterType` 有 `AIOCQHTTP`, `QQOFFICIAL`, `GEWECHAT`, `ALL`。

##### 管理员指令

```python
@filter.permission_type(filter.PermissionType.ADMIN)
@filter.command("test")
async def test(self, event: AstrMessageEvent):
    pass
```

仅管理员才能使用 `test` 指令。

#### 多个过滤器

支持同时使用多个过滤器，只需要在函数上添加多个装饰器即可。过滤器使用 `AND` 逻辑。也就是说，只有所有的过滤器都通过了，才会执行函数。

```python
@filter.command("helloworld")
@filter.event_message_type(filter.EventMessageType.PRIVATE_MESSAGE)
async def helloworld(self, event: AstrMessageEvent):
    yield event.plain_result("你好！")
```

#### 事件钩子

> [!TIP]
> 事件钩子不支持与上面的 @filter.command, @filter.command_group, @filter.event_message_type, @filter.platform_adapter_type, @filter.permission_type 一起使用。

##### Bot 初始化完成时

> v3.4.34 后

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.on_astrbot_loaded()
async def on_astrbot_loaded(self):
    print("AstrBot 初始化完成")

```

##### LLM 请求时

在 AstrBot 默认的执行流程中，在调用 LLM 前，会触发 `on_llm_request` 钩子。

可以获取到 `ProviderRequest` 对象，可以对其进行修改。

ProviderRequest 对象包含了 LLM 请求的所有信息，包括请求的文本、系统提示等。

```python
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.provider import ProviderRequest

@filter.on_llm_request()
async def my_custom_hook_1(self, event: AstrMessageEvent, req: ProviderRequest): # 请注意有三个参数
    print(req) # 打印请求的文本
    req.system_prompt += "自定义 system_prompt"

```

> 这里不能使用 yield 来发送消息。如需发送，请直接使用 `event.send()` 方法。

##### LLM 请求完成时

在 LLM 请求完成后，会触发 `on_llm_response` 钩子。

可以获取到 `ProviderResponse` 对象，可以对其进行修改。

```python
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.provider import LLMResponse

@filter.on_llm_response()
async def on_llm_resp(self, event: AstrMessageEvent, resp: LLMResponse): # 请注意有三个参数
    print(resp)
```

> 这里不能使用 yield 来发送消息。如需发送，请直接使用 `event.send()` 方法。

##### 发送消息前

在发送消息前，会触发 `on_decorating_result` 钩子。

可以在这里实现一些消息的装饰，比如转语音、转图片、加前缀等等

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.on_decorating_result()
async def on_decorating_result(self, event: AstrMessageEvent):
    result = event.get_result()
    chain = result.chain
    print(chain) # 打印消息链
    chain.append(Plain("!")) # 在消息链的最后添加一个感叹号
```

> 这里不能使用 yield 来发送消息。这个钩子只是用来装饰 event.get_result().chain 的。如需发送，请直接使用 `event.send()` 方法。

##### 发送消息后

在发送消息给消息平台后，会触发 `after_message_sent` 钩子。

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.after_message_sent()
async def after_message_sent(self, event: AstrMessageEvent):
    pass
```

> 这里不能使用 yield 来发送消息。如需发送，请直接使用 `event.send()` 方法。

#### 优先级

指令、事件监听器、事件钩子可以设置优先级，先于其他指令、监听器、钩子执行。默认优先级是 `0`。

```python
@filter.command("helloworld", priority=1)
async def helloworld(self, event: AstrMessageEvent):
    yield event.plain_result("Hello!")
```

### 控制事件传播

```python{6}
@filter.command("check_ok")
async def check_ok(self, event: AstrMessageEvent):
    ok = self.check() # 自己的逻辑
    if not ok:
        yield event.plain_result("检查失败")
        event.stop_event() # 停止事件传播
```

当事件停止传播，后续所有步骤将不会被执行。

假设有一个插件 A，A 终止事件传播之后所有后续操作都不会执行，比如执行其它插件的 handler、请求 LLM。

## 消息的发送

来源: https://docs.astrbot.app/dev/star/guides/send-message.html

### 被动消息

被动消息指的是机器人被动回复消息。

```python
@filter.command("helloworld")
async def helloworld(self, event: AstrMessageEvent):
    yield event.plain_result("Hello!")
    yield event.plain_result("你好！")

    yield event.image_result("path/to/image.jpg") # 发送图片
    yield event.image_result("https://example.com/image.jpg") # 发送 URL 图片，务必以 http 或 https 开头
```

### 主动消息

主动消息指的是机器人主动推送消息。某些平台可能不支持主动消息发送。

如果是一些定时任务或者不想立即发送消息，可以使用 `event.unified_msg_origin` 得到一个字符串并将其存储，然后在想发送消息的时候使用 `self.context.send_message(unified_msg_origin, chains)` 来发送消息。

```python
from astrbot.api.event import MessageChain

@filter.command("helloworld")
async def helloworld(self, event: AstrMessageEvent):
    umo = event.unified_msg_origin
    message_chain = MessageChain().message("Hello!").file_image("path/to/image.jpg")
    await self.context.send_message(event.unified_msg_origin, message_chain)
```

通过这个特性，你可以将 unified_msg_origin 存储起来，然后在需要的时候发送消息。

> [!TIP]
> 关于 unified_msg_origin。
> unified_msg_origin 是一个字符串，记录了一个会话的唯一 ID，AstrBot 能够据此找到属于哪个消息平台的哪个会话。这样就能够实现在 `send_message` 的时候，发送消息到正确的会话。有关 MessageChain，请参见接下来的一节。

### 富媒体消息

AstrBot 支持发送富媒体消息，比如图片、语音、视频等。使用 `MessageChain` 来构建消息。

```python
import astrbot.api.message_components as Comp

@filter.command("helloworld")
async def helloworld(self, event: AstrMessageEvent):
    chain = [
        Comp.At(qq=event.get_sender_id()), # At 消息发送者
        Comp.Plain("来看这个图："),
        Comp.Image.fromURL("https://example.com/image.jpg"), # 从 URL 发送图片
        Comp.Image.fromFileSystem("path/to/image.jpg"), # 从本地文件目录发送图片
        Comp.Plain("这是一个图片。")
    ]
    yield event.chain_result(chain)
```

上面构建了一个 `message chain`，也就是消息链，最终会发送一条包含了图片和文字的消息，并且保留顺序。

> [!TIP]
> 在 aiocqhttp 消息适配器中，对于 `plain` 类型的消息，在发送中会使用 `strip()` 方法去除空格及换行符，可以在消息前后添加零宽空格 `\u200b` 以解决这个问题。

类似地，

**文件 File**

```py
Comp.File(file="path/to/file.txt", name="file.txt") # 部分平台不支持
```

**语音 Record**

```py
path = "path/to/record.wav" # 暂时只接受 wav 格式，其他格式请自行转换
Comp.Record(file=path, url=path)
```

**视频 Video**

```py
path = "path/to/video.mp4"
Comp.Video.fromFileSystem(path=path)
Comp.Video.fromURL(url="https://example.com/video.mp4")
```

### 发送视频消息

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.command("test")
async def test(self, event: AstrMessageEvent):
    from astrbot.api.message_components import Video
    # fromFileSystem 需要用户的协议端和机器人端处于一个系统中。
    music = Video.fromFileSystem(
        path="test.mp4"
    )
    # 更通用
    music = Video.fromURL(
        url="https://example.com/video.mp4"
    )
    yield event.chain_result([music])
```

![发送视频消息](/source/images/plugin/db93a2bb-671c-4332-b8ba-9a91c35623c2.png)

### 发送群合并转发消息

> 大多数平台都不支持此种消息类型，当前适配情况：OneBot v11

可以按照如下方式发送群合并转发消息。

```py
from astrbot.api.event import filter, AstrMessageEvent

@filter.command("test")
async def test(self, event: AstrMessageEvent):
    from astrbot.api.message_components import Node, Plain, Image
    node = Node(
        uin=905617992,
        name="Soulter",
        content=[
            Plain("hi"),
            Image.fromFileSystem("test.jpg")
        ]
    )
    yield event.chain_result([node])
```

![发送群合并转发消息](/source/images/plugin/image-4.png)

## 插件配置

来源: https://docs.astrbot.app/dev/star/guides/plugin-config.html

随着插件功能的增加，可能需要定义一些配置以让用户自定义插件的行为。

AstrBot 提供了”强大“的配置解析和可视化功能。能够让用户在管理面板上直接配置插件，而不需要修改代码。

### 配置定义

要注册配置，首先需要在您的插件目录下添加一个 `_conf_schema.json` 的 json 文件。

文件内容是一个 `Schema`（模式），用于表示配置。Schema 是 json 格式的，例如上图的 Schema 是：

```json
{
  "token": {
    "description": "Bot Token",
    "type": "string",
  },
  "sub_config": {
    "description": "测试嵌套配置",
    "type": "object",
    "hint": "xxxx",
    "items": {
      "name": {
        "description": "testsub",
        "type": "string",
        "hint": "xxxx"
      },
      "id": {
        "description": "testsub",
        "type": "int",
        "hint": "xxxx"
      },
      "time": {
        "description": "testsub",
        "type": "int",
        "hint": "xxxx",
        "default": 123
      }
    }
  }
}
```

- `type`: **此项必填**。配置的类型。支持 `string`, `text`, `int`, `float`, `bool`, `object`, `list`。当类型为 `text` 时，将会可视化为一个更大的可拖拽宽高的 textarea 组件，以适应大文本。
- `description`: 可选。配置的描述。建议一句话描述配置的行为。
- `hint`: 可选。配置的提示信息，表现在上图中右边的问号按钮，当鼠标悬浮在问号按钮上时显示。
- `obvious_hint`: 可选。配置的 hint 是否醒目显示。如上图的 `token`。
- `default`: 可选。配置的默认值。如果用户没有配置，将使用默认值。int 是 0，float 是 0.0，bool 是 False，string 是 ""，object 是 {}，list 是 []。
- `items`: 可选。如果配置的类型是 `object`，需要添加 `items` 字段。`items` 的内容是这个配置项的子 Schema。理论上可以无限嵌套，但是不建议过多嵌套。
- `invisible`: 可选。配置是否隐藏。默认是 `false`。如果设置为 `true`，则不会在管理面板上显示。
- `options`: 可选。一个列表，如 `"options": ["chat", "agent", "workflow"]`。提供下拉列表可选项。
- `editor_mode`: 可选。是否启用代码编辑器模式。需要 AstrBot >= `v3.5.10`, 低于这个版本不会报错，但不会生效。默认是 false。
- `editor_language`: 可选。代码编辑器的代码语言，默认为 `json`。
- `editor_theme`: 可选。代码编辑器的主题，可选值有 `vs-light`（默认）， `vs-dark`。
- `_special`: 可选。用于调用 AstrBot 提供的可视化提供商选取、人格选取、知识库选取等功能，详见下文。

其中，如果启用了代码编辑器，效果如下图所示:

![editor_mode](/source/images/plugin/image-6.png)

![editor_mode_fullscreen](/source/images/plugin/image-7.png)

**_special** 字段仅 v4.0.0 之后可用。目前支持填写 `select_provider`, `select_provider_tts`, `select_provider_stt`, `select_persona`，用于让用户快速选择用户在 WebUI 上已经配置好的模型提供商、人设等数据。结果均为字符串。以 select_provider 为例，将呈现以下效果:

![image](/source/images/plugin/image.png)

### 在插件中使用配置

AstrBot 在载入插件时会检测插件目录下是否有 `_conf_schema.json` 文件，如果有，会自动解析配置并保存在 `data/config/<plugin_name>_config.json` 下（依照 Schema 创建的配置文件实体），并在实例化插件类时传入给 `__init__()`。

```py
from astrbot.api import AstrBotConfig

@register("config", "Soulter", "一个配置示例", "1.0.0")
class ConfigPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig): # AstrBotConfig 继承自 Dict，拥有字典的所有方法
        super().__init__(context)
        self.config = config
        print(self.config)

        # 支持直接保存配置
        # self.config.save_config() # 保存配置
```

### 配置更新

您在发布不同版本更新 Schema 时，AstrBot 会递归检查 Schema 的配置项，自动为缺失的配置项添加默认值、移除不存在的配置项。

## AI

来源: https://docs.astrbot.app/dev/star/guides/ai.html

AstrBot 内置了对多种大语言模型（LLM）提供商的支持，并且提供了统一的接口，方便插件开发者调用各种 LLM 服务。

您可以使用 AstrBot 提供的 LLM / Agent 接口来实现自己的智能体。

我们在 `v4.5.7` 版本之后对 LLM 提供商的调用方式进行了较大调整，推荐使用新的调用方式。新的调用方式更加简洁，并且支持更多的功能。当然，您仍然可以使用[旧的调用方式](/dev/star/plugin#ai)。

### 获取当前会话使用的聊天模型 ID

> [!TIP]
> 在 v4.5.7 时加入

```py
umo = event.unified_msg_origin
provider_id = await self.context.get_current_chat_provider_id(umo=umo)
```

### 调用大模型

> [!TIP]
> 在 v4.5.7 时加入

```py
llm_resp = await self.context.llm_generate(
    chat_provider_id=provider_id, # 聊天模型 ID
    prompt="Hello, world!",
)
# print(llm_resp.completion_text) # 获取返回的文本
```

### 定义 Tool

Tool 是大语言模型调用外部工具的能力。

```py
from pydantic import Field
from pydantic.dataclasses import dataclass

from astrbot.core.agent.run_context import ContextWrapper
from astrbot.core.agent.tool import FunctionTool, ToolExecResult
from astrbot.core.astr_agent_context import AstrAgentContext


@dataclass
class BilibiliTool(FunctionTool[AstrAgentContext]):
    name: str = "bilibili_videos"  # 工具名称
    description: str = "A tool to fetch Bilibili videos."  # 工具描述
    parameters: dict = Field(
        default_factory=lambda: {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "string",
                    "description": "Keywords to search for Bilibili videos.",
                },
            },
            "required": ["keywords"],
        }
    )

    async def call(
        self, context: ContextWrapper[AstrAgentContext], **kwargs
    ) -> ToolExecResult:
        return "1. 视频标题：如何使用AstrBot\n视频链接：xxxxxx"
```

### 注册 Tool 到 AstrBot

在上面定义好 Tool 之后，如果你需要实现的功能是让用户在使用 AstrBot 进行对话时自动调用该 Tool，那么你需要在插件的 __init__ 方法中将 Tool 注册到 AstrBot 中：

```py
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # >= v4.5.1 使用：
        self.context.add_llm_tools(BilibiliTool(), SecondTool(), ...)

        # < v4.5.1 之前使用：
        tool_mgr = self.context.provider_manager.llm_tools
        tool_mgr.func_list.append(BilibiliTool())
```

#### 通过装饰器定义 Tool 和注册 Tool

除了上述的通过 `@dataclass` 定义 Tool 的方式之外，你也可以使用装饰器的方式注册 tool 到 AstrBot。如果请务必按照以下格式编写一个工具（包括函数注释，AstrBot 会解析该函数注释，请务必将注释格式写对）

```py{3,4,5,6,7}
@filter.llm_tool(name="get_weather") # 如果 name 不填，将使用函数名
async def get_weather(self, event: AstrMessageEvent, location: str) -> MessageEventResult:
    '''获取天气信息。

    Args:
        location(string): 地点
    '''
    resp = self.get_weather_from_api(location)
    yield event.plain_result("天气信息: " + resp)
```

在 `location(string): 地点` 中，`location` 是参数名，`string` 是参数类型，`地点` 是参数描述。

支持的参数类型有 `string`, `number`, `object`, `boolean`, `array`。在 v4.5.7 之后，支持对 `array` 类型参数指定子类型，例如 `array[string]`。

### 调用 Agent

> [!TIP]
> 在 v4.5.7 时加入

Agent 可以被定义为 system_prompt + tools + llm 的结合体，可以实现更复杂的智能体行为。

在上面定义好 Tool 之后，可以通过以下方式调用 Agent：

```py
llm_resp = await self.context.tool_loop_agent(
    event=event,
    chat_provider_id=prov_id,
    prompt="搜索一下 bilibili 上关于 AstrBot 的相关视频。",
    tools=ToolSet([BilibiliTool()]),
    max_steps=30, # Agent 最大执行步骤
    tool_call_timeout=60, # 工具调用超时时间
)
# print(llm_resp.completion_text) # 获取返回的文本
```

`tool_loop_agent()` 方法会自动处理工具调用和大模型请求的循环，直到大模型不再调用工具或者达到最大步骤数为止。

### Multi-Agent

> [!TIP]
> 在 v4.5.7 时加入

Multi-Agent（多智能体）系统将复杂应用分解为多个专业化智能体，它们协同解决问题。不同于依赖单个智能体处理每一步，多智能体架构允许将更小、更专注的智能体组合成协调的工作流程。我们使用 `agent-as-tool` 模式来实现多智能体系统。

在下面的例子中，我们定义了一个主智能体（Main Agent），它负责根据用户查询将任务分配给不同的子智能体（Sub-Agents）。每个子智能体专注于特定任务，例如获取天气信息。

![multi-agent-example-1](multi-agent-example-1.svg)

定义 Tools:

```py
from pydantic import Field
from pydantic.dataclasses import dataclass

from astrbot.core.agent.run_context import ContextWrapper
from astrbot.core.agent.tool import FunctionTool, ToolExecResult
from astrbot.core.astr_agent_context import AstrAgentContext

@dataclass
class AssignAgentTool(FunctionTool[AstrAgentContext]):
    """Main agent uses this tool to decide which sub-agent to delegate a task to."""

    name: str = "assign_agent"
    description: str = "Assign an agent to a task based on the given query"
    parameters: dict = Field(
        default_factory=lambda: {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to call the sub-agent with.",
                },
            },
            "required": ["query"],
        }
    )

    async def call(
        self, context: ContextWrapper[AstrAgentContext], **kwargs
    ) -> ToolExecResult:
        # Here you would implement the actual agent assignment logic.
        # For demonstration purposes, we'll return a dummy response.
        return "Based on the query, you should assign agent 1."


@dataclass
class WeatherTool(FunctionTool[AstrAgentContext]):
    """In this example, sub agent 1 uses this tool to get weather information."""

    name: str = "weather"
    description: str = "Get weather information for a location"
    parameters: dict = Field(
        default_factory=lambda: {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get weather information for.",
                },
            },
            "required": ["city"],
        }
    )

    async def call(
        self, context: ContextWrapper[AstrAgentContext], **kwargs
    ) -> ToolExecResult:
        city = kwargs["city"]
        # Here you would implement the actual weather fetching logic.
        # For demonstration purposes, we'll return a dummy response.
        return f"The current weather in {city} is sunny with a temperature of 25°C."


@dataclass
class SubAgent1(FunctionTool[AstrAgentContext]):
    """Define a sub-agent as a function tool."""

    name: str = "subagent1_name"
    description: str = "subagent1_description"
    parameters: dict = Field(
        default_factory=lambda: {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to call the sub-agent with.",
                },
            },
            "required": ["query"],
        }
    )

    async def call(
        self, context: ContextWrapper[AstrAgentContext], **kwargs
    ) -> ToolExecResult:
        ctx = context.context.context
        event = context.context.event
        logger.info(f"the llm context messages: {context.messages}")
        llm_resp = await ctx.tool_loop_agent(
            event=event,
            chat_provider_id=await ctx.get_current_chat_provider_id(
                event.unified_msg_origin
            ),
            prompt=kwargs["query"],
            tools=ToolSet([WeatherTool()]),
            max_steps=30,
        )
        return llm_resp.completion_text


@dataclass
class SubAgent2(FunctionTool[AstrAgentContext]):
    """Define a sub-agent as a function tool."""

    name: str = "subagent2_name"
    description: str = "subagent2_description"
    parameters: dict = Field(
        default_factory=lambda: {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to call the sub-agent with.",
                },
            },
            "required": ["query"],
        }
    )

    async def call(
        self, context: ContextWrapper[AstrAgentContext], **kwargs
    ) -> ToolExecResult:
        return "I am useless :(, you shouldn't call me :("
```

然后，同样地，通过 `tool_loop_agent()` 方法调用 Agent：

```py
@filter.command("test")
async def test(self, event: AstrMessageEvent):
    umo = event.unified_msg_origin
    prov_id = await self.context.get_current_chat_provider_id(umo)
    llm_resp = await self.context.tool_loop_agent(
        event=event,
        chat_provider_id=prov_id,
        prompt="Test calling sub-agent for Beijing's weather information.",
        system_prompt=(
            "You are the main agent. Your task is to delegate tasks to sub-agents based on user queries."
            "Before delegating, use the 'assign_agent' tool to determine which sub-agent is best suited for the task."
        ),
        tools=ToolSet([SubAgent1(), SubAgent2(), AssignAgentTool()]),
        max_steps=30,
    )
    yield event.plain_result(llm_resp.completion_text)
```

### 对话管理器

#### 获取会话当前的 LLM 对话历史 `get_conversation`

```py
from astrbot.core.conversation_mgr import Conversation

uid = event.unified_msg_origin
conv_mgr = self.context.conversation_manager
curr_cid = await conv_mgr.get_curr_conversation_id(uid)
conversation = await conv_mgr.get_conversation(uid, curr_cid)  # Conversation
```

::: details Conversation 类型定义

```py
@dataclass
class Conversation:
    """The conversation entity representing a chat session."""

    platform_id: str
    """The platform ID in AstrBot"""
    user_id: str
    """The user ID associated with the conversation."""
    cid: str
    """The conversation ID, in UUID format."""
    history: str = ""
    """The conversation history as a string."""
    title: str | None = ""
    """The title of the conversation. For now, it's only used in WebChat."""
    persona_id: str | None = ""
    """The persona ID associated with the conversation."""
    created_at: int = 0
    """The timestamp when the conversation was created."""
    updated_at: int = 0
    """The timestamp when the conversation was last updated."""
```

:::

#### 快速添加 LLM 记录到对话 `add_message_pair`

```py
from astrbot.core.agent.message import (
    AssistantMessageSegment,
    UserMessageSegment,
    TextPart,
)

curr_cid = await conv_mgr.get_curr_conversation_id(event.unified_msg_origin)
user_msg = UserMessageSegment(content=[TextPart(text="hi")])
llm_resp = await self.context.llm_generate(
    chat_provider_id=provider_id, # 聊天模型 ID
    contexts=[user_msg], # 当未指定 prompt 时，使用 contexts 作为输入；同时指定 prompt 和 contexts 时，prompt 会被添加到 LLM 输入的最后
)
await conv_mgr.add_message_pair(
    cid=curr_cid,
    user_message=user_msg,
    assistant_message=AssistantMessageSegment(
        content=[TextPart(text=llm_resp.completion_text)]
    ),
)
```

#### 主要方法

##### `new_conversation`

- __Usage__  
  在当前会话中新建一条对话，并自动切换为该对话。
- __Arguments__  
  - `unified_msg_origin: str` – 形如 `platform_name:message_type:session_id`  
  - `platform_id: str | None` – 平台标识，默认从 `unified_msg_origin` 解析  
  - `content: list[dict] | None` – 初始历史消息  
  - `title: str | None` – 对话标题  
  - `persona_id: str | None` – 绑定的 persona ID
- __Returns__  
  `str` – 新生成的 UUID 对话 ID

##### `switch_conversation`

- __Usage__  
  将会话切换到指定的对话。
- __Arguments__  
  - `unified_msg_origin: str`  
  - `conversation_id: str`
- __Returns__  
  `None`

##### `delete_conversation`

- __Usage__  
  删除会话中的某条对话；若 `conversation_id` 为 `None`，则删除当前对话。
- __Arguments__  
  - `unified_msg_origin: str`  
  - `conversation_id: str | None`
- __Returns__  
  `None`

##### `get_curr_conversation_id`

- __Usage__  
  获取当前会话正在使用的对话 ID。
- __Arguments__  
  - `unified_msg_origin: str`
- __Returns__  
  `str | None` – 当前对话 ID，不存在时返回 `None`

##### `get_conversation`

- __Usage__  
  获取指定对话的完整对象；若不存在且 `create_if_not_exists=True` 则自动创建。
- __Arguments__  
  - `unified_msg_origin: str`  
  - `conversation_id: str`  
  - `create_if_not_exists: bool = False`
- __Returns__  
  `Conversation | None`

##### `get_conversations`

- __Usage__  
  拉取用户或平台下的全部对话列表。
- __Arguments__  
  - `unified_msg_origin: str | None` – 为 `None` 时不过滤用户  
  - `platform_id: str | None`
- __Returns__  
  `List[Conversation]`

##### `update_conversation`

- __Usage__  
  更新对话的标题、历史记录或 persona_id。
- __Arguments__  
  - `unified_msg_origin: str`  
  - `conversation_id: str | None` – 为 `None` 时使用当前对话  
  - `history: list[dict] | None`  
  - `title: str | None`  
  - `persona_id: str | None`
- __Returns__  
  `None`

### 人格设定管理器

`PersonaManager` 负责统一加载、缓存并提供所有人格（Persona）的增删改查接口，同时兼容 AstrBot 4.x 之前的旧版人格格式（v3）。  
初始化时会自动从数据库读取全部人格，并生成一份 v3 兼容数据，供旧代码无缝使用。

```py
persona_mgr = self.context.persona_manager
```

#### 主要方法

##### `get_persona`

- __Usage__
  获取根据人格 ID 获取人格数据。
- __Arguments__
  - `persona_id: str` – 人格 ID
- __Returns__
  `Persona` – 人格数据，若不存在则返回 None
- __Raises__
  `ValueError` – 当不存在时抛出

##### `get_all_personas`

- __Usage__  
  一次性获取数据库中所有人格。
- __Returns__  
  `list[Persona]` – 人格列表，可能为空

##### `create_persona`

- __Usage__  
  新建人格并立即写入数据库，成功后自动刷新本地缓存。
- __Arguments__  
  - `persona_id: str` – 新人格 ID（唯一）  
  - `system_prompt: str` – 系统提示词  
  - `begin_dialogs: list[str]` – 可选，开场对话（偶数条，user/assistant 交替）  
  - `tools: list[str]` – 可选，允许使用的工具列表；`None`=全部工具，`[]`=禁用全部
- __Returns__  
  `Persona` – 新建后的人格对象
- __Raises__  
  `ValueError` – 若 `persona_id` 已存在

##### `update_persona`

- __Usage__  
  更新现有人格的任意字段，并同步到数据库与缓存。
- __Arguments__  
  - `persona_id: str` – 待更新的人格 ID  
  - `system_prompt: str` – 可选，新的系统提示词  
  - `begin_dialogs: list[str]` – 可选，新的开场对话  
  - `tools: list[str]` – 可选，新的工具列表；语义同 `create_persona`
- __Returns__  
  `Persona` – 更新后的人格对象
- __Raises__  
  `ValueError` – 若 `persona_id` 不存在

##### `delete_persona`

- __Usage__  
  删除指定人格，同时清理数据库与缓存。
- __Arguments__  
  - `persona_id: str` – 待删除的人格 ID
- __Raises__  
  `Valueable` – 若 `persona_id` 不存在

##### `get_default_persona_v3`

- __Usage__  
  根据当前会话配置，获取应使用的默认人格（v3 格式）。  
  若配置未指定或指定的人格不存在，则回退到 `DEFAULT_PERSONALITY`。
- __Arguments__  
  - `umo: str | MessageSession | None` – 会话标识，用于读取用户级配置
- __Returns__  
  `Personality` – v3 格式的默认人格对象

::: details Persona / Personality 类型定义

```py

class Persona(SQLModel, table=True):
    """Persona is a set of instructions for LLMs to follow.

    It can be used to customize the behavior of LLMs.
    """

    __tablename__ = "personas"

    id: int = Field(primary_key=True, sa_column_kwargs={"autoincrement": True})
    persona_id: str = Field(max_length=255, nullable=False)
    system_prompt: str = Field(sa_type=Text, nullable=False)
    begin_dialogs: Optional[list] = Field(default=None, sa_type=JSON)
    """a list of strings, each representing a dialog to start with"""
    tools: Optional[list] = Field(default=None, sa_type=JSON)
    """None means use ALL tools for default, empty list means no tools, otherwise a list of tool names."""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc)},
    )

    __table_args__ = (
        UniqueConstraint(
            "persona_id",
            name="uix_persona_id",
        ),
    )


class Personality(TypedDict):
    """LLM 人格类。

    在 v4.0.0 版本及之后，推荐使用上面的 Persona 类。并且， mood_imitation_dialogs 字段已被废弃。
    """

    prompt: str
    name: str
    begin_dialogs: list[str]
    mood_imitation_dialogs: list[str]
    """情感模拟对话预设。在 v4.0.0 版本及之后，已被废弃。"""
    tools: list[str] | None
    """工具列表。None 表示使用所有工具，空列表表示不使用任何工具"""
```

:::

## 插件存储

来源: https://docs.astrbot.app/dev/star/guides/storage.html

### 简单 KV 存储

> [!TIP]
> 该功能需要 AstrBot 版本 >= 4.9.2。

插件可以使用 AstrBot 提供的简单 KV 存储功能来存储一些配置信息或临时数据。该存储是基于插件维度的，每个插件有独立的存储空间，互不干扰。

```py
class Main(star.Star):
    @filter.command("hello")
    async def hello(self, event: AstrMessageEvent):
        """Aloha!"""
        await self.put_kv_data("greeted", True)
        greeted = await self.get_kv_data("greeted", False)
        await self.delete_kv_data("greeted")
```


### 存储大文件规范

为了规范插件存储大文件的行为，请将大文件存储于 `data/plugin_data/{plugin_name}/` 目录下。

你可以通过以下代码获取插件数据目录：

```py
from astrbot.core.utils.astrbot_path import get_astrbot_data_path

plugin_data_path = get_astrbot_data_path() / "plugin_data" / self.name # self.name 为插件名称，在 v4.9.2 及以上版本可用，低于此版本请自行指定插件名称
```

## 文转图

来源: https://docs.astrbot.app/dev/star/guides/html-to-pic.html

### 基本

AstrBot 支持将文字渲染成图片。

```python
@filter.command("image") # 注册一个 /image 指令，接收 text 参数。
async def on_aiocqhttp(self, event: AstrMessageEvent, text: str):
    url = await self.text_to_image(text) # text_to_image() 是 Star 类的一个方法。
    # path = await self.text_to_image(text, return_url = False) # 如果你想保存图片到本地
    yield event.image_result(url)

```

![image](/source/images/plugin/image-3.png)

### 自定义(基于 HTML)

如果你觉得上面渲染出来的图片不够美观，你可以使用自定义的 HTML 模板来渲染图片。

AstrBot 支持使用 `HTML + Jinja2` 的方式来渲染文转图模板。

```py{7}
# 自定义的 Jinja2 模板，支持 CSS
TMPL = '''
<div style="font-size: 32px;">
<h1 style="color: black">Todo List</h1>

<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</div>
'''

@filter.command("todo")
async def custom_t2i_tmpl(self, event: AstrMessageEvent):
    options = {} # 可选择传入渲染选项。
    url = await self.html_render(TMPL, {"items": ["吃饭", "睡觉", "玩原神"]}, options=options) # 第二个参数是 Jinja2 的渲染数据
    yield event.image_result(url)
```

返回的结果:

![image](/source/images/plugin/fcc2dcb472a91b12899f617477adc5c7.png)

这只是一个简单的例子。得益于 HTML 和 DOM 渲染器的强大性，你可以进行更复杂和更美观的的设计。除此之外，Jinja2 支持循环、条件等语法以适应列表、字典等数据结构。你可以从网上了解更多关于 Jinja2 的知识。

**图片渲染选项(options)**：

请参考 Playwright 的 [screenshot](https://playwright.dev/python/docs/api/class-page#page-screenshot) API。

- `timeout` (float, optional): 截图超时时间.
- `type` (Literal["jpeg", "png"], optional): 截图图片类型.
- `quality` (int, optional): 截图质量，仅适用于 JPEG 格式图片.
- `omit_background` (bool, optional): 是否允许隐藏默认的白色背景，这样就可以截透明图了，仅适用于 PNG 格式
- `full_page` (bool, optional): 是否截整个页面而不是仅设置的视口大小，默认为 True.
- `clip` (dict, optional): 截图后裁切的区域。参考 Playwright screenshot API。
- `animations`: (Literal["allow", "disabled"], optional): 是否允许播放 CSS 动画.
- `caret`: (Literal["hide", "initial"], optional): 当设置为 hide 时，截图时将隐藏文本插入符号，默认为 hide.
- `scale`: (Literal["css", "device"], optional): 页面缩放设置. 当设置为 css 时，则将设备分辨率与 CSS 中的像素一一对应，在高分屏上会使得截图变小. 当设置为 device 时，则根据设备的屏幕缩放设置或当前 Playwright 的 Page/Context 中的 device_scale_factor 参数来缩放.

## 会话控制

来源: https://docs.astrbot.app/dev/star/guides/session-control.html

> 大于等于 v3.4.36

为什么需要会话控制？考虑一个 成语接龙 插件，某个/群用户需要和机器人进行多次对话，而不是一次性的指令。这时候就需要会话控制。

```txt
用户: /成语接龙
机器人: 请发送一个成语
用户: 一马当先
机器人: 先见之明
用户: 明察秋毫
...
```

AstrBot 提供了开箱即用的会话控制功能：

导入：

```py
import astrbot.api.message_components as Comp
from astrbot.core.utils.session_waiter import (
    session_waiter,
    SessionController,
)
```

handler 内的代码可以如下：

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.command("成语接龙")
async def handle_empty_mention(self, event: AstrMessageEvent):
    """成语接龙具体实现"""
    try:
        yield event.plain_result("请发送一个成语~")

        # 具体的会话控制器使用方法
        @session_waiter(timeout=60, record_history_chains=False) # 注册一个会话控制器，设置超时时间为 60 秒，不记录历史消息链
        async def empty_mention_waiter(controller: SessionController, event: AstrMessageEvent):
            idiom = event.message_str # 用户发来的成语，假设是 "一马当先"

            if idiom == "退出":   # 假设用户想主动退出成语接龙，输入了 "退出"
                await event.send(event.plain_result("已退出成语接龙~"))
                controller.stop()    # 停止会话控制器，会立即结束。
                return

            if len(idiom) != 4:   # 假设用户输入的不是4字成语
                await event.send(event.plain_result("成语必须是四个字的呢~"))  # 发送回复，不能使用 yield
                return
                # 退出当前方法，不执行后续逻辑，但此会话并未中断，后续的用户输入仍然会进入当前会话

            # ...
            message_result = event.make_result()
            message_result.chain = [Comp.Plain("先见之明")] # import astrbot.api.message_components as Comp
            await event.send(message_result) # 发送回复，不能使用 yield

            controller.keep(timeout=60, reset_timeout=True) # 重置超时时间为 60s，如果不重置，则会继续之前的超时时间计时。

            # controller.stop() # 停止会话控制器，会立即结束。
            # 如果记录了历史消息链，可以通过 controller.get_history_chains() 获取历史消息链

        try:
            await empty_mention_waiter(event)
        except TimeoutError as _: # 当超时后，会话控制器会抛出 TimeoutError
            yield event.plain_result("你超时了！")
        except Exception as e:
            yield event.plain_result("发生错误，请联系管理员: " + str(e))
        finally:
            event.stop_event()
    except Exception as e:
        logger.error("handle_empty_mention error: " + str(e))
```

当激活会话控制器后，该发送人之后发送的消息会首先经过上面你定义的 `empty_mention_waiter` 函数处理，直到会话控制器被停止或者超时。

### SessionController

用于开发者控制这个会话是否应该结束，并且可以拿到历史消息链。

- keep(): 保持这个会话
  - timeout (float): 必填。会话超时时间。
  - reset_timeout (bool): 设置为 True 时, 代表重置超时时间, timeout 必须 > 0, 如果 <= 0 则立即结束会话。设置为 False 时, 代表继续维持原来的超时时间, 新 timeout = 原来剩余的 timeout + timeout (可以 < 0)
- stop(): 结束这个会话
- get_history_chains() -> List[List[Comp.BaseMessageComponent]]: 获取历史消息链

### 自定义会话 ID 算子

默认情况下，AstrBot 会话控制器会将基于 `sender_id` （发送人的 ID）作为识别不同会话的标识，如果想将一整个群作为一个会话，则需要自定义会话 ID 算子。

```py
import astrbot.api.message_components as Comp
from astrbot.core.utils.session_waiter import (
    session_waiter,
    SessionFilter,
    SessionController,
)

# 沿用上面的 handler
# ...
class CustomFilter(SessionFilter):
    def filter(self, event: AstrMessageEvent) -> str:
        return event.get_group_id() if event.get_group_id() else event.unified_msg_origin

await empty_mention_waiter(event, session_filter=CustomFilter()) # 这里传入 session_filter
# ...
```

这样之后，当群内一个用户发送消息后，会话控制器会将这个群作为一个会话，群内其他用户发送的消息也会被认为是同一个会话。

甚至，可以使用这个特性来让群内组队！

## 杂项

来源: https://docs.astrbot.app/dev/star/guides/other.html

### 获取消息平台实例

> v3.4.34 后

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.command("test")
async def test_(self, event: AstrMessageEvent):
    from astrbot.api.platform import AiocqhttpAdapter # 其他平台同理
    platform = self.context.get_platform(filter.PlatformAdapterType.AIOCQHTTP)
    assert isinstance(platform, AiocqhttpAdapter)
    # platform.get_client().api.call_action()
```

### 调用 QQ 协议端 API

```py
@filter.command("helloworld")
async def helloworld(self, event: AstrMessageEvent):
    if event.get_platform_name() == "aiocqhttp":
        # qq
        from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
        assert isinstance(event, AiocqhttpMessageEvent)
        client = event.bot # 得到 client
        payloads = {
            "message_id": event.message_obj.message_id,
        }
        ret = await client.api.call_action('delete_msg', **payloads) # 调用 协议端  API
        logger.info(f"delete_msg: {ret}")
```

关于 CQHTTP API，请参考如下文档：

Napcat API 文档：<https://napcat.apifox.cn/>

Lagrange API 文档：<https://lagrange-onebot.apifox.cn/>

### 获取载入的所有插件

```py
plugins = self.context.get_all_stars() # 返回 StarMetadata 包含了插件类实例、配置等等
```

### 获取加载的所有平台

```py
from astrbot.api.platform import Platform
platforms = self.context.platform_manager.get_insts() # List[Platform]
```

## 发布插件到插件市场

来源: https://docs.astrbot.app/dev/star/plugin-publish.html

在编写完插件后，你可以选择将插件发布到 AstrBot 的插件市场，让更多用户使用你的插件。

AstrBot 使用 GitHub 托管插件，因此你需要先将插件代码推送到之前创建的 GitHub 插件仓库中。

你可以前往 [AstrBot 插件市场](https://plugins.astrbot.app) 提交你的插件。进入该网站后，点击右下角的 `+` 按钮，填写好基本信息、作者信息、仓库信息等内容后，点击 `提交到 GTIHUB` 按钮，你将会被导航到 AstrBot 仓库的 Issue 提交页面，请确认信息无误后点击 `Create` 按钮提交，即可完成插件发布。

![fill out the form](/source/images/plugin-publish/image.png)

## 插件开发指南（旧）

来源: https://docs.astrbot.app/dev/star/plugin.html

几行代码开发一个插件！

> [!WARNING]
> **您仍然可以参考此页进行插件开发。**
>
> 由于插件实用 API 逐渐增多，目前已无法在单个页面中将所有 API 进行详尽介绍。因此此指南在 v4.5.7 之后已过时，请参考我们新的插件开发指南: [🌠 从这里开始](plugin-new.md)，新的指南内容上和此指南基本一致，但我们将会持续维护新的指南内容。

### 开发环境准备

#### 获取插件模板

1. 打开 AstrBot 插件模板: [helloworld](https://github.com/Soulter/helloworld)
2. 点击右上角的 `Use this template`
3. 然后点击 `Create new repository`。
4. 在 `Repository name` 处填写您的插件名。插件名格式:
   - 推荐以 `astrbot_plugin_` 开头；
   - 不能包含空格；
   - 保持全部字母小写；
   - 尽量简短。

![image](/source/images/plugin/image.png)

5. 点击右下角的 `Create repository`。

#### Clone 插件和 AstrBot 项目

Clone AstrBot 项目本体和刚刚创建的插件仓库到本地。

```bash
git clone https://github.com/AstrBotDevs/AstrBot
mkdir -p AstrBot/data/plugins
cd AstrBot/data/plugins
git clone 插件仓库地址
```

然后，使用 `VSCode` 打开 `AstrBot` 项目。找到 `data/plugins/<你的插件名字>` 目录。

更新 `metadata.yaml` 文件，填写插件的元数据信息。

> [!NOTE]
> AstrBot 插件市场的信息展示依赖于 `metadata.yaml` 文件。

#### 调试插件

AstrBot 采用在运行时注入插件的机制。因此，在调试插件时，需要启动 AstrBot 本体。

插件的代码修改后，可以在 AstrBot WebUI 的插件管理处找到自己的插件，点击 `管理`，点击 `重载插件` 即可。

#### 插件依赖管理

目前 AstrBot 对插件的依赖管理使用 `pip` 自带的 `requirements.txt` 文件。如果你的插件需要依赖第三方库，请务必在插件目录下创建 `requirements.txt` 文件并写入所使用的依赖库，以防止用户在安装你的插件时出现依赖未找到(Module Not Found)的问题。

> `requirements.txt` 的完整格式可以参考 [pip 官方文档](https://pip.pypa.io/en/stable/reference/requirements-file-format/)。

### 提要

#### 最小实例

插件模版中的 `main.py` 是一个最小的插件实例。

```python
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger # 使用 astrbot 提供的 logger 接口

@register("helloworld", "author", "一个简单的 Hello World 插件", "1.0.0", "repo url")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        '''这是一个 hello world 指令''' # 这是 handler 的描述，将会被解析方便用户了解插件内容。非常建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 获取消息的纯文本内容
        logger.info("触发hello world指令!")
        yield event.plain_result(f"Hello, {user_name}!") # 发送一条纯文本消息

    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''
```

解释如下：

1. 插件是继承自 `Star` 基类的类实现。
2. 开发者必须使用 `@register` 装饰器来注册插件，这是 AstrBot 识别和加载插件的必要条件。
3. 该装饰器提供了插件的元数据信息，包括名称、作者、描述、版本和仓库地址等信息。（该信息的优先级低于 `metadata.yaml` 文件）
4. 在 `__init__` 方法中会传入 `Context` 对象，这个对象包含了 AstrBot 的大多数组件
5. 具体的处理函数 `Handler` 在插件类中定义，如这里的 `helloworld` 函数。
6. 请务必使用 `from astrbot.api import logger` 来获取日志对象，而不是使用 `logging` 模块。

> [!TIP]
>
> `Handler` 一定需要在插件类中注册，前两个参数必须为 `self` 和 `event`。如果文件行数过长，可以将服务写在外部，然后在 `Handler` 中调用。
>
> 插件类所在的文件名需要命名为 `main.py`。

#### AstrMessageEvent

`AstrMessageEvent` 是 AstrBot 的消息事件对象。你可以通过 `AstrMessageEvent` 来获取消息发送者、消息内容等信息。

#### AstrBotMessage

`AstrBotMessage` 是 AstrBot 的消息对象。你可以通过 `AstrBotMessage` 来查看消息适配器下发的消息的具体内容。通过 `event.message_obj` 获取。

```py{11}
class AstrBotMessage:
    '''AstrBot 的消息对象'''
    type: MessageType  # 消息类型
    self_id: str  # 机器人的识别id
    session_id: str  # 会话id。取决于 unique_session 的设置。
    message_id: str  # 消息id
    group_id: str = "" # 群组id，如果为私聊，则为空
    sender: MessageMember  # 发送者
    message: List[BaseMessageComponent]  # 消息链。比如 [Plain("Hello"), At(qq=123456)]
    message_str: str  # 最直观的纯文本消息字符串，将消息链中的 Plain 消息（文本消息）连接起来
    raw_message: object
    timestamp: int  # 消息时间戳
```

其中，`raw_message` 是消息平台适配器的**原始消息对象**。

#### 消息链

`消息链`描述一个消息的结构，是一个有序列表，列表中每一个元素称为`消息段`。

引用方式：

```py
import astrbot.api.message_components as Comp
```

```
[Comp.Plain(text="Hello"), Comp.At(qq=123456), Comp.Image(file="https://example.com/image.jpg")]
```

> qq 是对应消息平台上的用户 ID。

消息链的结构使用了 `nakuru-project`。它一共有如下种消息类型。常用的已经用注释标注。

```py
ComponentTypes = {
    "plain": Plain, # 文本消息
    "text": Plain, # 文本消息，同上
    "face": Face, # QQ 表情
    "record": Record, # 语音
    "video": Video, # 视频
    "at": At, # At 消息发送者
    "music": Music, # 音乐
    "image": Image, # 图片
    "reply": Reply, # 回复消息
    "forward": Forward, # 转发消息
    "node": Node, # 转发消息中的节点
    "nodes": Nodes, # Node 的列表，用于支持一个转发消息中的多个节点
    "poke": Poke, # 戳一戳
}
```

请善于 debug 来了解消息结构：

```python{3,4}
@event_message_type(EventMessageType.ALL) # 注册一个过滤器，参见下文。
async def on_message(self, event: AstrMessageEvent):
    print(event.message_obj.raw_message) # 平台下发的原始消息在这里
    print(event.message_obj.message) # AstrBot 解析出来的消息链内容
```

> [!TIP]
>
> 在aiocqhttp消息适配器中，对于 `plain` 类型的消息，在发送中会自动使用 `strip()` 方法去除空格及换行符，可以使用零宽空格 `\u200b` 解决限制。

#### 平台适配矩阵

不是所有的平台都支持所有的消息类型。下方的表格展示了 AstrBot 支持的平台和消息类型的对应关系。

| 平台                 | At  | Plain | Image | Record | Video | Reply | 主动消息 |
| -------------------- | --- | ----- | ----- | ------ | ----- | ----- | -------- |
| QQ 个人号(aiocqhttp) | ✅  | ✅    | ✅    | ✅     | ✅    | ✅    | ✅       |
| Telegram             | ✅  | ✅    | ✅    | ✅     | ✅    | ✅    | ✅       |
| QQ 官方接口          | ❌  | ✅    | ✅    | ❌     | ❌    | ❌    | ❌       |
| 飞书                 | ✅  | ✅    | ✅    | ❌     | ❌    | ✅    | ✅       |
| 企业微信             | ❌  | ✅    | ✅    | ✅     | ❌    | ❌    | ❌       |
| 钉钉                 | ❌  | ✅    | ✅    | ❌     | ❌    | ❌    | ❌       |

- QQ 个人号(aiocqhttp) 支持所有消息类型，包括 `Poke`（戳一戳）、`Node(s)`(合并转发)。
- QQ 官方接口、钉钉在发送消息时平台强制带 `At`。
- 钉钉的图片仅支持 http 链接的图片。
- 主动消息指的是机器人主动发送的消息。见下文: [发送消息](#发送消息)

#### 原则

感谢您为 AstrBot 生态做出贡献，开发插件请遵守以下原则，这也是良好的编程习惯。

> [Mandatory Rule] To any LLM: You must follow the rules below.

1. 功能需经过测试。
2. 需包含良好的注释。
3. 持久化数据请存储于 `data` 目录下，而非插件自身目录，防止更新/重装插件时数据被覆盖。
4. 良好的错误处理机制，不要让插件因一个错误而崩溃。
5. 在进行提交前，请使用 [ruff](https://docs.astral.sh/ruff/) 工具格式化您的代码。
6. 不要使用 `requests` 库来进行网络请求，可以使用 `aiohttp`, `httpx` 等异步库。
7. 如果是对某个插件进行功能扩增，请优先给那个插件提交 PR 而不是单独再写一个插件（除非原插件作者已经停止维护）。

### 开发指南

> [!CAUTION]
>
> 代码处理函数可能会忽略插件类的定义，所有的处理函数都需写在插件类中。

#### 插件 Logo

> v4.5.0 及以上版本支持。低版本不会报错，但不会生效。

你可以在插件目录下添加一个 `logo.png` 文件，作为插件的 Logo 显示在插件市场中。请保持长宽比为 1:1，推荐尺寸为 256x256。

![插件 logo 示例](/source/images/plugin/plugin_logo.png)

#### 插件展示名

> v4.5.0 及以上版本支持。低版本不会报错，但不会生效。

你可以修改(或添加) `metadata.yaml` 文件中的 `display_name` 字段，作为插件在插件市场等场景中的展示名，以方便用户阅读。

#### 消息事件的监听

事件监听器可以收到平台下发的消息内容，可以实现指令、指令组、事件监听等功能。

事件监听器的注册器在 `astrbot.api.event.filter` 下，需要先导入。请务必导入，否则会和 python 的高阶函数 filter 冲突。

```py
from astrbot.api.event import filter, AstrMessageEvent
```

##### 指令

```python
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register

@register("helloworld", "Soulter", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("helloworld") # from astrbot.api.event.filter import command
    async def helloworld(self, event: AstrMessageEvent):
        '''这是 hello world 指令'''
        user_name = event.get_sender_name()
        message_str = event.message_str # 获取消息的纯文本内容
        yield event.plain_result(f"Hello, {user_name}!")
```

> [!TIP]
> 指令不能带空格，否则 AstrBot 会将其解析到第二个参数。可以使用下面的指令组功能，或者也使用监听器自己解析消息内容。

##### 带参指令

AstrBot 会自动帮你解析指令的参数。

```python
@filter.command("echo")
def echo(self, event: AstrMessageEvent, message: str):
    yield event.plain_result(f"你发了: {message}")

@filter.command("add")
def add(self, event: AstrMessageEvent, a: int, b: int):
    # /add 1 2 -> 结果是: 3
    yield event.plain_result(f"结果是: {a + b}")
```

##### 指令组

指令组可以帮助你组织指令。

```python
@filter.command_group("math")
def math(self):
    pass

@math.command("add")
async def add(self, event: AstrMessageEvent, a: int, b: int):
    # /math add 1 2 -> 结果是: 3
    yield event.plain_result(f"结果是: {a + b}")

@math.command("sub")
async def sub(self, event: AstrMessageEvent, a: int, b: int):
    # /math sub 1 2 -> 结果是: -1
    yield event.plain_result(f"结果是: {a - b}")
```

指令组函数内不需要实现任何函数，请直接 `pass` 或者添加函数内注释。指令组的子指令使用 `指令组名.command` 来注册。

当用户没有输入子指令时，会报错并，并渲染出该指令组的树形结构。

![image](/source/images/plugin/image-1.png)

![image](/source/images/plugin/898a169ae7ed0478f41c0a7d14cb4d64.png)

![image](/source/images/plugin/image-2.png)

理论上，指令组可以无限嵌套！

```py
'''
math
├── calc
│   ├── add (a(int),b(int),)
│   ├── sub (a(int),b(int),)
│   ├── help (无参数指令)
'''

@filter.command_group("math")
def math():
    pass

@math.group("calc") # 请注意，这里是 group，而不是 command_group
def calc():
    pass

@calc.command("add")
async def add(self, event: AstrMessageEvent, a: int, b: int):
    yield event.plain_result(f"结果是: {a + b}")

@calc.command("sub")
async def sub(self, event: AstrMessageEvent, a: int, b: int):
    yield event.plain_result(f"结果是: {a - b}")

@calc.command("help")
def calc_help(self, event: AstrMessageEvent):
    # /math calc help
    yield event.plain_result("这是一个计算器插件，拥有 add, sub 指令。")
```

##### 指令别名

> v3.4.28 后

可以为指令或指令组添加不同的别名：

```python
@filter.command("help", alias={'帮助', 'helpme'})
def help(self, event: AstrMessageEvent):
    yield event.plain_result("这是一个计算器插件，拥有 add, sub 指令。")
```

##### 事件类型过滤

###### 接收所有

这将接收所有的事件。

```python
@filter.event_message_type(filter.EventMessageType.ALL)
async def on_all_message(self, event: AstrMessageEvent):
    yield event.plain_result("收到了一条消息。")
```

###### 群聊和私聊

```python
@filter.event_message_type(filter.EventMessageType.PRIVATE_MESSAGE)
async def on_private_message(self, event: AstrMessageEvent):
    message_str = event.message_str # 获取消息的纯文本内容
    yield event.plain_result("收到了一条私聊消息。")
```

`EventMessageType` 是一个 `Enum` 类型，包含了所有的事件类型。当前的事件类型有 `PRIVATE_MESSAGE` 和 `GROUP_MESSAGE`。

###### 消息平台

```python
@filter.platform_adapter_type(filter.PlatformAdapterType.AIOCQHTTP | filter.PlatformAdapterType.QQOFFICIAL)
async def on_aiocqhttp(self, event: AstrMessageEvent):
    '''只接收 AIOCQHTTP 和 QQOFFICIAL 的消息'''
    yield event.plain_result("收到了一条信息")
```

当前版本下，`PlatformAdapterType` 有 `AIOCQHTTP`, `QQOFFICIAL`, `GEWECHAT`, `ALL`。

###### 管理员指令

```python
@filter.permission_type(filter.PermissionType.ADMIN)
@filter.command("test")
async def test(self, event: AstrMessageEvent):
    pass
```

仅管理员才能使用 `test` 指令。

##### 多个过滤器

支持同时使用多个过滤器，只需要在函数上添加多个装饰器即可。过滤器使用 `AND` 逻辑。也就是说，只有所有的过滤器都通过了，才会执行函数。

```python
@filter.command("helloworld")
@filter.event_message_type(filter.EventMessageType.PRIVATE_MESSAGE)
async def helloworld(self, event: AstrMessageEvent):
    yield event.plain_result("你好！")
```

##### 事件钩子

> [!TIP]
> 事件钩子不支持与上面的 @filter.command, @filter.command_group, @filter.event_message_type, @filter.platform_adapter_type, @filter.permission_type 一起使用。

###### Bot 初始化完成时

> v3.4.34 后

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.on_astrbot_loaded()
async def on_astrbot_loaded(self):
    print("AstrBot 初始化完成")

```

###### LLM 请求时

在 AstrBot 默认的执行流程中，在调用 LLM 前，会触发 `on_llm_request` 钩子。

可以获取到 `ProviderRequest` 对象，可以对其进行修改。

ProviderRequest 对象包含了 LLM 请求的所有信息，包括请求的文本、系统提示等。

```python
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.provider import ProviderRequest

@filter.on_llm_request()
async def my_custom_hook_1(self, event: AstrMessageEvent, req: ProviderRequest): # 请注意有三个参数
    print(req) # 打印请求的文本
    req.system_prompt += "自定义 system_prompt"

```

> 这里不能使用 yield 来发送消息。如需发送，请直接使用 `event.send()` 方法。

###### LLM 请求完成时

在 LLM 请求完成后，会触发 `on_llm_response` 钩子。

可以获取到 `ProviderResponse` 对象，可以对其进行修改。

```python
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.provider import LLMResponse

@filter.on_llm_response()
async def on_llm_resp(self, event: AstrMessageEvent, resp: LLMResponse): # 请注意有三个参数
    print(resp)
```

> 这里不能使用 yield 来发送消息。如需发送，请直接使用 `event.send()` 方法。

###### 发送消息前

在发送消息前，会触发 `on_decorating_result` 钩子。

可以在这里实现一些消息的装饰，比如转语音、转图片、加前缀等等

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.on_decorating_result()
async def on_decorating_result(self, event: AstrMessageEvent):
    result = event.get_result()
    chain = result.chain
    print(chain) # 打印消息链
    chain.append(Plain("!")) # 在消息链的最后添加一个感叹号
```

> 这里不能使用 yield 来发送消息。这个钩子只是用来装饰 event.get_result().chain 的。如需发送，请直接使用 `event.send()` 方法。

###### 发送消息后

在发送消息给消息平台后，会触发 `after_message_sent` 钩子。

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.after_message_sent()
async def after_message_sent(self, event: AstrMessageEvent):
    pass
```

> 这里不能使用 yield 来发送消息。如需发送，请直接使用 `event.send()` 方法。

##### 优先级

> 大于等于 v3.4.21。

指令、事件监听器、事件钩子可以设置优先级，先于其他指令、监听器、钩子执行。默认优先级是 `0`。

```python
@filter.command("helloworld", priority=1)
async def helloworld(self, event: AstrMessageEvent):
    yield event.plain_result("Hello!")
```

#### 消息的发送

##### 被动消息

被动消息指的是机器人被动回复消息。

```python
@filter.command("helloworld")
async def helloworld(self, event: AstrMessageEvent):
    yield event.plain_result("Hello!")
    yield event.plain_result("你好！")

    yield event.image_result("path/to/image.jpg") # 发送图片
    yield event.image_result("https://example.com/image.jpg") # 发送 URL 图片，务必以 http 或 https 开头
```

##### 主动消息

主动消息指的是机器人主动推送消息。某些平台可能不支持主动消息发送。

如果是一些定时任务或者不想立即发送消息，可以使用 `event.unified_msg_origin` 得到一个字符串并将其存储，然后在想发送消息的时候使用 `self.context.send_message(unified_msg_origin, chains)` 来发送消息。

```python
from astrbot.api.event import MessageChain

@filter.command("helloworld")
async def helloworld(self, event: AstrMessageEvent):
    umo = event.unified_msg_origin
    message_chain = MessageChain().message("Hello!").file_image("path/to/image.jpg")
    await self.context.send_message(event.unified_msg_origin, message_chain)
```

通过这个特性，你可以将 unified_msg_origin 存储起来，然后在需要的时候发送消息。

> [!TIP]
> 关于 unified_msg_origin。
> unified_msg_origin 是一个字符串，记录了一个会话的唯一 ID，AstrBot 能够据此找到属于哪个消息平台的哪个会话。这样就能够实现在 `send_message` 的时候，发送消息到正确的会话。有关 MessageChain，请参见接下来的一节。

##### 富媒体消息

AstrBot 支持发送富媒体消息，比如图片、语音、视频等。使用 `MessageChain` 来构建消息。

```python
import astrbot.api.message_components as Comp

@filter.command("helloworld")
async def helloworld(self, event: AstrMessageEvent):
    chain = [
        Comp.At(qq=event.get_sender_id()), # At 消息发送者
        Comp.Plain("来看这个图："),
        Comp.Image.fromURL("https://example.com/image.jpg"), # 从 URL 发送图片
        Comp.Image.fromFileSystem("path/to/image.jpg"), # 从本地文件目录发送图片
        Comp.Plain("这是一个图片。")
    ]
    yield event.chain_result(chain)
```

上面构建了一个 `message chain`，也就是消息链，最终会发送一条包含了图片和文字的消息，并且保留顺序。

类似地，

**文件 File**

```py
Comp.File(file="path/to/file.txt", name="file.txt") # 部分平台不支持
```

**语音 Record**

```py
path = "path/to/record.wav" # 暂时只接受 wav 格式，其他格式请自行转换
Comp.Record(file=path, url=path)
```

**视频 Video**

```py
path = "path/to/video.mp4"
Comp.Video.fromFileSystem(path=path)
Comp.Video.fromURL(url="https://example.com/video.mp4")
```

##### 发送群合并转发消息

> 当前适配情况：aiocqhttp

可以按照如下方式发送群合并转发消息。

```py
from astrbot.api.event import filter, AstrMessageEvent

@filter.command("test")
async def test(self, event: AstrMessageEvent):
    from astrbot.api.message_components import Node, Plain, Image
    node = Node(
        uin=905617992,
        name="Soulter",
        content=[
            Plain("hi"),
            Image.fromFileSystem("test.jpg")
        ]
    )
    yield event.chain_result([node])
```

![发送群合并转发消息](/source/images/plugin/image-4.png)

##### 发送视频消息

> 当前适配情况：aiocqhttp

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.command("test")
async def test(self, event: AstrMessageEvent):
    from astrbot.api.message_components import Video
    # fromFileSystem 需要用户的协议端和机器人端处于一个系统中。
    music = Video.fromFileSystem(
        path="test.mp4"
    )
    # 更通用
    music = Video.fromURL(
        url="https://example.com/video.mp4"
    )
    yield event.chain_result([music])
```

![发送视频消息](/source/images/plugin/db93a2bb-671c-4332-b8ba-9a91c35623c2.png)

##### 发送 QQ 表情

> 当前适配情况：仅 aiocqhttp

QQ 表情 ID 参考：<https://bot.q.qq.com/wiki/develop/api-v2/openapi/emoji/model.html#EmojiType>

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.command("test")
async def test(self, event: AstrMessageEvent):
    from astrbot.api.message_components import Face, Plain
    yield event.chain_result([Face(id=21), Plain("你好呀")])
```

![发送 QQ 表情](/source/images/plugin/image-5.png)

#### 控制事件传播

```python{6}
@filter.command("check_ok")
async def check_ok(self, event: AstrMessageEvent):
    ok = self.check() # 自己的逻辑
    if not ok:
        yield event.plain_result("检查失败")
        event.stop_event() # 停止事件传播
```

当事件停止传播，后续所有步骤将不会被执行。

假设有一个插件 A，A 终止事件传播之后所有后续操作都不会执行，比如执行其它插件的 handler、请求 LLM。

#### 插件配置

> 大于等于 v3.4.15

随着插件功能的增加，可能需要定义一些配置以让用户自定义插件的行为。

AstrBot 提供了”强大“的配置解析和可视化功能。能够让用户在管理面板上直接配置插件，而不需要修改代码。

![image](/source/images/plugin/QQ_1738149538737.png)

**Schema 介绍**

要注册配置，首先需要在您的插件目录下添加一个 `_conf_schema.json` 的 json 文件。

文件内容是一个 `Schema`（模式），用于表示配置。Schema 是 json 格式的，例如上图的 Schema 是：

```json
{
  "token": {
    "description": "Bot Token",
    "type": "string",
    "hint": "测试醒目提醒",
    "obvious_hint": true
  },
  "sub_config": {
    "description": "测试嵌套配置",
    "type": "object",
    "hint": "xxxx",
    "items": {
      "name": {
        "description": "testsub",
        "type": "string",
        "hint": "xxxx"
      },
      "id": {
        "description": "testsub",
        "type": "int",
        "hint": "xxxx"
      },
      "time": {
        "description": "testsub",
        "type": "int",
        "hint": "xxxx",
        "default": 123
      }
    }
  }
}
```

- `type`: **此项必填**。配置的类型。支持 `string`, `text`, `int`, `float`, `bool`, `object`, `list`。当类型为 `text` 时，将会可视化为一个更大的可拖拽宽高的 textarea 组件，以适应大文本。
- `description`: 可选。配置的描述。建议一句话描述配置的行为。
- `hint`: 可选。配置的提示信息，表现在上图中右边的问号按钮，当鼠标悬浮在问号按钮上时显示。
- `obvious_hint`: 可选。配置的 hint 是否醒目显示。如上图的 `token`。
- `default`: 可选。配置的默认值。如果用户没有配置，将使用默认值。int 是 0，float 是 0.0，bool 是 False，string 是 ""，object 是 {}，list 是 []。
- `items`: 可选。如果配置的类型是 `object`，需要添加 `items` 字段。`items` 的内容是这个配置项的子 Schema。理论上可以无限嵌套，但是不建议过多嵌套。
- `invisible`: 可选。配置是否隐藏。默认是 `false`。如果设置为 `true`，则不会在管理面板上显示。
- `options`: 可选。一个列表，如 `"options": ["chat", "agent", "workflow"]`。提供下拉列表可选项。
- `editor_mode`: 可选。是否启用代码编辑器模式。需要 AstrBot >= `v3.5.10`, 低于这个版本不会报错，但不会生效。默认是 false。
- `editor_language`: 可选。代码编辑器的代码语言，默认为 `json`。
- `editor_theme`: 可选。代码编辑器的主题，可选值有 `vs-light`（默认）， `vs-dark`。
- `_special`: 可选。用于调用 AstrBot 提供的可视化提供商选取、人格选取、知识库选取等功能，详见下文。

其中，如果启用了代码编辑器，效果如下图所示:

![editor_mode](/source/images/plugin/image-6.png)

![editor_mode_fullscreen](/source/images/plugin/image-7.png)

**_special** 字段仅 v4.0.0 之后可用。目前支持填写 `select_provider`, `select_provider_tts`, `select_provider_stt`, `select_persona`，用于让用户快速选择用户在 WebUI 上已经配置好的模型提供商、人设等数据。结果均为字符串。以 select_provider 为例，将呈现以下效果:

![image](/source/images/plugin/image.png)

**使用配置**

AstrBot 在载入插件时会检测插件目录下是否有 `_conf_schema.json` 文件，如果有，会自动解析配置并保存在 `data/config/<plugin_name>_config.json` 下（依照 Schema 创建的配置文件实体），并在实例化插件类时传入给 `__init__()`。

```py
from astrbot.api import AstrBotConfig

@register("config", "Soulter", "一个配置示例", "1.0.0")
class ConfigPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig): # AstrBotConfig 继承自 Dict，拥有字典的所有方法
        super().__init__(context)
        self.config = config
        print(self.config)

        # 支持直接保存配置
        # self.config.save_config() # 保存配置
```

**配置版本管理**

如果您在发布不同版本时更新了 Schema，请注意，AstrBot 会递归检查 Schema 的配置项，如果发现配置文件中缺失了某个配置项，会自动添加默认值。但是 AstrBot 不会删除配置文件中**多余的**配置项，即使这个配置项在新的 Schema 中不存在（您在新的 Schema 中删除了这个配置项）。

#### 文转图

##### 基本

AstrBot 支持将文字渲染成图片。

```python
@filter.command("image") # 注册一个 /image 指令，接收 text 参数。
async def on_aiocqhttp(self, event: AstrMessageEvent, text: str):
    url = await self.text_to_image(text) # text_to_image() 是 Star 类的一个方法。
    # path = await self.text_to_image(text, return_url = False) # 如果你想保存图片到本地
    yield event.image_result(url)

```

![image](/source/images/plugin/image-3.png)

##### 自定义(基于 HTML)

如果你觉得上面渲染出来的图片不够美观，你可以使用自定义的 HTML 模板来渲染图片。

AstrBot 支持使用 `HTML + Jinja2` 的方式来渲染文转图模板。

```py{7}
# 自定义的 Jinja2 模板，支持 CSS
TMPL = '''
<div style="font-size: 32px;">
<h1 style="color: black">Todo List</h1>

<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</div>
'''

@filter.command("todo")
async def custom_t2i_tmpl(self, event: AstrMessageEvent):
    options = {} # 可选择传入渲染选项。
    url = await self.html_render(TMPL, {"items": ["吃饭", "睡觉", "玩原神"]}, options=options) # 第二个参数是 Jinja2 的渲染数据
    yield event.image_result(url)
```

返回的结果:

![image](/source/images/plugin/fcc2dcb472a91b12899f617477adc5c7.png)

这只是一个简单的例子。得益于 HTML 和 DOM 渲染器的强大性，你可以进行更复杂和更美观的的设计。除此之外，Jinja2 支持循环、条件等语法以适应列表、字典等数据结构。你可以从网上了解更多关于 Jinja2 的知识。

**图片渲染选项(options)**：

请参考 Playwright 的 [screenshot](https://playwright.dev/python/docs/api/class-page#page-screenshot) API。

- `timeout` (float, optional): 截图超时时间.
- `type` (Literal["jpeg", "png"], optional): 截图图片类型.
- `quality` (int, optional): 截图质量，仅适用于 JPEG 格式图片.
- `omit_background` (bool, optional): 是否允许隐藏默认的白色背景，这样就可以截透明图了，仅适用于 PNG 格式
- `full_page` (bool, optional): 是否截整个页面而不是仅设置的视口大小，默认为 True.
- `clip` (dict, optional): 截图后裁切的区域。参考 Playwright screenshot API。
- `animations`: (Literal["allow", "disabled"], optional): 是否允许播放 CSS 动画.
- `caret`: (Literal["hide", "initial"], optional): 当设置为 hide 时，截图时将隐藏文本插入符号，默认为 hide.
- `scale`: (Literal["css", "device"], optional): 页面缩放设置. 当设置为 css 时，则将设备分辨率与 CSS 中的像素一一对应，在高分屏上会使得截图变小. 当设置为 device 时，则根据设备的屏幕缩放设置或当前 Playwright 的 Page/Context 中的 device_scale_factor 参数来缩放.
- `mask` (List["Locator"]], optional): 指定截图时的遮罩的 Locator。元素将被一颜色为 #FF00FF 的框覆盖.

#### 会话控制

> 大于等于 v3.4.36

为什么需要会话控制？考虑一个 成语接龙 插件，某个/群用户需要和机器人进行多次对话，而不是一次性的指令。这时候就需要会话控制。

```txt
用户: /成语接龙
机器人: 请发送一个成语
用户: 一马当先
机器人: 先见之明
用户: 明察秋毫
...
```

AstrBot 提供了开箱即用的会话控制功能：

导入：

```py
import astrbot.api.message_components as Comp
from astrbot.core.utils.session_waiter import (
    session_waiter,
    SessionController,
)
```

handler 内的代码可以如下：

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.command("成语接龙")
async def handle_empty_mention(self, event: AstrMessageEvent):
    """成语接龙具体实现"""
    try:
        yield event.plain_result("请发送一个成语~")

        # 具体的会话控制器使用方法
        @session_waiter(timeout=60, record_history_chains=False) # 注册一个会话控制器，设置超时时间为 60 秒，不记录历史消息链
        async def empty_mention_waiter(controller: SessionController, event: AstrMessageEvent):
            idiom = event.message_str # 用户发来的成语，假设是 "一马当先"

            if idiom == "退出":   # 假设用户想主动退出成语接龙，输入了 "退出"
                await event.send(event.plain_result("已退出成语接龙~"))
                controller.stop()    # 停止会话控制器，会立即结束。
                return

            if len(idiom) != 4:   # 假设用户输入的不是4字成语
                await event.send(event.plain_result("成语必须是四个字的呢~"))  # 发送回复，不能使用 yield
                return
                # 退出当前方法，不执行后续逻辑，但此会话并未中断，后续的用户输入仍然会进入当前会话

            # ...
            message_result = event.make_result()
            message_result.chain = [Comp.Plain("先见之明")] # import astrbot.api.message_components as Comp
            await event.send(message_result) # 发送回复，不能使用 yield

            controller.keep(timeout=60, reset_timeout=True) # 重置超时时间为 60s，如果不重置，则会继续之前的超时时间计时。

            # controller.stop() # 停止会话控制器，会立即结束。
            # 如果记录了历史消息链，可以通过 controller.get_history_chains() 获取历史消息链

        try:
            await empty_mention_waiter(event)
        except TimeoutError as _: # 当超时后，会话控制器会抛出 TimeoutError
            yield event.plain_result("你超时了！")
        except Exception as e:
            yield event.plain_result("发生错误，请联系管理员: " + str(e))
        finally:
            event.stop_event()
    except Exception as e:
        logger.error("handle_empty_mention error: " + str(e))
```

当激活会话控制器后，该发送人之后发送的消息会首先经过上面你定义的 `empty_mention_waiter` 函数处理，直到会话控制器被停止或者超时。

##### SessionController

用于开发者控制这个会话是否应该结束，并且可以拿到历史消息链。

- keep(): 保持这个会话
  - timeout (float): 必填。会话超时时间。
  - reset_timeout (bool): 设置为 True 时, 代表重置超时时间, timeout 必须 > 0, 如果 <= 0 则立即结束会话。设置为 False 时, 代表继续维持原来的超时时间, 新 timeout = 原来剩余的 timeout + timeout (可以 < 0)
- stop(): 结束这个会话
- get_history_chains() -> List[List[Comp.BaseMessageComponent]]: 获取历史消息链

##### 自定义会话 ID 算子

默认情况下，AstrBot 会话控制器会将基于 `sender_id` （发送人的 ID）作为识别不同会话的标识，如果想将一整个群作为一个会话，则需要自定义会话 ID 算子。

```py
import astrbot.api.message_components as Comp
from astrbot.core.utils.session_waiter import (
    session_waiter,
    SessionFilter,
    SessionController,
)

# 沿用上面的 handler
# ...
class CustomFilter(SessionFilter):
    def filter(self, event: AstrMessageEvent) -> str:
        return event.get_group_id() if event.get_group_id() else event.unified_msg_origin

await empty_mention_waiter(event, session_filter=CustomFilter()) # 这里传入 session_filter
# ...
```

这样之后，当群内一个用户发送消息后，会话控制器会将这个群作为一个会话，群内其他用户发送的消息也会被认为是同一个会话。

甚至，可以使用这个特性来让群内组队！

#### AI

##### 通过提供商调用 LLM

获取提供商有以下几种方式:

- 获取当前使用的大语言模型提供商: `self.context.get_using_provider(umo=event.unified_msg_origin)`。
- 根据 ID 获取大语言模型提供商: `self.context.get_provider_by_id(provider_id="xxxx")`。
- 获取所有大语言模型提供商: `self.context.get_all_providers()`。

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.command("test")
async def test(self, event: AstrMessageEvent):
    # func_tools_mgr = self.context.get_llm_tool_manager()
    prov = self.context.get_using_provider(umo=event.unified_msg_origin)
    if prov:
        llm_resp = await provider.text_chat(
            prompt="Hi!",
            context=[
                {"role": "user", "content": "balabala"},
                {"role": "assistant", "content": "response balabala"}
            ],
            system_prompt="You are a helpful assistant."
        )
        print(llm_resp)
```

`Provider.text_chat()` 用于请求 LLM。其返回 `LLMResponse` 方法。除了上面的三个参数，其还支持:

- `func_tool`(ToolSet): 可选。用于传入函数工具。参考 [函数工具](#函数工具)。
- `image_urls`(List[str]): 可选。用于传入请求中带有的图片 URL 列表。支持文件路径。
- `model`(str): 可选。用于强制指定使用的模型。默认使用这个提供商默认配置的模型。
- `tool_calls_result`(dict): 可选。用于传入工具调用的结果。

::: details LLMResponse 类型定义

```py

@dataclass
class LLMResponse:
    role: str
    """角色, assistant, tool, err"""
    result_chain: MessageChain = None
    """返回的消息链"""
    tools_call_args: List[Dict[str, any]] = field(default_factory=list)
    """工具调用参数"""
    tools_call_name: List[str] = field(default_factory=list)
    """工具调用名称"""
    tools_call_ids: List[str] = field(default_factory=list)
    """工具调用 ID"""

    raw_completion: ChatCompletion = None
    _new_record: Dict[str, any] = None

    _completion_text: str = ""

    is_chunk: bool = False
    """是否是流式输出的单个 Chunk"""

    def __init__(
        self,
        role: str,
        completion_text: str = "",
        result_chain: MessageChain = None,
        tools_call_args: List[Dict[str, any]] = None,
        tools_call_name: List[str] = None,
        tools_call_ids: List[str] = None,
        raw_completion: ChatCompletion = None,
        _new_record: Dict[str, any] = None,
        is_chunk: bool = False,
    ):
        """初始化 LLMResponse

        Args:
            role (str): 角色, assistant, tool, err
            completion_text (str, optional): 返回的结果文本，已经过时，推荐使用 result_chain. Defaults to "".
            result_chain (MessageChain, optional): 返回的消息链. Defaults to None.
            tools_call_args (List[Dict[str, any]], optional): 工具调用参数. Defaults to None.
            tools_call_name (List[str], optional): 工具调用名称. Defaults to None.
            raw_completion (ChatCompletion, optional): 原始响应, OpenAI 格式. Defaults to None.
        """
        if tools_call_args is None:
            tools_call_args = []
        if tools_call_name is None:
            tools_call_name = []
        if tools_call_ids is None:
            tools_call_ids = []

        self.role = role
        self.completion_text = completion_text
        self.result_chain = result_chain
        self.tools_call_args = tools_call_args
        self.tools_call_name = tools_call_name
        self.tools_call_ids = tools_call_ids
        self.raw_completion = raw_completion
        self._new_record = _new_record
        self.is_chunk = is_chunk

    @property
    def completion_text(self):
        if self.result_chain:
            return self.result_chain.get_plain_text()
        return self._completion_text

    @completion_text.setter
    def completion_text(self, value):
        if self.result_chain:
            self.result_chain.chain = [
                comp
                for comp in self.result_chain.chain
                if not isinstance(comp, Comp.Plain)
            ]  # 清空 Plain 组件
            self.result_chain.chain.insert(0, Comp.Plain(value))
        else:
            self._completion_text = value

    def to_openai_tool_calls(self) -> List[Dict]:
        """将工具调用信息转换为 OpenAI 格式"""
        ret = []
        for idx, tool_call_arg in enumerate(self.tools_call_args):
            ret.append(
                {
                    "id": self.tools_call_ids[idx],
                    "function": {
                        "name": self.tools_call_name[idx],
                        "arguments": json.dumps(tool_call_arg),
                    },
                    "type": "function",
                }
            )
        return ret
```

:::

##### 获取其他类型的提供商

> 嵌入、重排序 没有 “当前使用”。这两个提供商主要用于知识库。

- 获取当前使用的语音识别提供商(STTProvider): `self.context.get_using_stt_provider(umo=event.unified_msg_origin)`。
- 获取当前使用的语音合成提供商(TTSProvider): `self.context.get_using_tts_provider(umo=event.unified_msg_origin)`。
- 获取所有语音识别提供商: `self.context.get_all_stt_providers()`。
- 获取所有语音合成提供商: `self.context.get_all_tts_providers()`。
- 获取所有嵌入提供商: `self.context.get_all_embedding_providers()`。

::: details STTProvider / TTSProvider / EmbeddingProvider 类型定义

```py
class TTSProvider(AbstractProvider):
    def __init__(self, provider_config: dict, provider_settings: dict) -> None:
        super().__init__(provider_config)
        self.provider_config = provider_config
        self.provider_settings = provider_settings

    @abc.abstractmethod
    async def get_audio(self, text: str) -> str:
        """获取文本的音频，返回音频文件路径"""
        raise NotImplementedError()


class EmbeddingProvider(AbstractProvider):
    def __init__(self, provider_config: dict, provider_settings: dict) -> None:
        super().__init__(provider_config)
        self.provider_config = provider_config
        self.provider_settings = provider_settings

    @abc.abstractmethod
    async def get_embedding(self, text: str) -> list[float]:
        """获取文本的向量"""
        ...

    @abc.abstractmethod
    async def get_embeddings(self, text: list[str]) -> list[list[float]]:
        """批量获取文本的向量"""
        ...

    @abc.abstractmethod
    def get_dim(self) -> int:
        """获取向量的维度"""
        ...

class STTProvider(AbstractProvider):
    def __init__(self, provider_config: dict, provider_settings: dict) -> None:
        super().__init__(provider_config)
        self.provider_config = provider_config
        self.provider_settings = provider_settings

    @abc.abstractmethod
    async def get_text(self, audio_url: str) -> str:
        """获取音频的文本"""
        raise NotImplementedError()
```

:::

##### 函数工具

函数工具给了大语言模型调用外部工具的能力。在 AstrBot 中，函数工具有多种定义方式。

###### 以类的形式（推荐）

推荐在插件目录下新建 `tools` 文件夹，然后在其中编写工具类：

`tools/search.py`:

```py
from astrbot.api import FunctionTool
from astrbot.api.event import AstrMessageEvent
from dataclasses import dataclass, field

@dataclass
class HelloWorldTool(FunctionTool):
    name: str = "hello_world" # 工具名称
    description: str = "Say hello to the world." # 工具描述
    parameters: dict = field(
        default_factory=lambda: {
            "type": "object",
            "properties": {
                "greeting": {
                    "type": "string",
                    "description": "The greeting message.",
                },
            },
            "required": ["greeting"],
        }
    ) # 工具参数定义，见 OpenAI 官网或 https://json-schema.org/understanding-json-schema/

    async def run(
        self,
        event: AstrMessageEvent, # 必须包含此 event 参数在前面，用于获取上下文
        greeting: str, # 工具参数，必须与 parameters 中定义的参数名一致
    ):
        return f"{greeting}, World!" # 也支持 mcp.types.CallToolResult 类型
```

要将上述工具注册到 AstrBot，可以在插件主文件的 `__init__.py` 中添加以下代码：

```py
from .tools.search import SearchTool

class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # >= v4.5.1 使用：
        self.context.add_llm_tools(HelloWorldTool(), SecondTool(), ...)

        # < v4.5.1 之前使用：
        tool_mgr = self.context.provider_manager.llm_tools
        tool_mgr.func_list.append(HelloWorldTool())
```

###### 以装饰器的形式

这个形式定义的工具函数会被自动加载到 AstrBot Core 中，在 Core 请求大模型时会被自动带上。

请务必按照以下格式编写一个工具（包括**函数注释**，AstrBot 会解析该函数注释，请务必将注释格式写对）

```py{3,4,5,6,7}
@filter.llm_tool(name="get_weather") # 如果 name 不填，将使用函数名
async def get_weather(self, event: AstrMessageEvent, location: str) -> MessageEventResult:
    '''获取天气信息。

    Args:
        location(string): 地点
    '''
    resp = self.get_weather_from_api(location)
    yield event.plain_result("天气信息: " + resp)
```

在 `location(string): 地点` 中，`location` 是参数名，`string` 是参数类型，`地点` 是参数描述。

支持的参数类型有 `string`, `number`, `object`, `boolean`。

> [!NOTE]
> 对于装饰器注册的 llm_tool，如果需要调用 Provider.text_chat()，func_tool（ToolSet 类型） 可以通过以下方式获取：
>
> ```py
> func_tool = self.context.get_llm_tool_manager() # 获取 AstrBot 的 LLM Tool Manager，包含了所有插件和 MCP 注册的 Tool
> tool = func_tool.get_func("xxx")
> if tool:
>     tool_set = ToolSet()
>     tool_set.add_tool(tool)
> ```

##### 对话管理器 ConversationManager

**获取会话当前的 LLM 对话历史**

```py
from astrbot.core.conversation_mgr import Conversation

uid = event.unified_msg_origin
conv_mgr = self.context.conversation_manager
curr_cid = await conv_mgr.get_curr_conversation_id(uid)
conversation = await conv_mgr.get_conversation(uid, curr_cid)  # Conversation
```

::: details Conversation 类型定义

```py
@dataclass
class Conversation:
    """LLM 对话类

    对于 WebChat，history 存储了包括指令、回复、图片等在内的所有消息。
    对于其他平台的聊天，不存储非 LLM 的回复（因为考虑到已经存储在各自的平台上）。

    在 v4.0.0 版本及之后，WebChat 的历史记录被迁移至 `PlatformMessageHistory` 表中，
    """

    platform_id: str
    user_id: str
    cid: str
    """对话 ID, 是 uuid 格式的字符串"""
    history: str = ""
    """字符串格式的对话列表。"""
    title: str | None = ""
    persona_id: str | None = ""
    """对话当前使用的人格 ID"""
    created_at: int = 0
    updated_at: int = 0
```

:::

**所有方法**

###### `new_conversation`

- **Usage**  
  在当前会话中新建一条对话，并自动切换为该对话。
- **Arguments**  
  - `unified_msg_origin: str` – 形如 `platform_name:message_type:session_id`  
  - `platform_id: str | None` – 平台标识，默认从 `unified_msg_origin` 解析  
  - `content: list[dict] | None` – 初始历史消息  
  - `title: str | None` – 对话标题  
  - `persona_id: str | None` – 绑定的 persona ID
- **Returns**  
  `str` – 新生成的 UUID 对话 ID

###### `switch_conversation`

- **Usage**  
  将会话切换到指定的对话。
- **Arguments**  
  - `unified_msg_origin: str`  
  - `conversation_id: str`
- **Returns**  
  `None`

###### `delete_conversation`

- **Usage**  
  删除会话中的某条对话；若 `conversation_id` 为 `None`，则删除当前对话。
- **Arguments**  
  - `unified_msg_origin: str`  
  - `conversation_id: str | None`
- **Returns**  
  `None`

###### `get_curr_conversation_id`

- **Usage**  
  获取当前会话正在使用的对话 ID。
- **Arguments**  
  - `unified_msg_origin: str`
- **Returns**  
  `str | None` – 当前对话 ID，不存在时返回 `None`

###### `get_conversation`

- **Usage**  
  获取指定对话的完整对象；若不存在且 `create_if_not_exists=True` 则自动创建。
- **Arguments**  
  - `unified_msg_origin: str`  
  - `conversation_id: str`  
  - `create_if_not_exists: bool = False`
- **Returns**  
  `Conversation | None`

###### `get_conversations`

- **Usage**  
  拉取用户或平台下的全部对话列表。
- **Arguments**  
  - `unified_msg_origin: str | None` – 为 `None` 时不过滤用户  
  - `platform_id: str | None`
- **Returns**  
  `List[Conversation]`

###### `get_filtered_conversations`

- **Usage**  
  分页 + 关键词搜索对话。
- **Arguments**  
  - `page: int = 1`  
  - `page_size: int = 20`  
  - `platform_ids: list[str] | None`  
  - `search_query: str = ""`  
  - `**kwargs` – 透传其他过滤条件
- **Returns**  
  `tuple[list[Conversation], int]` – 对话列表与总数

###### `update_conversation`

- **Usage**  
  更新对话的标题、历史记录或 persona_id。
- **Arguments**  
  - `unified_msg_origin: str`  
  - `conversation_id: str | None` – 为 `None` 时使用当前对话  
  - `history: list[dict] | None`  
  - `title: str | None`  
  - `persona_id: str | None`
- **Returns**  
  `None`

###### `get_human_readable_context`

- **Usage**  
  生成分页后的人类可读对话上下文，方便展示或调试。
- **Arguments**  
  - `unified_msg_origin: str`  
  - `conversation_id: str`  
  - `page: int = 1`  
  - `page_size: int = 10`
- **Returns**  
  `tuple[list[str], int]` – 当前页文本列表与总页数

```py
import json

context = json.loads(conversation.history)
```

##### 人格设定管理器 PersonaManager

`PersonaManager` 负责统一加载、缓存并提供所有人格（Persona）的增删改查接口，同时兼容 AstrBot 4.x 之前的旧版人格格式（v3）。  
初始化时会自动从数据库读取全部人格，并生成一份 v3 兼容数据，供旧代码无缝使用。

```py
persona_mgr = self.context.persona_manager
```

###### `get_persona`

- **Usage**
  获取根据人格 ID 获取人格数据。
- **Arguments**
  - `persona_id: str` – 人格 ID
- **Returns**
  `Persona` – 人格数据，若不存在则返回 None
- **Raises**
  `ValueError` – 当不存在时抛出

###### `get_all_personas`

- **Usage**  
  一次性获取数据库中所有人格。
- **Returns**  
  `list[Persona]` – 人格列表，可能为空

###### `create_persona`

- **Usage**  
  新建人格并立即写入数据库，成功后自动刷新本地缓存。
- **Arguments**  
  - `persona_id: str` – 新人格 ID（唯一）  
  - `system_prompt: str` – 系统提示词  
  - `begin_dialogs: list[str]` – 可选，开场对话（偶数条，user/assistant 交替）  
  - `tools: list[str]` – 可选，允许使用的工具列表；`None`=全部工具，`[]`=禁用全部
- **Returns**  
  `Persona` – 新建后的人格对象
- **Raises**  
  `ValueError` – 若 `persona_id` 已存在

###### `update_persona`

- **Usage**  
  更新现有人格的任意字段，并同步到数据库与缓存。
- **Arguments**  
  - `persona_id: str` – 待更新的人格 ID  
  - `system_prompt: str` – 可选，新的系统提示词  
  - `begin_dialogs: list[str]` – 可选，新的开场对话  
  - `tools: list[str]` – 可选，新的工具列表；语义同 `create_persona`
- **Returns**  
  `Persona` – 更新后的人格对象
- **Raises**  
  `ValueError` – 若 `persona_id` 不存在

###### `delete_persona`

- **Usage**  
  删除指定人格，同时清理数据库与缓存。
- **Arguments**  
  - `persona_id: str` – 待删除的人格 ID
- **Raises**  
  `Valueable` – 若 `persona_id` 不存在

###### `get_default_persona_v3`

- **Usage**  
  根据当前会话配置，获取应使用的默认人格（v3 格式）。  
  若配置未指定或指定的人格不存在，则回退到 `DEFAULT_PERSONALITY`。
- **Arguments**  
  - `umo: str | MessageSession | None` – 会话标识，用于读取用户级配置
- **Returns**  
  `Personality` – v3 格式的默认人格对象

::: details Persona / Personality 类型定义

```py

class Persona(SQLModel, table=True):
    """Persona is a set of instructions for LLMs to follow.

    It can be used to customize the behavior of LLMs.
    """

    __tablename__ = "personas"

    id: int = Field(primary_key=True, sa_column_kwargs={"autoincrement": True})
    persona_id: str = Field(max_length=255, nullable=False)
    system_prompt: str = Field(sa_type=Text, nullable=False)
    begin_dialogs: Optional[list] = Field(default=None, sa_type=JSON)
    """a list of strings, each representing a dialog to start with"""
    tools: Optional[list] = Field(default=None, sa_type=JSON)
    """None means use ALL tools for default, empty list means no tools, otherwise a list of tool names."""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc)},
    )

    __table_args__ = (
        UniqueConstraint(
            "persona_id",
            name="uix_persona_id",
        ),
    )


class Personality(TypedDict):
    """LLM 人格类。

    在 v4.0.0 版本及之后，推荐使用上面的 Persona 类。并且， mood_imitation_dialogs 字段已被废弃。
    """

    prompt: str
    name: str
    begin_dialogs: list[str]
    mood_imitation_dialogs: list[str]
    """情感模拟对话预设。在 v4.0.0 版本及之后，已被废弃。"""
    tools: list[str] | None
    """工具列表。None 表示使用所有工具，空列表表示不使用任何工具"""
```

:::

#### 其他

##### 配置文件

###### 默认配置文件

```py
config = self.context.get_config()
```

不建议修改默认配置文件，建议只读取。

###### 会话配置文件

v4.0.0 后，AstrBot 支持会话粒度的多配置文件。

```py
umo = event.unified_msg_origin
config = self.context.get_config(umo=umo)
```

##### 获取消息平台实例

> v3.4.34 后

```python
from astrbot.api.event import filter, AstrMessageEvent

@filter.command("test")
async def test_(self, event: AstrMessageEvent):
    from astrbot.api.platform import AiocqhttpAdapter # 其他平台同理
    platform = self.context.get_platform(filter.PlatformAdapterType.AIOCQHTTP)
    assert isinstance(platform, AiocqhttpAdapter)
    # platform.get_client().api.call_action()
```

##### 调用 QQ 协议端 API

```py
@filter.command("helloworld")
async def helloworld(self, event: AstrMessageEvent):
    if event.get_platform_name() == "aiocqhttp":
        # qq
        from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
        assert isinstance(event, AiocqhttpMessageEvent)
        client = event.bot # 得到 client
        payloads = {
            "message_id": event.message_obj.message_id,
        }
        ret = await client.api.call_action('delete_msg', **payloads) # 调用 协议端  API
        logger.info(f"delete_msg: {ret}")
```

关于 CQHTTP API，请参考如下文档：

Napcat API 文档：<https://napcat.apifox.cn/>

Lagrange API 文档：<https://lagrange-onebot.apifox.cn/>

##### 载入的所有插件

```py
plugins = self.context.get_all_stars() # 返回 StarMetadata 包含了插件类实例、配置等等
```

##### 注册一个异步任务

直接在 **init**() 中使用 `asyncio.create_task()` 即可。

```py
import asyncio

@register("task", "Soulter", "一个异步任务示例", "1.0.0")
class TaskPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        asyncio.create_task(self.my_task())

    async def my_task(self):
        await asyncio.sleep(1)
        print("Hello")
```

##### 获取加载的所有平台

```py
from astrbot.api.platform import Platform
platforms = self.context.platform_manager.get_insts() # List[Platform]
```

## 开发一个平台适配器

来源: https://docs.astrbot.app/dev/plugin-platform-adapter.html

AstrBot 支持以插件的形式接入平台适配器，你可以自行接入 AstrBot 没有的平台。如飞书、钉钉甚至是哔哩哔哩私信、Minecraft。

我们以一个平台 `FakePlatform` 为例展开讲解。

首先，在插件目录下新增 `fake_platform_adapter.py` 和 `fake_platform_event.py` 文件。前者主要是平台适配器的实现，后者是平台事件的定义。

### 平台适配器

假设 FakePlatform 的客户端 SDK 是这样：

```py
import asyncio

class FakeClient():
    '''模拟一个消息平台，这里 5 秒钟下发一个消息'''
    def __init__(self, token: str, username: str):
        self.token = token
        self.username = username
        # ...
                
    async def start_polling(self):
        while True:
            await asyncio.sleep(5)
            await getattr(self, 'on_message_received')({
                'bot_id': '123',
                'content': '新消息',
                'username': 'zhangsan',
                'userid': '123',
                'message_id': 'asdhoashd',
                'group_id': 'group123',
            })
            
    async def send_text(self, to: str, message: str):
        print('发了消息:', to, message)
        
    async def send_image(self, to: str, image_path: str):
        print('发了消息:', to, image_path)
```

我们创建  `fake_platform_adapter.py`：

```py
import asyncio

from astrbot.api.platform import Platform, AstrBotMessage, MessageMember, PlatformMetadata, MessageType
from astrbot.api.event import MessageChain
from astrbot.api.message_components import Plain, Image, Record # 消息链中的组件，可以根据需要导入
from astrbot.core.platform.astr_message_event import MessageSesion
from astrbot.api.platform import register_platform_adapter
from astrbot import logger
from .client import FakeClient
from .fake_platform_event import FakePlatformEvent
            
# 注册平台适配器。第一个参数为平台名，第二个为描述。第三个为默认配置。
@register_platform_adapter("fake", "fake 适配器", default_config_tmpl={
    "token": "your_token",
    "username": "bot_username"
})
class FakePlatformAdapter(Platform):

    def __init__(self, platform_config: dict, platform_settings: dict, event_queue: asyncio.Queue) -> None:
        super().__init__(event_queue)
        self.config = platform_config # 上面的默认配置，用户填写后会传到这里
        self.settings = platform_settings # platform_settings 平台设置。
    
    async def send_by_session(self, session: MessageSesion, message_chain: MessageChain):
        # 必须实现
        await super().send_by_session(session, message_chain)
    
    def meta(self) -> PlatformMetadata:
        # 必须实现，直接像下面一样返回即可。
        return PlatformMetadata(
            "fake",
            "fake 适配器",
        )

    async def run(self):
        # 必须实现，这里是主要逻辑。

        # FakeClient 是我们自己定义的，这里只是示例。这个是其回调函数
        async def on_received(data):
            logger.info(data)
            abm = await self.convert_message(data=data) # 转换成 AstrBotMessage
            await self.handle_msg(abm) 
        
        # 初始化 FakeClient
        self.client = FakeClient(self.config['token'], self.config['username'])
        self.client.on_message_received = on_received
        await self.client.start_polling() # 持续监听消息，这是个堵塞方法。

    async def convert_message(self, data: dict) -> AstrBotMessage:
        # 将平台消息转换成 AstrBotMessage
        # 这里就体现了适配程度，不同平台的消息结构不一样，这里需要根据实际情况进行转换。
        abm = AstrBotMessage()
        abm.type = MessageType.GROUP_MESSAGE # 还有 friend_message，对应私聊。具体平台具体分析。重要！
        abm.group_id = data['group_id'] # 如果是私聊，这里可以不填
        abm.message_str = data['content'] # 纯文本消息。重要！
        abm.sender = MessageMember(user_id=data['userid'], nickname=data['username']) # 发送者。重要！
        abm.message = [Plain(text=data['content'])] # 消息链。如果有其他类型的消息，直接 append 即可。重要！
        abm.raw_message = data # 原始消息。
        abm.self_id = data['bot_id']
        abm.session_id = data['userid'] # 会话 ID。重要！
        abm.message_id = data['message_id'] # 消息 ID。
        
        return abm
    
    async def handle_msg(self, message: AstrBotMessage):
        # 处理消息
        message_event = FakePlatformEvent(
            message_str=message.message_str,
            message_obj=message,
            platform_meta=self.meta(),
            session_id=message.session_id,
            client=self.client
        )
        self.commit_event(message_event) # 提交事件到事件队列。不要忘记！
```


`fake_platform_event.py`：

```py
from astrbot.api.event import AstrMessageEvent, MessageChain
from astrbot.api.platform import AstrBotMessage, PlatformMetadata
from astrbot.api.message_components import Plain, Image
from .client import FakeClient
from astrbot.core.utils.io import download_image_by_url

class FakePlatformEvent(AstrMessageEvent):
    def __init__(self, message_str: str, message_obj: AstrBotMessage, platform_meta: PlatformMetadata, session_id: str, client: FakeClient):
        super().__init__(message_str, message_obj, platform_meta, session_id)
        self.client = client
        
    async def send(self, message: MessageChain):
        for i in message.chain: # 遍历消息链
            if isinstance(i, Plain): # 如果是文字类型的
                await self.client.send_text(to=self.get_sender_id(), message=i.text)
            elif isinstance(i, Image): # 如果是图片类型的 
                img_url = i.file
                img_path = ""
                # 下面的三个条件可以直接参考一下。
                if img_url.startswith("file:///"):
                    img_path = img_url[8:]
                elif i.file and i.file.startswith("http"):
                    img_path = await download_image_by_url(i.file)
                else:
                    img_path = img_url

                # 请善于 Debug！
                    
                await self.client.send_image(to=self.get_sender_id(), image_path=img_path)

        await super().send(message) # 需要最后加上这一段，执行父类的 send 方法。
```

最后，main.py 只需这样，在初始化的时候导入 fake_platform_adapter 模块。装饰器会自动注册。

```py
from astrbot.api.star import Context, Star, register
@register("helloworld", "Your Name", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        from .fake_platform_adapter import FakePlatformAdapter # noqa
```

搞好后，运行 AstrBot：

![image](/source/images/plugin-platform-adapter/QQ_1738155926221.png)

这里出现了我们创建的 fake。

![image](/source/images/plugin-platform-adapter/QQ_1738155982211.png)

启动后，可以看到正常工作：

![image](/source/images/plugin-platform-adapter/QQ_1738156166893.png)


有任何疑问欢迎加群询问~
