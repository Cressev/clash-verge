# AGENTS.md

## Project Summary

- Project name: `clash-verge`
- Project root: `/Users/liam/Code/codex/clash-verge`
- Primary goal: 沉淀 Clash Verge / Feilian / Codex / SSH 相关代理网络问题的检修手册、脚本和可复用操作记录。
- Current phase: initialization
- Main users/stakeholders: 当前机器的使用者与后续接手的 Codex agent

## Scope

本文件定义 `/Users/liam/Code/codex/clash-verge` 下的长期规则。若任务会触及仓库外路径或系统级配置，应先确认风险再改动。

## Canonical Paths

- Project root: `/Users/liam/Code/codex/clash-verge`
- Durable memory root: `/Users/liam/Code/codex/clash-verge`
- Handbook: `/Users/liam/Code/codex/clash-verge/handbook`
- Scripts: `/Users/liam/Code/codex/clash-verge/script`
- Findings: `/Users/liam/Code/codex/clash-verge/findings`
- Reports: `/Users/liam/Code/codex/clash-verge/reports`
- User task intake: `/Users/liam/Code/codex/clash-verge/user-queries.md`
- Task tracking: `/Users/liam/Code/codex/clash-verge/TODOList.md`

## Project Story

这个项目来自一次关于 Clash Verge 开启 TUN 后，Codex 或公司网络链路时好时坏的排查。
关键结论是：不能只看“代理开没开”，要同时检查 DNS、规则和 TUN 路由三层。
handbook 负责把这些经验整理成可复用章节，script 负责保留检查手段。

## Session Startup Rules

开始新任务前，先读：

1. `AGENTS.md`
2. `CURRENT.md`
3. `PROGRESS.md`
4. 相关目录 `README.md`
5. `log.md` 末尾
6. `user-queries.md` 末尾
7. 找到最新未处理 query
8. 立刻追加 `[Recieve:<timestamp>]`

## Task Intake

- `user-queries.md` 是任务入口 source of truth。
- 用户原话必须原样追加，不能改写、润色、合并或重排。
- 完成后在同一 block 追加 `[Done:<timestamp>]`，如有 git commit 再附 commit hash。

## TODOList Rules

- `TODOList.md` 是追加式任务追踪，不得删除或重写历史记录。
- 每个新请求都要新开一个 begin block，初始状态全部为 `[]`。
- 执行过程中持续更新状态，不能事后批量补写。
- 失败任务标记为 `[o]`，并在“执行问题记录”里说明原因与处理方式。
- 所有任务完成后补 end 分隔符。

## Logging Rules

- `log.md` 只做简短追加，记录动作、产物、验证和下一步。
- 真实时间统一使用 `date '+%y/%m/%d-%H:%M:%S %Z'`。

## Git Policy

- Local git: enabled
- Remote git: enabled
- Default branch policy: `main`
- Commit rule: 每次形成可交付里程碑就提交一次，尽量保持小而清晰。
- Never rewrite history unless: 用户明确要求且能解释影响

## File Safety

- 不删除、不覆盖用户未明确要求处理的内容。
- 改动保持局部、可审查。
- 任何破坏性命令都需要明确理由。

## User Preferences

- 回答请用中文。
- 优先使用现有的分析语言、脚本和文件结构，不要凭空另起一套。

## Hard Rules / Do Not Violate

- 不要修改仓库外的文件，除非任务明确要求且已确认。
- 不要重写 git 历史。
- 不要把关键记忆只留在聊天里。

## External Systems

- Clash Verge / Mihomo: 作为系统级网络代理与 TUN 控制面，改动前先看配置与运行状态。
- Feilian VPN: 作为公司内网路由与 DNS 来源，排查时要和 Clash 区分开。
- GitHub: 用于远程同步仓库。

## Validation Expectations

- 默认验证：`git status --short`
- 结构验证：`find . -maxdepth 2 -type f`
- 脚本验证：`python3 script/codex_backend_diagnostics.py --help`
- 手工验证：DNS、路由、TUN 相关问题仍需在目标机器上实际确认

## Durable Artifacts

- Handbook chapters: 代理网络问题检修的分章说明
- Scripts: 可复用的检查脚本与诊断代码
- Findings: 会反复用到的稳定经验或环境坑点
- Logs: 任务轨迹与验证结果

## Open Questions

- 远程仓库默认设为 private，是否符合你的长期习惯？
- 后续 handbook 还要不要继续拆成更细的子章节？
