<p align="center">
  <img src="_statics/goclaw.png" alt="GoClaw" />
</p>

# GoClaw

[![Go](https://img.shields.io/badge/Go_1.26-00ADD8?style=flat-square&logo=go&logoColor=white)](https://go.dev/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL_18-316192?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/) [![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/) [![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=flat-square&logo=socket.io&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) [![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-000000?style=flat-square&logo=opentelemetry&logoColor=white)](https://opentelemetry.io/) [![Anthropic](https://img.shields.io/badge/Anthropic-191919?style=flat-square&logo=anthropic&logoColor=white)](https://www.anthropic.com/) [![OpenAI](https://img.shields.io/badge/OpenAI_Compatible-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

**GoClaw** là một AI gateway đa agent kết nối các LLM với công cụ, kênh liên lạc và dữ liệu của bạn — triển khai dưới dạng một file binary Go duy nhất, không phụ thuộc runtime. Hệ thống điều phối các nhóm agent và ủy quyền liên agent qua hơn 13 nhà cung cấp LLM với cách ly multi-tenant hoàn toàn.

Phiên bản Go của [OpenClaw](https://github.com/openclaw/openclaw) với bảo mật nâng cao, PostgreSQL multi-tenant và khả năng giám sát cấp production.

## Điểm Khác Biệt

- **Nhóm Agent & Điều Phối** — Nhóm với task board dùng chung, ủy quyền liên agent (sync/async), và khám phá agent lai
- **Multi-Tenant PostgreSQL** — Workspace riêng từng user, context file riêng từng user, API key mã hóa (AES-256-GCM), session cách ly — dự án Claw duy nhất có multi-tenancy native trong DB
- **Binary Đơn** — ~25 MB binary Go tĩnh, không cần Node.js runtime, khởi động <1s, chạy trên VPS $5
- **Bảo Mật Production** — 5 lớp phòng thủ: rate limiting, phát hiện prompt injection, bảo vệ SSRF, chặn shell nguy hiểm, mã hóa AES-256-GCM
- **13+ Nhà Cung Cấp LLM** — Anthropic (HTTP+SSE native với prompt caching), OpenAI, OpenRouter, Groq, DeepSeek, Gemini, Mistral, xAI, MiniMax, Cohere, Perplexity, DashScope (Qwen), Bailian Coding + Claude CLI (stdio + MCP bridge), Codex (gpt-5.3-codex qua OAuth)
- **7 Kênh Nhắn Tin** — Telegram (forum topics, STT), Discord, Slack, Zalo OA, Zalo Personal (DM + nhóm), Feishu/Lark (streaming cards, media), WhatsApp với lệnh `/stop` và `/stopall`
- **Extended Thinking** — Chế độ thinking theo provider (Anthropic budget tokens, OpenAI reasoning effort, DashScope thinking budget) hỗ trợ streaming

## Hệ Sinh Thái Claw

**Tài Nguyên Sử Dụng:**

|                 | OpenClaw        | ZeroClaw | PicoClaw | **GoClaw**                              |
| --------------- | --------------- | -------- | -------- | --------------------------------------- |
| Ngôn ngữ        | TypeScript      | Rust     | Go       | **Go**                                  |
| Kích thước binary | 28 MB + Node.js | 3.4 MB   | ~8 MB    | **~25 MB** (base) / **~36 MB** (+ OTel) |
| Docker image    | —               | —        | —        | **~50 MB** (Alpine)                     |
| RAM (idle)      | > 1 GB          | < 5 MB   | < 10 MB  | **~35 MB**                              |
| Khởi động       | > 5 s           | < 10 ms  | < 1 s    | **< 1 s**                               |
| Phần cứng mục tiêu | $599+ Mac Mini  | $10 edge | $10 edge | **$5 VPS+**                             |

**Ma Trận Tính Năng:**

| Tính năng                  | OpenClaw                             | ZeroClaw                                     | PicoClaw                              | **GoClaw**                     |
| -------------------------- | ------------------------------------ | -------------------------------------------- | ------------------------------------- | ------------------------------ |
| Multi-tenant (PostgreSQL)  | —                                    | —                                            | —                                     | ✅                             |
| Tích hợp MCP               | — (dùng ACP)                         | —                                            | —                                     | ✅ (stdio/SSE/streamable-http) |
| Nhóm agent                 | —                                    | —                                            | —                                     | ✅ Task board + mailbox        |
| Bảo mật nâng cao           | ✅ (SSRF, path traversal, injection) | ✅ (sandbox, rate limit, injection, pairing) | Cơ bản (workspace restrict, exec deny) | ✅ 5 lớp phòng thủ             |
| OTel observability         | ✅ (opt-in extension)                | ✅ (Prometheus + OTLP)                       | —                                     | ✅ OTLP (opt-in build tag)     |
| Prompt caching             | —                                    | —                                            | —                                     | ✅ Anthropic + OpenAI-compat   |
| Knowledge graph            | —                                    | —                                            | —                                     | ✅ LLM extraction + traversal  |
| Hệ thống skill             | ✅ Embeddings/semantic               | ✅ SKILL.md + TOML                           | ✅ Cơ bản                              | ✅ BM25 + pgvector hybrid      |
| Scheduler theo lane        | ✅                                   | Bounded concurrency                          | —                                     | ✅ (main/subagent/team/cron + concurrent group runs) |
| Kênh nhắn tin              | 37+                                  | 15+                                          | 10+                                   | 7+                             |
| Ứng dụng đi kèm            | macOS, iOS, Android                  | Python SDK                                   | —                                     | Web dashboard                  |
| Live Canvas / Voice        | ✅ (A2UI + TTS/STT)                  | —                                            | Voice transcription                   | TTS (4 providers)              |
| Nhà cung cấp LLM           | 10+                                  | 8 native + 29 compat                         | 13+                                   | **13+**                        |
| Workspace riêng user       | ✅ (file-based)                      | —                                            | —                                     | ✅ (PostgreSQL)                |
| Secret mã hóa              | — (env vars only)                    | ✅ ChaCha20-Poly1305                         | — (plaintext JSON)                    | ✅ AES-256-GCM trong DB        |

> **Điểm mạnh riêng GoClaw:** Dự án duy nhất có PostgreSQL multi-tenant, nhóm agent, hệ thống hooks, knowledge graph và hỗ trợ MCP protocol.

## Kiến Trúc

```mermaid
graph TB
    subgraph Clients
        WEB["Web Dashboard<br/>(React SPA)"]
        TG["Telegram"]
        DC["Discord"]
        SL["Slack"]
        FS["Feishu/Lark"]
        ZL["Zalo OA"]
        ZLP["Zalo Personal"]
        API["HTTP API"]
    end

    subgraph Gateway["GoClaw Gateway"]
        direction TB
        WS["WebSocket RPC"] & REST["HTTP Server"] & CM["Channel Manager"]
        WS & REST & CM --> BUS["Message Bus"]
        BUS --> SCHED["Lane-based Scheduler<br/>main · subagent · team · cron"]
        SCHED --> ROUTER["Agent Router"]
        ROUTER --> LOOP["Agent Loop<br/>think → act → observe"]
        LOOP --> TOOLS["Tool Registry<br/>fs · exec · web · memory · team · mcp · custom"]
        LOOP --> LLM["LLM Providers<br/>Anthropic (native + prompt caching) · OpenAI-compat (12+)"]
    end

    subgraph Storage
        PG["PostgreSQL 18 + pgvector<br/>(multi-tenant)"]
    end

    WEB --> WS
    TG & DC & SL & FS & ZL & ZLP --> CM
    API --> REST
    LOOP --> PG
```

## Điều Phối Đa Agent

GoClaw hỗ trợ bốn mô hình điều phối cho cộng tác agent, tất cả được quản lý qua liên kết quyền hạn rõ ràng.

### Ủy Quyền Agent

> **Lưu ý:** Tool `delegate` độc lập đã bị loại bỏ. Ủy quyền hiện được quản lý qua nhóm agent — leader tạo task trên board dùng chung và spawn member một cách tường minh. Các mô hình dưới đây mô tả khái niệm; xem [Nhóm Agent](#nhóm-agent) để biết công cụ hiện tại.

Ủy quyền agent cho phép các agent được đặt tên ủy quyền task cho agent khác — mỗi agent chạy với định danh, công cụ, nhà cung cấp LLM và context file riêng. Khác với subagent (bản sao ẩn danh của agent cha), mục tiêu ủy quyền là các agent độc lập hoàn toàn.

```mermaid
flowchart TD
    USER((Người dùng)) -->|"Nghiên cứu giá đối thủ"| SUPPORT

    subgraph TEAM["Nhóm Agent"]
        SUPPORT["Support Bot<br/>(Claude Haiku)"]
        RESEARCH["Research Bot<br/>(GPT-4)"]
        WRITER["Content Writer<br/>(Claude Sonnet)"]
        BILLING["Billing Bot<br/>(Gemini)"]
    end

    SUPPORT -->|"sync: chờ câu trả lời"| RESEARCH
    RESEARCH -->|"kết quả"| SUPPORT
    SUPPORT -->|"async: không chờ"| WRITER
    WRITER -.->|"thông báo khi xong"| SUPPORT
    SUPPORT -.-x|"không có link"| BILLING

    SUPPORT -->|"câu trả lời cuối"| USER

    style USER fill:#e1f5fe
    style SUPPORT fill:#fff3e0
    style RESEARCH fill:#e8f5e9
    style WRITER fill:#f3e5f5
    style BILLING fill:#ffebee
```

| Chế độ | Cách hoạt động | Phù hợp cho |
|--------|----------------|-------------|
| **Sync** | Agent A hỏi Agent B và **chờ** câu trả lời | Tra cứu nhanh, kiểm tra dữ kiện |
| **Async** | Agent A hỏi Agent B và **tiếp tục**. B thông báo kết quả sau | Task dài, báo cáo, phân tích sâu |

**Liên Kết Quyền Hạn** — Agent giao tiếp qua **agent links** tường minh với kiểm soát truy cập:

```bash
# Một chiều: support-bot có thể ủy quyền TỚI research-bot
agents.links.create {
  "sourceAgent": "support-bot",
  "targetAgent": "research-bot",
  "direction": "outbound",
  "maxConcurrent": 3
}

# Hai chiều: cả hai agent có thể ủy quyền cho nhau
agents.links.create {
  "sourceAgent": "support-bot",
  "targetAgent": "content-writer",
  "direction": "bidirectional"
}
```

| Hướng | Ý nghĩa |
|-------|---------|
| `outbound` | Source có thể ủy quyền TỚI target |
| `inbound` | Target có thể ủy quyền TỚI source |
| `bidirectional` | Cả hai agent có thể ủy quyền cho nhau |

**Kiểm Soát Đồng Thời** — Hai lớp ngăn agent bị quá tải:

| Lớp | Cấu hình | Ví dụ |
|-----|----------|-------|
| **Theo link** | `agent_links.max_concurrent` | support → research: tối đa 3 |
| **Theo agent** | `agents.other_config.max_delegation_load` | research-bot: tối đa 5 tổng |

**Hạn Chế Theo User** — JSONB `settings` trên agent links hỗ trợ danh sách deny/allow theo user.

**Khám Phá Agent** — Mỗi agent có trường `frontmatter` để khám phá. Với ≤15 mục tiêu, `AGENTS.md` tự động được inject vào context. Ủy quyền dùng subagent spawning cho tập mục tiêu lớn hơn.

<details>
<summary>Ủy Quyền vs Subagent</summary>

| Khía cạnh | Subagent | Ủy Quyền Agent |
|-----------|----------|----------------|
| Mục tiêu | Bản sao ẩn danh của cha | Agent được đặt tên với định danh riêng |
| Provider/Model | Kế thừa từ cha | Cấu hình riêng của target |
| Tools | Tool của cha trừ deny list | Registry + policy riêng của target |
| Context file | System prompt đơn giản | SOUL.md, IDENTITY.md riêng của target |
| Session | Dùng chung với cha | Cách ly (mới mỗi lần ủy quyền) |
| Quyền hạn | Chỉ giới hạn theo depth | `agent_links` tường minh với direction |
| Kiểm soát user | Không | Deny/allow theo user qua settings JSONB |
| Đồng thời | Giới hạn global + theo cha | Giới hạn theo link + theo target-agent |

</details>

### Nhóm Agent

Nhóm cho phép workflow đa agent phối hợp với task board dùng chung và nhắn tin peer-to-peer.

```mermaid
flowchart TD
    USER((Người dùng)) -->|tin nhắn| LEAD

    subgraph TEAM["Nhóm Agent"]
        LEAD["Lead Agent<br/>(điều phối)"]
        A1["Chuyên gia A"]
        A2["Chuyên gia B"]
        A3["Chuyên gia C"]
    end

    subgraph BOARD["Task Board Dùng Chung"]
        T1["Task 1: pending"]
        T2["Task 2: in_progress<br/>owner: A1"]
        T3["Task 3: blocked_by T2"]
    end

    subgraph MAIL["Mailbox Nhóm"]
        M1["A1 → LEAD: cập nhật trạng thái"]
        M2["LEAD → ALL: broadcast"]
    end

    LEAD -->|"tạo task"| BOARD
    A1 -->|"nhận"| T2
    T2 -.->|"tự động unblock"| T3
    A1 -->|"gửi tin"| MAIL
    LEAD -->|"broadcast"| MAIL
    LEAD -->|câu trả lời cuối| USER

    style USER fill:#e1f5fe
    style LEAD fill:#fff3e0
    style A1 fill:#e8f5e9
    style A2 fill:#e8f5e9
    style A3 fill:#e8f5e9
```

- **Vai trò nhóm** — Lead agent điều phối công việc, member agent thực thi task
- **Task board dùng chung** — Tạo, nhận, hoàn thành, tìm kiếm task với dependency `blocked_by`. Nhận task atomic ngăn gán trùng
- **Mailbox nhóm** — Nhắn tin peer-to-peer trực tiếp (gửi, broadcast, đọc chưa đọc)
- **Công cụ**: `team_tasks` cho quản lý task, `team_message` cho mailbox

## Tính Năng

### Nhà Cung Cấp LLM
- **13+ provider** — OpenRouter, Anthropic, OpenAI, Groq, DeepSeek, Gemini, Mistral, xAI, MiniMax, Cohere, Perplexity, DashScope (Qwen), Bailian Coding, và bất kỳ endpoint tương thích OpenAI
- **Anthropic native** — Tích hợp HTTP+SSE trực tiếp với prompt caching (`cache_control`) giảm ~90% chi phí trên prefix lặp lại. Cũng hỗ trợ chế độ Claude CLI (stdio + MCP bridge với quản lý session)
- **Tương thích OpenAI** — Prompt caching tự động cho OpenAI, MiniMax, OpenRouter (cache metrics theo dõi trong traces). Cũng hỗ trợ chế độ Codex (gpt-5.3-codex qua OAuth với metadata "phase")
- **Extended thinking** — Chế độ thinking theo provider: Anthropic (budget tokens), OpenAI-compat (reasoning effort), DashScope (thinking budget) với hỗ trợ streaming

### Điều Phối Agent
- **Agent loop** — Chu trình think-act-observe với tool use, history session, và auto-summarization
- **Subagent** — Spawn agent con với model khác để thực thi task song song
- **Ủy quyền agent** — Ủy quyền task liên agent sync/async với permission links, giới hạn đồng thời, và hạn chế theo user
- **Nhóm agent** — Task board dùng chung với dependency, mailbox nhóm, và workflow đa agent phối hợp
- **Lịch sử ủy quyền** — Trail audit có thể query của tất cả ủy quyền liên agent
- **Thực thi đồng thời** — Scheduler theo lane (main/subagent/team/cron), throttle thích ứng cho group chat

### Công Cụ & Tích Hợp
- **60+ built-in tool** — File system, shell exec, web search/fetch, memory, browser automation, TTS và nhiều hơn
- **Tích hợp MCP** — Kết nối MCP server bên ngoài qua stdio, SSE, hoặc streamable-http với grant theo agent/user
- **Hệ thống hooks** — Hook theo sự kiện với command evaluator (shell exit code) và agent evaluator (ủy quyền cho reviewer) để validate output

### Kênh Nhắn Tin
- **Telegram** — Tích hợp đầy đủ với streaming, rich formatting (HTML, table, code block), reaction, media, forum topic (config và session isolation theo topic), speech-to-text, bot command, giới hạn ghi file nhóm
- **Slack** — Tích hợp channel với bot command
- **Feishu/Lark** — Streaming card update, media attachment (ảnh/file), mention resolution, topic session mode
- **Zalo OA** — Tích hợp Official Account cho DM conversation
- **Zalo Personal** — Protocol reverse-engineered không chính thức hỗ trợ DM + tin nhắn nhóm với policy mặc định hạn chế
- **Discord, WhatsApp** — Channel adapter với lệnh `/stop` và `/stopall`
- **Persistent pending message** — Tin nhắn group chat lưu vào PostgreSQL với auto-compaction (LLM summarization) khi queue vượt ngưỡng

### Kiến Thức & Bộ Nhớ
- **Skill** — Knowledge base dựa trên SKILL.md với tìm kiếm hybrid BM25 + embedding (pgvector)
- **Long-term memory** — Tìm kiếm hybrid pgvector (full-text + vector similarity) với admin dashboard cho CRUD, search, và bulk re-indexing
- **Knowledge graph** — Trích xuất entity/relationship bằng LLM từ memory, duyệt graph (recursive CTE, max depth 3), và visualization force-directed. Agent tool: `knowledge_graph_search`

### Hạ Tầng
- **Cron scheduling** — Cú pháp `at`, `every`, và cron expression cho task agent theo lịch
- **Browser automation** — Headless Chrome qua Rod cho tương tác web
- **Text-to-Speech** — Provider OpenAI, ElevenLabs, Edge, MiniMax
- **Docker sandbox** — Thực thi code cách ly trong container
- **Tracing** — LLM call tracing với cache metrics, span metadata, và export OpenTelemetry OTLP tùy chọn
- **Tailscale** — Listener VPN mesh tùy chọn cho truy cập từ xa an toàn (build-tag gated)

### Bảo Mật
- **Rate limiting** — Token bucket theo user/IP, RPM có thể cấu hình
- **Quản lý API key** — Auth multi-key với RBAC scope (`admin`, `read`, `write`, `approvals`, `pairing`), lưu trữ SHA-256 hash, expiry tùy chọn, revocation
- **Phát hiện prompt injection** — Scanner 6 pattern regex (chỉ phát hiện, không bao giờ block)
- **Credential scrubbing** — Tự động redact API key, token, password từ tool output
- **Shell deny pattern** — Block `curl|sh`, reverse shell, `eval $()`, `base64|sh`
- **Bảo vệ SSRF** — DNS pinning, block private IP, block host
- **AES-256-GCM** — API key provider mã hóa trong database
- **Browser pairing** — Auth browser không cần token với pairing code được admin approve

### Web Dashboard
- Quản lý agent, xem trace & span, skill, team, MCP server, phê duyệt pairing, quản lý memory (CRUD + search + chunking), knowledge graph (table + force-directed visualization), dashboard pending message, quản lý API key, và tài liệu API tương tác (Swagger UI)

## Bắt Đầu Nhanh

```bash
git clone https://github.com/nextlevelbuilder/goclaw.git
cd goclaw
```

### Từ Source

```bash
# Build
make build

# Wizard setup tương tác
./goclaw onboard

# Khởi động gateway
source .env.local && ./goclaw
```

### Với Docker

**1. Chuẩn bị môi trường:**

```bash
# Tạo .env với secret tự động (GOCLAW_ENCRYPTION_KEY, GOCLAW_GATEWAY_TOKEN)
chmod +x prepare-env.sh
./prepare-env.sh
```

Script tạo `.env` từ `.env.example`, tự động tạo `GOCLAW_ENCRYPTION_KEY` và `GOCLAW_GATEWAY_TOKEN`, và kiểm tra API key provider. Thêm ít nhất một `GOCLAW_*_API_KEY` vào `.env` trước khi khởi động.

**2. Khởi động service:**

```bash
# Khuyến nghị: Gateway + Web Dashboard (http://localhost:3000)
# Pull image pre-built:
docker compose -f docker-compose.yml -f docker-compose.postgres.yml -f docker-compose.selfservice.yml up -d

# Hoặc build từ source:
docker compose -f docker-compose.yml -f docker-compose.postgres.yml -f docker-compose.selfservice.yml up -d --build

# Không có dashboard
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up -d

# + OpenTelemetry tracing (Jaeger tại http://localhost:16686)
docker compose -f docker-compose.yml -f docker-compose.postgres.yml -f docker-compose.otel.yml up -d --build

# + Tailscale (truy cập từ xa an toàn)
docker compose -f docker-compose.yml -f docker-compose.postgres.yml -f docker-compose.tailscale.yml up -d --build
```

Khi biến môi trường `GOCLAW_*_API_KEY` được set, gateway **tự động onboard** không cần prompt tương tác — nó phát hiện provider, tạo gateway token, kết nối Postgres, chạy migration, và seed dữ liệu mặc định.

**Auto-onboard phát hiện** API key khả dụng đầu tiên theo thứ tự ưu tiên: OpenRouter → Anthropic → OpenAI → Groq → DeepSeek → Gemini → Mistral → xAI → MiniMax → Cohere → Perplexity. Override với `GOCLAW_PROVIDER` và `GOCLAW_MODEL`. Memory tự động enable với hỗ trợ embedding nếu phát hiện key OpenAI, OpenRouter, hoặc Gemini.

**`.env` tối thiểu:**

```bash
GOCLAW_OPENROUTER_API_KEY=sk-or-your-key    # Bắt buộc: ít nhất một provider key
GOCLAW_GATEWAY_TOKEN=...                     # Tự động tạo bởi prepare-env.sh
GOCLAW_ENCRYPTION_KEY=...                    # Tự động tạo bởi prepare-env.sh
# GOCLAW_PROVIDER=openrouter                 # Tùy chọn: override provider mặc định
# GOCLAW_MODEL=anthropic/claude-sonnet-4     # Tùy chọn: override model mặc định
# POSTGRES_PASSWORD=your-secure-password     # Tùy chọn: mặc định "goclaw"
```

## Triển Khai

GoClaw yêu cầu PostgreSQL với pgvector. Thiết kế cho triển khai multi-user và multi-tenant với **cách ly theo user** — mỗi user có context file, history session, và workspace riêng.

```bash
# Thiết lập database
export GOCLAW_POSTGRES_DSN="postgres://user:pass@localhost:5432/goclaw?sslmode=disable"
export GOCLAW_ENCRYPTION_KEY=$(openssl rand -hex 32)

# Chạy upgrade database (schema migration + data hook)
./goclaw upgrade

# Khởi động gateway
./goclaw
```

**Tính năng:**

- Context file và workspace riêng user (bảng `user_context_files`)
- Loại agent: `open` (workspace riêng user) vs `predefined` (context dùng chung)
- Nhóm agent, ủy quyền
- LLM call tracing với span và prompt cache metrics
- Tích hợp MCP server với grant theo agent và user
- Tìm kiếm skill dựa embedding (hybrid BM25 + pgvector)
- Web dashboard cho agent, trace, skill, team, và MCP server
- Mã hóa API key (AES-256-GCM)

## Cài Đặt

### Yêu Cầu

- Go 1.26+
- PostgreSQL 18 với pgvector
- Docker (tùy chọn, cho sandbox và triển khai container)

### Build

```bash
# Build production (~25MB binary, static, stripped symbol)
CGO_ENABLED=0 go build -ldflags="-s -w" -o goclaw .

# Với hỗ trợ OpenTelemetry (~36MB binary)
CGO_ENABLED=0 go build -ldflags="-s -w" -tags otel -o goclaw .

# Với hỗ trợ Tailscale (~54MB binary)
CGO_ENABLED=0 go build -ldflags="-s -w" -tags tsnet -o goclaw .

# Với backend Redis cache
CGO_ENABLED=0 go build -ldflags="-s -w" -tags redis -o goclaw .

# Với cả OTel + Tailscale
CGO_ENABLED=0 go build -ldflags="-s -w" -tags "otel,tsnet" -o goclaw .
```

**So sánh kích thước binary qua hệ sinh thái Claw:**

| Build                    | Kích Thước Binary | Docker Image | Ghi chú                                   |
| ------------------------ | ----------------- | ------------ | ----------------------------------------- |
| **GoClaw** (base)        | ~25 MB            | ~50 MB       | `CGO_ENABLED=0 go build -ldflags="-s -w"` |
| **GoClaw** (+ OTel)      | ~36 MB            | ~60 MB       | Thêm `-tags otel` cho OTLP export         |
| **GoClaw** (+ Tailscale) | ~54 MB            | ~75 MB       | Thêm `-tags tsnet` cho Tailscale listener |
| **GoClaw** (+ cả hai)    | ~65 MB            | ~85 MB       | `-tags "otel,tsnet"`                      |
| PicoClaw                 | ~8 MB             | —            | Binary Go đơn                             |
| ZeroClaw                 | 3.4 MB            | —            | Binary Rust tối giản                      |
| OpenClaw                 | 28 MB             | —            | + ~390 MB Node.js runtime cần thiết       |

> Tính năng tùy chọn được gated sau build tag để tránh phình binary. OTel thêm ~11 MB (gRPC + protobuf). Tailscale thêm ~20 MB (tsnet + WireGuard). Build base bao gồm in-app tracing backed bởi PostgreSQL và truy cập localhost-only.

### Docker Image (Pre-built)

Image pre-built multi-arch (linux/amd64 + linux/arm64) được publish lên **GHCR** và **Docker Hub** mỗi release:

```bash
# GHCR (khuyến nghị)
docker pull ghcr.io/nextlevelbuilder/goclaw:latest

# Docker Hub
docker pull digitop/goclaw:latest
```

**Tag khả dụng:**

| Tag        | Mô tả                                   |
| ---------- | --------------------------------------- |
| `latest`   | Image base (~50 MB Alpine)              |
| `node`     | + Node.js runtime cho JS tool           |
| `python`   | + Python runtime cho Python tool        |
| `full`     | + Node.js + Python + tất cả bundled skill |
| `otel`     | + Hỗ trợ OpenTelemetry tracing          |
| `tsnet`    | + Tailscale VPN mesh listener           |
| `redis`    | + Backend Redis cache                   |

Tag semver cũng khả dụng: `1.0.0`, `1.0`, v.v. (ví dụ `ghcr.io/nextlevelbuilder/goclaw:1.0.0-python`).

**Web Dashboard:**

```bash
docker pull ghcr.io/nextlevelbuilder/goclaw-web:latest
docker pull digitop/goclaw-web:latest
```

### Docker Build (từ source)

```bash
# Image chuẩn (~50MB Alpine)
docker build -t goclaw .

# Với OpenTelemetry (~60MB)
docker build --build-arg ENABLE_OTEL=true -t goclaw:otel .

# Với Tailscale (~75MB)
docker build --build-arg ENABLE_TSNET=true -t goclaw:tsnet .

# Với cả OTel + Tailscale (~85MB)
docker build --build-arg ENABLE_OTEL=true --build-arg ENABLE_TSNET=true -t goclaw:full .
```

## Cấu Hình

### Wizard Setup

```bash
./goclaw onboard
```

Wizard cấu hình: provider, model, port gateway, channel, memory, browser, TTS, và tracing. Nó tạo `config.json` (không secret) và `.env.local` (chỉ secret).

### Auto-Onboard (Docker / CI)

Khi biến môi trường `GOCLAW_*_API_KEY` được set, gateway tự động cấu hình không cần prompt tương tác. Nó retry kết nối Postgres (tối đa 5 lần), chạy migration, và seed dữ liệu mặc định.

### Biến Môi Trường

<details>
<summary><strong>API Key Provider</strong> (set ít nhất một)</summary>

| Biến                        | Provider                 |
| --------------------------- | ------------------------ |
| `GOCLAW_OPENROUTER_API_KEY` | OpenRouter (khuyến nghị) |
| `GOCLAW_ANTHROPIC_API_KEY`  | Anthropic Claude         |
| `GOCLAW_OPENAI_API_KEY`     | OpenAI                   |
| `GOCLAW_GROQ_API_KEY`       | Groq                     |
| `GOCLAW_DEEPSEEK_API_KEY`   | DeepSeek                 |
| `GOCLAW_GEMINI_API_KEY`     | Google Gemini            |
| `GOCLAW_MISTRAL_API_KEY`    | Mistral AI               |
| `GOCLAW_XAI_API_KEY`        | xAI Grok                 |
| `GOCLAW_MINIMAX_API_KEY`    | MiniMax                  |
| `GOCLAW_COHERE_API_KEY`     | Cohere                   |
| `GOCLAW_PERPLEXITY_API_KEY` | Perplexity               |
| `GOCLAW_DASHSCOPE_API_KEY`  | DashScope (Qwen)         |
| `GOCLAW_BAILIAN_API_KEY`    | Bailian Coding           |

</details>

<details>
<summary><strong>Gateway & Ứng Dụng</strong></summary>

| Biến                      | Mô tả                            | Mặc định                     |
| ------------------------- | -------------------------------- | ---------------------------- |
| `GOCLAW_CONFIG`           | Đường dẫn file config            | `config.json`                |
| `GOCLAW_GATEWAY_TOKEN`    | Token xác thực API               | (tự tạo)                     |
| `GOCLAW_HOST`             | Địa chỉ bind server              | `0.0.0.0`                    |
| `GOCLAW_PORT`             | Port server                      | `18790`                      |
| `GOCLAW_PROVIDER`         | Provider LLM mặc định            | `anthropic`                  |
| `GOCLAW_MODEL`            | Model mặc định                   | `claude-sonnet-4-5-20250929` |
| `GOCLAW_WORKSPACE`        | Thư mục workspace agent          | `~/.goclaw/workspace`        |
| `GOCLAW_DATA_DIR`         | Thư mục lưu trữ dữ liệu          | `~/.goclaw/data`             |
| `GOCLAW_SESSIONS_STORAGE` | Đường dẫn lưu session            | `~/.goclaw/sessions`         |
| `GOCLAW_SKILLS_DIR`       | Thư mục skill                    | `~/.goclaw/skills`           |
| `GOCLAW_OWNER_IDS`        | ID user admin (phân cách bằng dấu phẩy) — owner có thể quản lý **tất cả** agent bất kể ownership và được dùng làm owner mặc định cho tài nguyên auto-seed |                              |

</details>

<details>
<summary><strong>Database</strong></summary>

| Biến                    | Mô tả                                      |
| ----------------------- | ------------------------------------------ |
| `GOCLAW_POSTGRES_DSN`   | Connection string PostgreSQL               |
| `GOCLAW_ENCRYPTION_KEY` | Key AES-256-GCM cho mã hóa API key         |
| `GOCLAW_MIGRATIONS_DIR` | Đường dẫn đến file migration               |

</details>

<details>
<summary><strong>Kênh Nhắn Tin</strong></summary>

| Biến                               | Mô tả                         |
| ---------------------------------- | ----------------------------- |
| `GOCLAW_TELEGRAM_TOKEN`            | Token bot Telegram            |
| `GOCLAW_ZALO_TOKEN`                | Access token Zalo             |
| `GOCLAW_FEISHU_APP_ID`             | App ID Feishu/Lark            |
| `GOCLAW_FEISHU_APP_SECRET`         | App secret Feishu/Lark        |
| `GOCLAW_FEISHU_ENCRYPT_KEY`        | Key mã hóa tin nhắn Feishu    |
| `GOCLAW_FEISHU_VERIFICATION_TOKEN` | Token xác minh Feishu         |

</details>

<details>
<summary><strong>Scheduler Lane</strong></summary>

| Biến                   | Mô tả                        | Mặc định |
| ---------------------- | ---------------------------- | -------- |
| `GOCLAW_LANE_MAIN`     | Đồng thời lane main          | `30`     |
| `GOCLAW_LANE_SUBAGENT` | Đồng thời lane subagent      | `50`     |
| `GOCLAW_LANE_TEAM`     | Đồng thời lane team          | `100`    |
| `GOCLAW_LANE_CRON`     | Đồng thời lane cron          | `30`     |

</details>

<details>
<summary><strong>Tailscale</strong> (yêu cầu build tag <code>tsnet</code>)</summary>

| Biến                    | Mô tả                                         | Mặc định   |
| ----------------------- | --------------------------------------------- | ---------- |
| `GOCLAW_TSNET_HOSTNAME` | Tên thiết bị Tailscale (vd: `goclaw-gateway`) | (tắt)      |
| `GOCLAW_TSNET_AUTH_KEY` | Auth key Tailscale                            |            |
| `GOCLAW_TSNET_DIR`      | Thư mục state persistent                      | OS default |

</details>

<details>
<summary><strong>Telemetry</strong> (yêu cầu build tag <code>otel</code>)</summary>

| Biến                            | Mô tả                       | Mặc định         |
| ------------------------------- | --------------------------- | ---------------- |
| `GOCLAW_TELEMETRY_ENABLED`      | Bật OTel export             | `false`          |
| `GOCLAW_TELEMETRY_ENDPOINT`     | OTLP endpoint               |                  |
| `GOCLAW_TELEMETRY_PROTOCOL`     | `grpc` hoặc `http`          | `grpc`           |
| `GOCLAW_TELEMETRY_INSECURE`     | Bỏ qua xác minh TLS         | `false`          |
| `GOCLAW_TELEMETRY_SERVICE_NAME` | Tên service trong trace     | `goclaw-gateway` |
| `GOCLAW_TRACE_VERBOSE`          | Log full LLM input trong span | `0`              |

</details>

<details>
<summary><strong>TTS (Text-to-Speech)</strong></summary>

| Biến                            | Mô tả                 |
| ------------------------------- | --------------------- |
| `GOCLAW_TTS_OPENAI_API_KEY`     | API key TTS OpenAI    |
| `GOCLAW_TTS_ELEVENLABS_API_KEY` | API key ElevenLabs    |
| `GOCLAW_TTS_MINIMAX_API_KEY`    | API key TTS MiniMax   |
| `GOCLAW_TTS_MINIMAX_GROUP_ID`   | Group ID MiniMax      |

</details>

## Lệnh CLI

```
goclaw                    Khởi động gateway (lệnh mặc định)
goclaw onboard            Wizard setup tương tác
goclaw version            In thông tin version và protocol
goclaw doctor             Kiểm tra sức khỏe hệ thống (bao gồm trạng thái schema)

goclaw upgrade            Upgrade schema database và chạy data hook
goclaw upgrade --status   Hiển thị version schema hiện tại vs yêu cầu
goclaw upgrade --dry-run  Xem trước thay đổi chờ xử lý mà không áp dụng

goclaw agent list         Liệt kê agent đã cấu hình
goclaw agent chat         Chat với agent
goclaw agent add          Thêm agent mới
goclaw agent delete       Xóa agent

goclaw migrate up         Áp dụng tất cả migration chờ xử lý
goclaw migrate down       Rollback migration
goclaw migrate version    Hiển thị version migration hiện tại
goclaw migrate force N    Buộc set version migration
goclaw migrate goto N     Migrate đến version cụ thể
goclaw migrate drop       Drop tất cả bảng (nguy hiểm)

goclaw config show        Hiển thị cấu hình hiện tại
goclaw config path        Hiển thị đường dẫn file config
goclaw config validate    Validate cấu hình

goclaw sessions list      Liệt kê session active
goclaw sessions delete    Xóa session
goclaw sessions reset     Reset history session

goclaw cron list          Liệt kê job đã lên lịch
goclaw cron delete        Xóa job
goclaw cron toggle        Bật/tắt job

goclaw skills list        Liệt kê skill khả dụng
goclaw skills show        Hiển thị chi tiết skill
```

**Thêm core skill:**

Đặt thư mục skill trong `skills/` (local dev) hoặc `/app/bundled-skills/` (Docker image). Mỗi thư mục phải chứa `SKILL.md` với YAML frontmatter (`name`, `description`, `slug`). Thư mục có tiền tố `_` được coi là code dùng chung, không phải skill.

Khi server khởi động, seeder tự động phát hiện tất cả thư mục skill, upsert vào database, và chạy kiểm tra dependency async. Không cần biến môi trường — seeder fallback về `skills/` trong local dev và `/app/bundled-skills` trong Docker.

```

goclaw models             Liệt kê model AI và provider
goclaw channels           Liệt kê kênh nhắn tin

goclaw pairing approve    Approve pairing code
goclaw pairing list       Liệt kê thiết bị đã pair
goclaw pairing revoke     Thu hồi pairing
```

**Flag:**

```
--config, -c    Đường dẫn đến file config (mặc định: config.json)
--verbose, -v   Bật debug logging
```

## API

Tài liệu API tương tác khả dụng tại `/docs` (Swagger UI) khi gateway đang chạy. Spec OpenAPI 3.0 được serve tại `/v1/openapi.json`.

| Tài liệu | Mô tả |
|----------|-------|
| [HTTP REST API](docs/18-http-api.md) | 130+ HTTP endpoint — chat completion, agent, skill, provider, MCP, memory, knowledge graph, channel, trace, usage, storage, API key |
| [WebSocket RPC](docs/19-websocket-rpc.md) | 64+ method RPC — chat, agent, config, session, cron, team, pairing, delegation, approval |
| [API Key & Auth](docs/20-api-keys-auth.md) | Mô hình xác thực, RBAC scope, quản lý API key, thiết kế bảo mật |
| [Gateway Protocol](docs/04-gateway-protocol.md) | Wire protocol WebSocket (v3), định dạng frame, vòng đời kết nối |

## Docker Compose

File compose cho các scenario triển khai khác nhau:

| File                             | Mục đích                                           |
| -------------------------------- | -------------------------------------------------- |
| `docker-compose.yml`             | Định nghĩa service base                            |
| `docker-compose.postgres.yml`    | PostgreSQL (pgvector/pgvector:pg18)                |
| `docker-compose.upgrade.yml`     | Service upgrade database one-shot                  |
| `docker-compose.selfservice.yml` | Web dashboard UI (nginx + React SPA)               |
| `docker-compose.browser.yml`     | Headless Chrome cho browser automation             |
| `docker-compose.sandbox.yml`     | Sandbox thực thi code dựa Docker                   |
| `docker-compose.otel.yml`        | OpenTelemetry + Jaeger tracing                     |
| `docker-compose.redis.yml`       | Backend Redis cache (build-tag gated)              |
| `docker-compose.tailscale.yml`   | Tailscale VPN mesh listener                        |

### Ví Dụ

```bash
# Chuẩn bị .env (tự động tạo secret, yêu cầu API key)
chmod +x prepare-env.sh && ./prepare-env.sh

# Dùng image pre-built (không có flag --build):
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up -d

# Managed + Web Dashboard (http://localhost:3000)
docker compose -f docker-compose.yml \
  -f docker-compose.postgres.yml \
  -f docker-compose.selfservice.yml up -d

# Managed + Web Dashboard + OpenTelemetry (Jaeger UI tại http://localhost:16686)
docker compose -f docker-compose.yml \
  -f docker-compose.postgres.yml \
  -f docker-compose.selfservice.yml \
  -f docker-compose.otel.yml up -d --build

# Managed + Tailscale (truy cập từ xa an toàn qua VPN mesh)
docker compose -f docker-compose.yml \
  -f docker-compose.postgres.yml \
  -f docker-compose.tailscale.yml up -d --build

# Kiểm tra health
curl http://localhost:18790/health
```

> **Lưu ý:** Bỏ `--build` để dùng image pre-built từ GHCR. Thêm `--build` để build từ source. Overlay yêu cầu build arg (otel, tsnet, redis, sandbox) cần `--build`.

### Upgrading (Docker Compose)

**Upgrade đơn giản** — pull image mới nhất và restart. Entrypoint tự động chạy `goclaw upgrade` (schema migration + data hook) trước khi khởi động:

```bash
# Dùng image pre-built (khuyến nghị):
docker compose -f docker-compose.yml -f docker-compose.postgres.yml \
  -f docker-compose.selfservice.yml pull
docker compose -f docker-compose.yml -f docker-compose.postgres.yml \
  -f docker-compose.selfservice.yml up -d

# Hoặc build từ source:
git pull
docker compose -f docker-compose.yml -f docker-compose.postgres.yml \
  -f docker-compose.selfservice.yml up -d --build
```

Thay file compose với overlay bạn dùng (vd: thêm `-f docker-compose.otel.yml` cho OTel).

**Upgrade tường minh** — nếu bạn muốn xem trước thay đổi hoặc chạy upgrade riêng trước khi restart:

```bash
# Kiểm tra trạng thái schema hiện tại
docker compose -f docker-compose.yml -f docker-compose.postgres.yml \
  -f docker-compose.upgrade.yml run --rm upgrade --status

# Xem trước thay đổi chờ xử lý (dry-run)
docker compose -f docker-compose.yml -f docker-compose.postgres.yml \
  -f docker-compose.upgrade.yml run --rm upgrade --dry-run

# Áp dụng upgrade (schema migration + data hook), sau đó xóa container
docker compose -f docker-compose.yml -f docker-compose.postgres.yml \
  -f docker-compose.upgrade.yml run --rm upgrade

# Sau đó rebuild và restart gateway với image mới
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up -d --build
```

### File Môi Trường (.env)

Dùng script `prepare-env.sh` để tạo `.env` với secret tự động:

```bash
./prepare-env.sh
```

Điều này tạo `.env` với `GOCLAW_ENCRYPTION_KEY` và `GOCLAW_GATEWAY_TOKEN` đã điền sẵn. Bạn chỉ cần thêm API key provider. Xem `.env.example` cho tất cả biến khả dụng.

## Công Cụ Built-in

| Công cụ            | Nhóm          | Mô tả                                                        |
| ------------------ | ------------- | ------------------------------------------------------------ |
| `read_file`        | fs            | Đọc nội dung file (với virtual FS routing)                   |
| `write_file`       | fs            | Ghi/tạo file                                                 |
| `edit_file`        | fs            | Áp dụng edit nhắm mục tiêu vào file hiện có                  |
| `list_files`       | fs            | Liệt kê nội dung thư mục                                     |
| `search`           | fs            | Tìm kiếm nội dung file theo pattern                          |
| `glob`             | fs            | Tìm file theo glob pattern                                   |
| `exec`             | runtime       | Thực thi lệnh shell (với workflow approval)                  |
| `web_search`       | web           | Tìm kiếm web (Brave, DuckDuckGo)                             |
| `web_fetch`        | web           | Fetch và parse nội dung web                                  |
| `memory_search`    | memory        | Tìm kiếm long-term memory (FTS + vector)                     |
| `memory_get`       | memory        | Lấy các entry memory                                         |
| `skill_search`     | —             | Tìm kiếm skill (BM25 + embedding hybrid)                     |
| `knowledge_graph_search` | memory  | Tìm kiếm entity và duyệt quan hệ knowledge graph             |
| `create_image`     | media         | Tạo ảnh (DashScope, MiniMax)                                 |
| `create_audio`     | media         | Tạo audio (OpenAI, ElevenLabs, MiniMax, Suno)                |
| `create_video`     | media         | Tạo video (MiniMax, Veo)                                     |
| `read_document`    | media         | Đọc tài liệu (Gemini File API, provider chain)               |
| `read_image`       | media         | Phân tích ảnh                                                |
| `read_audio`       | media         | Transcription và phân tích audio                             |
| `read_video`       | media         | Phân tích video                                              |
| `message`          | messaging     | Gửi tin nhắn đến channel                                     |
| `tts`              | —             | Tổng hợp Text-to-Speech                                      |
| `spawn`            | —             | Spawn subagent                                               |
| `subagents`        | sessions      | Điều khiển subagent đang chạy                                |
| ~~`delegate`~~     | orchestration | ~~Ủy quyền task cho agent khác~~ (đã xóa — dùng `team_tasks`) |
| `team_tasks`       | teams         | Task board dùng chung (list, create, claim, complete, search) |
| `team_message`     | teams         | Mailbox nhóm (send, broadcast, read)                         |
| `sessions_list`    | sessions      | Liệt kê session active                                       |
| `sessions_history` | sessions      | Xem history session                                          |
| `sessions_send`    | sessions      | Gửi tin nhắn đến session                                     |
| `sessions_spawn`   | sessions      | Spawn session mới                                            |
| `session_status`   | sessions      | Kiểm tra trạng thái session                                  |
| `cron`             | automation    | Lên lịch và quản lý cron job                                 |
| `gateway`          | automation    | Quản trị gateway                                             |
| `browser`          | ui            | Browser automation (navigate, click, type, screenshot)       |
| `announce_queue`   | automation    | Thông báo kết quả async (cho ủy quyền async)                 |

## Browser Pairing

Browser client có thể xác thực không cần token pre-shared qua flow pairing code:

1. User mở web dashboard và nhập User ID
2. Click "Yêu Cầu Truy Cập (Pairing)" — gateway tạo code 8 ký tự
3. Code hiển thị trong browser UI
4. Admin approve code qua CLI (`goclaw pairing approve XXXX`) hoặc web UI
5. Browser tự động phát hiện approval và được quyền truy cập operator-level
6. Lần truy cập sau, browser tự động reconnect dùng pairing đã lưu (không cần re-approval)

**Thu hồi truy cập:**

```bash
# Liệt kê thiết bị đã pair
goclaw pairing list

# Thu hồi pairing cụ thể
goclaw pairing revoke <sender_id>
```

Sau khi thu hồi, browser fallback về flow pairing lần truy cập sau.

## Tailscale (Truy Cập Từ Xa)

GoClaw hỗ trợ listener [Tailscale](https://tailscale.com) tùy chọn cho truy cập từ xa an toàn qua VPN mesh. Tailscale listener chạy cùng gateway chính, serve cùng route trên cả hai listener.

**Build-tag gated:** Dependency `tsnet` (~20 MB) chỉ được compile khi build với `-tags tsnet`. Binary mặc định không bị ảnh hưởng.

```bash
# Build với hỗ trợ Tailscale
go build -tags tsnet -o goclaw .

# Cấu hình qua biến môi trường
export GOCLAW_TSNET_HOSTNAME=goclaw-gateway
export GOCLAW_TSNET_AUTH_KEY=tskey-auth-xxxxx

# Khởi động — cả localhost:18790 và Tailscale listener đều active
./goclaw
```

Khi Tailscale được bật và gateway vẫn bind `0.0.0.0`, log sẽ gợi ý chuyển sang `127.0.0.1` cho truy cập localhost-only + Tailscale:

```
GOCLAW_HOST=127.0.0.1 ./goclaw
```

Điều này giữ gateway không thể truy cập từ LAN trong khi vẫn có thể truy cập qua Tailscale từ bất kỳ thiết bị nào trên tailnet.

**Docker:**

```bash
docker compose -f docker-compose.yml \
  -f docker-compose.postgres.yml \
  -f docker-compose.tailscale.yml up -d
```

Yêu cầu `GOCLAW_TSNET_AUTH_KEY` trong file `.env`. State Tailscale được persist trong Docker volume `tsnet-state`.

## Bảo Mật

- **Transport**: Validate CORS WebSocket, giới hạn tin nhắn 512KB, giới hạn body HTTP 1MB, token auth timing-safe
- **Quản lý API key**: Auth multi-key với 5 RBAC scope, lưu trữ SHA-256 hash, expiry tùy chọn, revocation, pattern show-once. Xem [API Key & Auth](docs/20-api-keys-auth.md)
- **Rate limiting**: Token bucket theo user/IP, RPM có thể cấu hình
- **Prompt injection**: Input guard với 6 pattern detection (chỉ phát hiện, không bao giờ block)
- **Shell security**: Deny pattern cho `curl|sh`, `wget|sh`, reverse shell, `eval`, `base64|sh`
- **Network**: Bảo vệ SSRF với blocked host + private IP + DNS pinning
- **File system**: Ngăn path traversal, hạn chế workspace
- **Encryption**: AES-256-GCM cho API key provider trong database
- **Browser pairing**: Auth browser không token với admin approval (pairing code, auto-reconnect)
- **Tailscale**: Listener VPN mesh tùy chọn cho truy cập từ xa an toàn (build-tag gated)

## Testing

```bash
# Unit test
go test ./...

# Integration test (yêu cầu gateway đang chạy)
go test -v -run 'TestHealthHTTP|TestConnectHandshake' ./tests/integration/

# Full integration (yêu cầu API key)
GOCLAW_OPENROUTER_API_KEY=sk-or-xxx go test -v ./tests/integration/ -timeout 120s
```

## Trạng Thái Dự Án

### Đã Implement & Test Production

- **Quản lý & cấu hình agent** — Tạo, cập nhật, xóa agent qua API và web dashboard. Loại agent (`open` / `predefined`), agent routing, và lazy resolution đều đã test.
- **Kênh Telegram** — Tích hợp đầy đủ đã test: xử lý tin nhắn, streaming response, rich formatting (HTML, table, code block), reaction, media, chunk tin nhắn dài.
- **Seed data & bootstrapping** — Auto-onboard, DB seeding, migration pipeline test end-to-end.
- **User-scope & content file** — Context file riêng user (`user_context_files`), context file cấp agent (`agent_context_files`), virtual FS interceptor, seeding riêng user (`SeedUserFiles`), và tracking user-agent profile tất cả đã implement và test.
- **Core built-in tool** — File system tool (`read_file`, `write_file`, `edit_file`, `list_files`, `search`, `glob`), shell execution (`exec`), web tool (`web_search`, `web_fetch`), và session management tool test trong agent loop thực.
- **Hệ thống memory** — Long-term memory với pgvector hybrid search (FTS + vector) implement và test với conversation thực.
- **Agent loop** — Chu trình think-act-observe, tool use, session history, auto-summarization, và subagent spawning test trong production.
- **WebSocket RPC protocol (v3)** — Connect handshake, chat streaming, event push tất cả test với web dashboard và integration test.
- **Store layer (PostgreSQL)** — Tất cả PG store (session, agent, provider, skill, cron, pairing, tracing, memory, team) implement và đang chạy.
- **Browser automation** — Tích hợp Rod/CDP cho headless Chrome, test trong workflow agent production.
- **Scheduler theo lane** — Cách ly lane main/subagent/team/cron với thực thi đồng thời đã test. Group chat hỗ trợ đến 3 agent run đồng thời mỗi session với throttle thích ứng và deferred session write cho history isolation.
- **Bảo mật nâng cao** — Rate limiting, phát hiện prompt injection, CORS, shell deny pattern, bảo vệ SSRF, credential scrubbing tất cả implement và verify.
- **Web dashboard** — Quản lý channel, quản lý agent, approval pairing, xem trace & span, skill, MCP, cron, session, team, và trang config tất cả implement và hoạt động.
- **Prompt caching** — Anthropic (`cache_control` tường minh), OpenAI/MiniMax/OpenRouter (tự động). Cache metrics theo dõi trong trace span và hiển thị trong web dashboard.
- **Ủy quyền agent** — Ủy quyền task liên agent với permission link, chế độ sync/async, hạn chế theo user, giới hạn đồng thời, và hybrid agent search. Test trong production.
- **Nhóm agent** — Tạo nhóm với vai trò lead/member, task board dùng chung (create, claim, complete, search, blocked_by dependency), mailbox nhóm (send, broadcast, read). Test trong production.
- **Evaluate loop** — Chu trình feedback generator-evaluator với max round và pass criteria có thể cấu hình. Test trong production.
- **Lịch sử ủy quyền** — Trail audit có thể query của ủy quyền liên agent. Test trong production.
- **Hệ thống skill** — Tìm kiếm BM25, upload ZIP, parse SKILL.md, và tìm kiếm hybrid embedding. Test trong production.
- **Tích hợp MCP** — Transport stdio, SSE, và streamable-http với grant theo agent/user. Test trong production.
- **Cron scheduling** — Scheduling `at`, `every`, và cron expression. Test trong production.
- **Docker sandbox** — Thực thi code cách ly trong container. Test trong production.
- **Text-to-Speech** — Provider OpenAI, ElevenLabs, Edge, MiniMax. Test trong production.
- **HTTP API** — `/v1/chat/completions`, `/v1/agents`, `/v1/skills`, v.v. Test trong production. Swagger UI tương tác tại `/docs`.
- **Quản lý API key** — Auth multi-key với RBAC scope, lưu trữ SHA-256 hash, pattern show-once, expiry tùy chọn, revocation. HTTP + WebSocket CRUD. Web UI cho quản lý.
- **Hệ thống hook** — Hook theo sự kiện với command evaluator (shell exit code) và agent evaluator (ủy quyền cho reviewer). Blocking gate với auto-retry và evaluation recursion-safe.
- **Media tool** — `create_image` (DashScope, MiniMax), `create_audio` (OpenAI, ElevenLabs, MiniMax, Suno), `create_video` (MiniMax, Veo), `read_document` (Gemini File API), `read_image`, `read_audio`, `read_video`. Lưu trữ media persistent với MediaRef lazy-loaded.
- **Chế độ provider bổ sung** — Claude CLI (Anthropic qua stdio + MCP bridge), Codex (OpenAI gpt-5.3-codex qua OAuth).
- **Knowledge graph** — Trích xuất entity bằng LLM, duyệt graph, visualization force-directed, và agent tool `knowledge_graph_search`.
- **Quản lý memory** — Admin dashboard cho memory document (CRUD, semantic search, chi tiết chunk/embedding, bulk re-indexing).
- **Persistent pending message** — Tin nhắn channel persist vào PostgreSQL với auto-compaction (LLM summarization) và dashboard giám sát.

### Đã Implement Nhưng Chưa Test Đầy Đủ

- **Slack** — Tích hợp channel implement, chưa validate với user thực.
- **Các kênh nhắn tin khác** — Channel adapter Discord, Zalo OA, Zalo Personal, Feishu/Lark, WhatsApp implement nhưng chưa test end-to-end trong production. Chỉ Telegram được validate với user thực.
- **OpenTelemetry export** — OTLP gRPC/HTTP exporter implement (build-tag gated). In-app tracing hoạt động; external OTel export chưa validate trong production.
- **Tích hợp Tailscale** — tsnet listener implement (build-tag gated). Chưa test trong triển khai thực.
- **Redis cache** — Backend distributed cache tùy chọn (build-tag gated). Chưa test trong production.
- **Browser pairing** — Flow pairing code implement với CLI và web UI approval. Flow cơ bản test nhưng chưa validate ở quy mô.

## Ghi Nhận

GoClaw được xây dựng dựa trên dự án [OpenClaw](https://github.com/openclaw/openclaw) gốc. Chúng tôi biết ơn kiến trúc và tầm nhìn đã truyền cảm hứng cho phiên bản Go này.

## Giấy Phép

MIT
