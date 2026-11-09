---
title: Secure Claude Code and Codex With Agent Identities
channel: accuknox
video: AccuKnox_Agent_Identities_Walkthrough.mp4
video_length: 1:44
source_page: https://help.accuknox.com/how-to/agent-identities/
visibility: public
category: Science & Technology
made_for_kids: false
---

# Title (pick one)

1. **Secure Claude Code and Codex With Agent Identities** (50 characters, recommended, matches the search words)
2. Give Every Coding Agent Its Own Identity in 5 Steps (51 characters)
3. Stop Coding Agents From Borrowing Your Login (44 characters)

# Description (paste as is)

Give Claude Code and Codex their own identity in AgentZ. Set one up in 5 steps and approve the models it can use.

Written guide: https://help.accuknox.com/how-to/agent-identities/
AgentZ: https://agentzharness.ai/
AgentZ docs: https://docs.agentzharness.ai/

Coding agents such as Claude Code and Codex run on a developer's machine with that developer's own login. Their calls look like the developer's calls, and nothing limits or records them. An agent identity gives each agent its own name, a list of approved models and its own access that you can revoke.

This walkthrough connects a Codex agent from start to finish. It ends with Codex running on an approved model.

What you will see
- The External agents list, with the status and approved access of each agent
- How to add Claude Code or Codex and name the machine
- How to download the AgentZ CLI for your system
- How to save the config block to ~/.config/agentz/config.yaml
- How to launch the agent, sign in, tick the models it may use and click Authorize

Before you start
- An AgentZ workspace where you can open Workspace settings
- Claude Code or Codex on the machine you want to connect. Codex must be version 0.162.1 or later.

The five steps
1. Open Workspace settings, then External agents, and click Add agent.
2. Pick Claude Code or Codex and name the machine, such as work-laptop.
3. Download the AgentZ CLI and put the agentz binary on your PATH.
4. Save the config block from the Setup tab to ~/.config/agentz/config.yaml.
5. Run the launch command, sign in, choose the models and click Authorize.

The written guide also covers MCP tools, agent traces in Lens, and how to revoke an agent's access.

Chapters
0:00 Open the External Agents Page
0:22 Add an Agent and Name the Machine
0:34 Download the AgentZ CLI
0:50 Save the Agent Config
1:04 Launch the Agent and Choose Models
1:20 Run Codex and Open Lens

# Tags

AccuKnox, AgentZ, agent identities, AI agent security, coding agent security, Claude Code security, Codex security, secure coding agents, AI agent governance, AI agent access control, AI agent audit trail, AgentZ CLI, external agents, Claude Code, Codex

# Thumbnail brief

- Pair with the title. Text on the image: "Every agent gets its own name" (5 words, or cut to "Own name. Own limits.").
- Image: a zoomed crop of the External agents list. Show the rows m4 (Codex), ubuntu (Claude Code) and test (Codex), with Connected and "3 models" visible. The user column is already blurred in the video.
- Alternative start: the existing poster `docs/how-to/images/agent-identities/AccuKnox_Agent_Identities_Walkthrough.jpg` on branch `docs/agent-identities-external-agents`.
- Size: 1280x720, JPEG or PNG under 2 MB.

# Check before you publish

1. Chapter times came from frames at 1 to 4 second steps. Scrub each one in the player. I could not hear the audio.
2. The video shows Lens only as a menu hover at about 1:28. The guide says activity is under Lens, Traces. Keep chapter 1:20 as is unless the narration says more.
3. First 10 seconds show a loading page, then the agent list. A video cannot be swapped after upload, so decide now if you want a cold open on the finished result.
4. YouTube rejects the less-than and greater-than characters in titles and descriptions. This draft has none.
5. Upload the clean name `AccuKnox_Agent_Identities_Walkthrough.mp4`. Set the same name as the file title.
