------ todo-list begin at 2026/05/13/17:05:08 -----

用户请求：
clash verge问题：查看019dc51d-e92a-7910-9762-633b0264debc中的会话内容，查看/Users/liam/Code/codex/tools/codex-tun-feilian-fix和/Users/liam/Code/codex/tools/codex-backend-diagnostics中的内容，在/Users/liam/Code/codex/clash-verge中创建一个代理网络问题检修的handbook/，目录建立一个文档，每个章节的内容单独新建一个文档。script/中存放相关脚本和代码文件和readme使用说明。按照/Users/liam/Code/codex/tools/project-memory-persistence初始化工作目录，gh新建仓库并用git提交远程。

制定清单：
- [] 1. 理解源会话与参考工具内容
  - [] 1.1 读取 session `019dc51d-e92a-7910-9762-633b0264debc`
  - [] 1.2 读取 `tools/codex-tun-feilian-fix`
  - [] 1.3 读取 `tools/codex-backend-diagnostics`
  - [] 1.4 提炼可复用的 handbook 结构
- [] 2. 初始化 `clash-verge` 的 durable 工作目录
  - [x] 2.1 创建 memory 资产文件
  - [x] 2.2 写入 `AGENTS.md` / `CURRENT.md` / `PROGRESS.md`
  - [x] 2.3 写入 `log.md` / `user-queries.md` / `TODOList.md`
  - [x] 2.4 补齐目录 README
- [] 3. 创建 handbook 章节
  - [x] 3.1 写入总览与核心原则
  - [x] 3.2 写入 DNS / 规则 / TUN 三层排查章节
  - [x] 3.3 写入订阅更新检查与平台差异章节
  - [x] 3.4 写入目录索引
- [] 4. 收拢 script 目录
  - [x] 4.1 写入脚本使用说明
  - [x] 4.2 放入 macOS / Windows 检查脚本
  - [x] 4.3 放入 Codex 诊断代码文件
- [] 5. 初始化 git 与远程仓库
  - [x] 5.1 确认本地仓库状态
  - [o] 5.2 使用 gh 创建远程仓库
  - [] 5.3 提交并推送首个版本
- [] 6. 验证与收尾
  - [] 6.1 检查目录结构与关键文件
  - [] 6.2 更新日志与任务状态
  - [] 6.3 结束 todo block

执行问题记录：
- 任务 5.2 失败：`gh repo create --push` 在没有任何本地 commit 的情况下拒绝执行。处理方式：先创建首个 commit，再重新创建/绑定远程并推送。
