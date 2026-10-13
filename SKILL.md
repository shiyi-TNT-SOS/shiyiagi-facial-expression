---
name: shiyiagi-facial-expression
description: "十一AGI 专属面部表情编码技能。当用户需要为 AI 视频/图像生成的人物精确控制面部表情——包括把「微笑/悲伤」等不可生成词转化为可量化的表情编码（表情类型+强度档+肌肉动作+眼神+动态阶段）、保证跨镜头表情一致、设计表情渐变与微表情、或为即梦/可灵/Seedream/Grok 等引擎适配提示词时使用。触发词：表情管理、表情编码、面部表情、微表情、表情一致性、表情参考图、expression coding。"
agent_created: true
license: MIT
user-invocable: true
tags: [facial-expression, shiyiagi, 十一AGI, 表情管理, 表情编码]
metadata:
  version: "1.0.0"
  brand: "十一AGI认知圈"
  owner: "爸爸"
---

# 十一AGI 面部表情编码

把「表情管理」从一句口号，固化成可量化、可复制的提示词编码系统。专治 AI 人物生成的三类翻车：面瘫（无表情）、表情瞬变（跨镜头断裂）、形容词废词（「微笑/悲伤」模型读不懂）。

## Overview

核心判断：**表情不是形容词，是「可数的值 + 可看的肌肉动作」。** 本技能提供一套完整编码体系——表情轮、强度档 I(0–10)、FACS 思路的肌肉分区、眼神焦距、动态三阶段（onset/apex/offset）、跨镜头一致性、引擎适配与 negative prompt——让每一帧表情都可被精确指定、跨镜头保持一致、可平滑演变。

## When to Use

- 用户要控制 AI 视频 / 图像人物的面部表情、微表情、表情渐变
- 用户抱怨「表情不对」「脸僵」「表情跳变」「微表情看不出」
- 用户要出「角色表情参考图组」（配合 IP 角色一致性工作室）
- 用户要为即梦 / Seedance、可灵 / Kling、豆包 / Seedream、Grok 写表情提示词

**不适用**：纯动作戏打斗设计（走 shiyiagi-director-action）、广告 / 故事分镜结构（走 shiyiagi-director-ad-tvc / -film）。本技能只解决「面部表情」这一层。

## How to Use

1. 读取 [references/expression-coding.md](references/expression-coding.md) 获取完整编码体系与可直接复制的提示词模板。
2. 按以下流程产出：
   - 确定角色表情基线（填「角色表情基线卡模板」）
   - 选定表情轮类型 + 强度档 I，写出具体肌肉动作（非情绪词）
   - 视频场景拆 onset / apex / offset 三阶段，相邻差 >3 档插过渡镜
   - 选引擎并套用对应 negative prompt（见第五节）
   - 跨镜头用锚点图垫图 + 固定描述段保证脸不变（见第六节）
3. 用「合格判定标准」（第十节）逐项核对，一处不满足即退回修改。

## Resources

- `references/expression-coding.md` — 完整提示词指令：四要素正文（可直接复制给 AI）+ 表情编码速查表 + 翻车↔正写对照 + 引擎适配与 negative prompt + 与参考图垫图协同 + 强度↔时长换算表 + 生理细节元件 + 补充示例（喜悦/惊讶/恐惧）+ 合格判定标准（8 项）
