# shiyiagi-facial-expression

一句话：把「表情管理」从一句口号，固化成可量化、可复制的提示词编码系统。

专治 AI 人物生成的三类翻车：面瘫（无表情）、表情瞬变（跨镜头断裂）、形容词废词（「微笑 / 悲伤」模型读不懂）。

## 它解决什么

| 翻车 | 根因 | 本 skill 的解法 |
|---|---|---|
| 面瘫 / 脸僵 | 只写情绪词，模型读不懂 | 换成「肌肉动作 + 可数强度」的编码 |
| 表情瞬变（帧间跳变） | 没给动态过程 | onset → apex → offset 三阶段，相邻差 >3 拆镜 |
| 橡皮脸（强度高但脸僵） | 无肌肉证据 | I≥8 必须有辅助证据（咬肌 / 鼻唇沟 / 青筋 / 泪） |
| 假笑（只动嘴不动眼） | 只写了颧大肌 | 颧大肌 + 眼轮匝肌同写（杜乡微笑） |
| 跨镜头表情断裂 | 无基线、无锚点图 | 表情基线卡 + 锚点图垫图 + 固定描述段 |

## 核心判断

> **表情不是形容词，是「可数的值 + 可看的肌肉动作」。**

## 编码体系（七个维度）

| 维度 | 内容 |
|---|---|
| 表情轮 | 8 基础态 + 细分态 + 复合态（同写两组肌肉）+ 微表情级 |
| 强度档 I | 0–10，每档附**可见标志**（不只写数字） |
| 肌肉分区 | 上脸（额/眉/眼周）+ 下脸（嘴/下颌）+ 鼻颈，写部位动作不写情绪词 |
| 眼神 | 直视 / 看某点 / 垂视 / 游离 / 瞪 / 眯视（含瞳孔缩放） |
| 动态三阶段 | onset(≈30%) → apex(≥0.5–1s) → offset(≈30%) |
| 景别光位耦合 | 微表情只特写可见；侧光/顶光/底光/柔光匹配情绪 |
| 引擎适配 | 即梦 Seedance / 可灵 Kling / 豆包 Seedream / Grok，各带写法与 negative prompt |

## 交付物

- 角色表情基线卡（每角色一张）
- 逐镜表情编码 + 可直接复制的提示词
- 跨镜头一致性方案（锚点图垫图 + 固定描述段）
- 表情资产哈希登记（出"表情参考图组"时，用 `scripts/asset_hash.py` 锁死参考图指纹，防偷换 / 损坏）

## 目录结构

```text
shiyiagi-facial-expression/
├── SKILL.md
├── scripts/
│   └── asset_hash.py             # 表情资产哈希登记/比对（防参考图被偷换/损坏）
└── references/
    ├── expression-coding.md      # 完整编码体系 + 四要素正文 + 速查表 + 合格判定 8 项
    ├── smoke-expression-grief.md # 端到端示例（林夏悲伤 I3→I7 跨 3 镜）
    └── asset-hash.md             # 表情资产哈希登记与比对说明
```

## 怎么用

**安装**

```bash
npx -y skills add shiyi-TNT-SOS/shiyiagi-facial-expression -g --all
```

或把整个目录复制到你的 Agent 技能目录（豆包为 `...\.doubao\agent_mode\workspace\.user_skills\`）。

**流程**：填表情基线卡 → 选表情轮类型 + 强度 I → 写具体肌肉动作（非情绪词）→ 拆 onset/apex/offset → 套引擎与 negative prompt → 跨镜头用锚点图垫图保脸不变 → 过「合格判定 8 项」。

## 适用 / 不适用

**适用**：控制 AI 视频 / 图像人物的面部表情、微表情、表情渐变；出角色表情参考图组；为即梦 / 可灵 / Seedream / Grok 写表情提示词。

**不适用**：纯动作戏打斗设计（走 `shiyiagi-director-action`）；广告 / 故事分镜结构（走 `shiyiagi-director-ad-tvc` / `-film`）。本 skill 只解决「面部表情」这一层。

## 依赖与协作

- 角色档案与锚点图：`shiyi-agi-ip-character-studio`
- 跨镜头脸 / 景 / 道具一致的总控：`shiyiagi-character-scene-consistency`

分工是 **表情编码负责「变」、锚点图负责「稳」**——换表情不变脸。

## 版本与授权

- 版本：`1.1.0`
- 授权：MIT（见 SKILL.md frontmatter）。学习与**非商业**用途可自由使用；商用请先联系作者授权。
- 作者：柳十一（十一AGI认知圈）

## 系列导航

| Skill | 定位 | 仓库 |
|---|---|---|
| shiyiagi-director-action | 武打 / 格斗 / 动作戏 | [shiyiagi-director-action](https://github.com/shiyi-TNT-SOS/shiyiagi-director-action) |
| shiyiagi-director-ad-tvc | 品牌广告片 / TVC | [shiyiagi-director-ad-tvc](https://github.com/shiyi-TNT-SOS/shiyiagi-director-ad-tvc) |
| shiyiagi-director-film | 故事片 / 叙事短片 | [shiyiagi-director-film](https://github.com/shiyi-TNT-SOS/shiyiagi-director-film) |
| shiyiagi-director-story-selling | 剧情化带货短视频 | [shiyiagi-director-story-selling](https://github.com/shiyi-TNT-SOS/shiyiagi-director-story-selling) |
| **shiyiagi-facial-expression** | **面部表情量化编码** | **本仓库** |
| shiyiagi-character-scene-consistency | 角色 / 场景跨镜头一致性（总控层） | [shiyiagi-character-scene-consistency](https://github.com/shiyi-TNT-SOS/shiyiagi-character-scene-consistency) |
