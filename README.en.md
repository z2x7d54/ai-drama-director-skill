# AI Short Drama Director Skill 8.0

[简体中文](README.md) | **English**

Turn scripts into production-ready storyboards for generating short dramas one multi-shot segment at a time. Designed for agents such as ChatGPT and DeepSeek, this skill explains character positions, emotional performance, meaningful cuts, and continuity between generation segments.

Author: **mr zhu**. Version: **8.0**.

## What this skill does

| Feature | What it helps you do |
| --- | --- |
| Script-to-storyboard planning | Cover the requested episodes, preserve original dialogue and story events, and distinguish source facts from directorial additions and unresolved information. |
| Spatial staging and camera placement | Specify doors, windows, furniture, character positions, facing directions, eyelines, action axes, and movement paths so new angles remain part of the same scene. |
| Shot and segment continuity | Carry forward action phases, physical contact, hand and prop states, sound, and unfinished exchanges without restarting the performance at each cut. |
| Dialogue delivery and acting details | Describe meaningful emphasis, pauses, pace, facial changes, small gestures, and the other character's response to reduce flat line readings and static performances. |
| Editing and pacing | Choose cuts around new information and emotional changes, using reaction shots, sound bridges, and varied shot lengths instead of a fixed five-second rhythm. |
| Multi-shot generation prompts | Organize independently usable segments with cast, scene and prop references, shot instructions, and continuity handoffs. Each segment has an integer duration of 1–30 seconds. |
| Ensemble staging | Track identity separately from position, identify who speaks to whom, set priorities and exit order, and check eyelines, unexplained position changes, and identity consistency. |
| Content review before production | Check applicable review requirements and potential issues before creating or revising a storyboard, then apply the findings to the visual plan. |
| Storyboard review and revision | Check source fidelity, spatial logic, acting, continuity, and timing sums. Use the standalone checklist to revisit a storyboard after a long conversation. |
| Illustrated instruction | Learn from 17 diagrams, fictional examples with explicit premises, and complete storyboard demonstrations without needing access to reference videos. |

Typical workflow: **Script + Skill → agent-written storyboard → one segment per generation request in Seed2.5 or a similar video tool → editing and review of the finished footage**.

## Start here

- **Complete single-file skill:** [ai短剧导演skill-8.0版.md](ai短剧导演skill-8.0版.md), containing the main rules and three full teaching appendices.
- **Download with illustrations:** [Complete illustrated ZIP](AI短剧导演skill_8.0_图文完整版.zip). Keep the folder structure after extraction so relative image links work.
- **Startup instructions:** [8.0启动指令.txt](8.0启动指令.txt). Send these with the skill and script, specifying the episodes and production constraints.
- **Review an existing storyboard:** [Standalone self-check system](分镜自检系统_8.0独立版.md).
- **Native skill entry:** [ai-drama-director-storyboard/SKILL.md](ai-drama-director-storyboard/SKILL.md). This directory includes the entry file, teaching references, 17 diagrams, and agent interface metadata.
- **Changes and validation scope:** [8.0升级说明与验证记录.md](8.0升级说明与验证记录.md).

This page provides an English introduction. The skill instructions, teaching materials, and startup files linked above are in Chinese.

## How to use it

1. Give the agent the complete skill and script. Specify the episodes, completed production work, and available character, scene, and prop assets.
2. Ask the agent to read and apply the skill, including the content review in section 0.4 before writing the storyboard.
3. Send each complete multi-shot segment to your video generation tool. Review the generated footage before editing and final delivery.

Example request:

> Read the complete AI Short Drama Director Skill 8.0 and the supplied script, then storyboard the episodes I specify. First perform the content review in section 0.4. Preserve the original dialogue and story events. Specify character positions, hand and prop states, dialogue delivery, cuts, and continuity between segments. Every multi-shot generation segment must have an integer total duration from 1 to 30 seconds, inclusive. Individual shot durations and cut points may use decimals, but their sum must exactly equal the segment total. Check the result against the skill and deliver a complete TXT storyboard.

## Key rules

- Understand the whole exchange before planning individual shots. Fix the scene layout, character positions, and movement paths; carry the same event state into each new angle.
- Give dialogue a clear intention, with relevant emphasis, expressions or gestures, and a response from its recipient.
- Let the content determine pacing and shot count. There is no universal five-second shot length, fixed episode duration, or required number of generation segments.
- **Every generation segment must total an integer number of seconds from 1 to 30, inclusive.** Shorter segments are valid. Shot durations must sum exactly to the header total; rounding only the header is insufficient.
- Make each segment independently usable, with the necessary character, prop, sound, knowledge, and unfinished-exchange states. Do not treat the previous segment's final frame as the only reference for every new camera angle.
- In ensemble scenes, retain necessary relationship shots and reduce simultaneous actions or visible faces when they serve no purpose. Track identity and position separately.
- Complete the content review before every new storyboard or revision, and verify that its findings are reflected in the result before delivery.

## Files and illustrations

The complete Markdown file contains the full written explanation. Whether local relative images display depends on the receiving platform. For the illustrated version, provide the ZIP or the accompanying image directory.

This repository contains the skill, fictional teaching examples, and explanatory diagrams. It does not include production scripts, novels, finished videos, or local credentials. Planned timings and document checks do not establish video-model performance or guarantee platform approval.
