# AI Drama Director Skill · AI短剧导演 Skill

[Version index](https://github.com/z2x7d54/ai-drama-director-skill) · [8.0](../8.0/) · [8.1](../8.1/) · [8.2](../8.2/)

**Version 8.1 · Author: mr zhu · [中文](README.md)**

Turn a script into concise storyboard prompts for generating one multi-shot clip per group. Version 8.1 teaches two core abilities: **keeping characters in one coherent space and continuing actions across cuts.** It is a self-contained illustrated course with worked examples, followed by practical checks.

## Choose a file

- **For ChatGPT, DeepSeek, or another storyboard-writing agent:** [Complete 8.1 skill](ai短剧导演skill-8.1版.md). The Chinese-language Markdown includes the course, examples, output format, and review process.
- **For reading on a phone or computer:** [PDF with embedded images](AI短剧导演skill_8.1_跨设备阅读版.pdf), or download the [standalone offline HTML](AI短剧导演skill_8.1_离线图文阅读版.html) and open it in a browser.
- **For offline storage:** [Illustrated ZIP](AI短剧导演skill_8.1_图文完整版.zip). Keep the extracted image folders.
- **For native skill installation:** [ai-drama-director-storyboard/SKILL.md](ai-drama-director-storyboard/SKILL.md), together with its assets.
- **For reviewing a storyboard after a long conversation:** [Standalone review instructions](分镜自检系统_8.1独立版.md). These complement the complete course.

## What the course teaches

1. **Direct an event before choosing shots.** Work out the source events, dialogue, action, and viewer expectations, then choose coverage and cut points.
2. **Build repeatable spatial relationships.** Anchor people to landmarks, body orientations, and feasible routes. Distinguish world position, screen position, and a character's anatomical left/right. Derive multiple views from one map.
3. **Continue motion across cuts.** Track contact, grip, release, support, and elapsed offscreen time. Cover hugs, turns, walking, and developing expressions without restarting the action.
4. **Connect independently generated groups.** Plan the scene first, then choose generation boundaries. Each group contains its own starting conditions; adjacent shots offer a useful change of observation while preserving the event state.
5. **Use references and handle ensembles.** Separate identity, layout, composition, and action-state references. Keep the complete scene map while selecting coverage for the current interaction.
6. **Learn through complete examples.** A letter handoff and a reunion with an observer include fictional source text, blocking, copyable prompts, and explanations of every adjacent cut. A new-scene exercise checks transfer.

The course contains **14 teaching figures, including 12 new original diagrams**. It retains source fidelity, performance direction, vocal emphasis, shared picture/sound timing, mandatory content prechecks, and concise production output.

Each generated group must be **an integer from 1 through 30 seconds, inclusive**. Individual shot boundaries may use decimals, but their durations must add up exactly. Continuous visible mouth-to-mouth contact is limited to three seconds under this project's requirements; changing angles or generation groups does not reset the count. This is a project constraint, not a claim about universal platform policy.

## Start a project

Send the complete skill and current script to the writing agent, specify the episode/shot range, completed material, and available references, then use the [startup instructions](8.1启动指令.txt). Copy each finished production group into your video tool. Keep teaching explanations and review reports outside production prompts.

> Use AI Drama Director Skill 8.1 to storyboard the attached script for [scope]. Read the source and complete the content precheck. Apply the spatial and action lessons before producing concise, independently copyable groups. Check every adjacent shot and group boundary for position, action phase, sound, and coverage. Preserve the exact dialogue; each group must total an integer of 1–30 seconds. Verify suspected adaptation gaps against the supplied or authorized novel rather than inventing plot.

## Images and evidence

The root Markdown uses image URLs pinned to a Git commit. The native package and ZIP use local assets; the PDF and HTML embed their images. A viewer that blocks external HTML images may require the PDF.

This update includes sampled visual analysis of the reference clip, primary-source research, spatial reasoning, dialogue/timing checks, and reading-package validation. **Seed2.5 generation has not been tested.** Clear text does not guarantee a successful generated film. See the [upgrade and validation record](8.1升级说明与验证记录.md). All teaching examples are fictional, and the public repository excludes private scripts and reference-video frames.

Historical 8.0 reading copies remain available. Use 8.1 for new work and retain the attribution **mr zhu** when sharing or quoting it.
