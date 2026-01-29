#!/bin/bash
# Skills Migration & Sync Script
# 全自动迁移和同步技能

set -e  # 遇到错误立即退出

REPO_PATH="/Volumes/ORICO/Github/skills"
CLAUDE_SKILLS="$HOME/.claude/skills"
AGENTS_SKILLS="$HOME/.agents/skills"
SYNC_SCRIPT="$CLAUDE_SKILLS/skill-repo-syncer/scripts/sync.py"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ==================== 阶段 1: 迁移架构 ====================
phase1_migrate_structure() {
    log "========== 阶段 1: 迁移技能架构 =========="
    log "将 ~/.claude/skills 中的实际目录移到 ~/.agents/skills 并创建 symlink"
    echo ""

    cd "$CLAUDE_SKILLS"

    # 需要迁移的技能列表
    SKILLS_TO_MIGRATE=(
        "agent-browser"
        "article-translator"
        "artifacts-builder"
        "bm-md-formatter"
        "changelog-generator"
        "competitive-ads-extractor"
        "content-research-writer"
        "developer-growth-analysis"
        "document-skills"
        "domain-name-brainstormer"
        "doubao-tts-router"
        "explaining-code"
        "file-organizer"
        "image-enhancer"
        "invoice-organizer"
        "jimeng-image-router"
        "lead-research-assistant"
        "markdown-to-twitter"
        "meeting-insights-analyzer"
        "mindmap-generator"
        "nanobanana-router"
        "newsletter-collector"
        "openrouter-cost-tracker"
        "product-requirements"
        "raffle-winner-picker"
        "react-best-practices"
        "research-to-diagram"
        "skill-repo-syncer"
        "skill-share"
        "skills"
        "tech-manga-explainer"
        "twitter-to-wechat"
        "ui-ux-pro-max"
        "video-downloader"
        "wechat-cover-generator"
        "wechat-title-generator"
        "x-article-publisher"
    )

    MIGRATED_COUNT=0

    for skill in "${SKILLS_TO_MIGRATE[@]}"; do
        if [ -d "$skill" ] && [ ! -L "$skill" ]; then
            # 是实际目录，不是 symlink
            if [ ! -d "$AGENTS_SKILLS/$skill" ]; then
                log "迁移: $skill"

                # 1. 移动到 .agents/skills
                mv "$CLAUDE_SKILLS/$skill" "$AGENTS_SKILLS/"

                # 2. 创建 symlink
                ln -s "$AGENTS_SKILLS/$skill" "$CLAUDE_SKILLS/$skill"

                success "已迁移: $skill -> ~/.agents/skills/$skill"
                ((MIGRATED_COUNT++))
            else
                warn "$skill 已在 ~/.agents/skills 中存在，跳过"
            fi
        fi
    done

    echo ""
    success "阶段 1 完成: 共迁移 $MIGRATED_COUNT 个技能"
    echo ""
}

# ==================== 阶段 2: 同步新增技能到 Repo ====================
phase2_sync_new_to_repo() {
    log "========== 阶段 2: 同步新增技能到 Repo =========="
    log "将 ~/.agents/skills 中有但 Repo 中没有的技能同步到 GitHub"
    echo ""

    cd "$AGENTS_SKILLS"

    NEW_SKILLS_COUNT=0

    for skill in */; do
        skill=${skill%/}  # 移除末尾的 /
        if [ ! -d "$REPO_PATH/$skill" ]; then
            log "发现新技能，准备同步到 Repo: $skill"

            # 使用 sync.py 同步到 repo
            if python3 "$SYNC_SCRIPT" "$skill" --to-repo <<< "y" 2>/dev/null; then
                success "已同步到 Repo: $skill"
                ((NEW_SKILLS_COUNT++))
            else
                error "同步失败: $skill"
            fi
        fi
    done

    echo ""
    success "阶段 2 完成: 共同步 $NEW_SKILLS_COUNT 个新技能到 Repo"
    echo ""
}

# ==================== 阶段 3: 同步 Repo 更新到本地 ====================
phase3_sync_repo_to_local() {
    log "========== 阶段 3: 同步 Repo 更新到本地 =========="
    log "将 Repo 中比本地新的技能同步到 ~/.agents/skills"
    echo ""

    # 获取需要同步的技能列表（Repo 更新的）
    REPO_NEWER_SKILLS=$(python3 "$SYNC_SCRIPT" list 2>/dev/null | grep "Repo newer" | awk '{print $1}')

    SYNCED_COUNT=0

    for skill in $REPO_NEWER_SKILLS; do
        log "Repo 更新，同步到本地: $skill"

        # 使用 sync.py 从 repo 同步到本地
        if python3 "$SYNC_SCRIPT" "$skill" --from-repo <<< "y" 2>/dev/null; then
            success "已同步到本地: $skill"
            ((SYNCED_COUNT++))
        else
            error "同步失败: $skill"
        fi
    done

    echo ""
    success "阶段 3 完成: 共同步 $SYNCED_COUNT 个 Repo 更新的技能到本地"
    echo ""
}

# ==================== 验证结果 ====================
verify_result() {
    log "========== 验证结果 =========="
    echo ""

    # 统计数量
    CLaude_ACTUAL=$(find "$CLAUDE_SKILLS" -maxdepth 1 -type d | wc -l)
    CLaude_ACTUAL=$((CLaude_ACTUAL - 1))  # 减去 . 目录
    CLaude_SYMLINK=$(find "$CLAUDE_SKILLS" -maxdepth 1 -type l | wc -l)
    AGENTS_COUNT=$(find "$AGENTS_SKILLS" -maxdepth 1 -type d | wc -l)
    AGENTS_COUNT=$((AGENTS_COUNT - 1))
    REPO_COUNT=$(find "$REPO_PATH" -maxdepth 1 -type d | wc -l)
    REPO_COUNT=$((REPO_COUNT - 1))

    echo "📊 统计结果："
    echo "  ~/.claude/skills 实际目录: $CLaude_ACTUAL"
    echo "  ~/.claude/skills symlink: $CLaude_SYMLINK"
    echo "  ~/.agents/skills 技能总数: $AGENTS_COUNT"
    echo "  Repo 技能总数: $REPO_COUNT"
    echo ""

    # 检查是否还有非 symlink 的目录
    NON_SYMLINK=$(find "$CLAUDE_SKILLS" -maxdepth 1 -type d ! -type l | grep -v "^$CLAUDE_SKILLS$" | wc -l)
    if [ "$NON_SYMLINK" -gt 0 ]; then
        warn "~/.claude/skills 中还有 $NON_SYMLINK 个非 symlink 的目录"
        find "$CLAUDE_SKILLS" -maxdepth 1 -type d ! -type l | grep -v "^$CLAUDE_SKILLS$" | head -10
    else
        success "~/.claude/skills 中所有技能都是 symlink ✓"
    fi

    echo ""
    success "迁移和同步全部完成！"
}

# ==================== 主程序 ====================
main() {
    log "开始执行 Skills 全自动迁移和同步"
    log "时间: $(date)"
    echo ""

    # 检查必要目录
    if [ ! -d "$CLAUDE_SKILLS" ]; then
        error "目录不存在: $CLAUDE_SKILLS"
        exit 1
    fi

    if [ ! -d "$AGENTS_SKILLS" ]; then
        error "目录不存在: $AGENTS_SKILLS"
        exit 1
    fi

    if [ ! -d "$REPO_PATH" ]; then
        error "目录不存在: $REPO_PATH"
        exit 1
    fi

    # 确认执行
    echo "⚠️  这将执行以下操作："
    echo "   1. 将 ~/.claude/skills 中的 37 个实际目录移到 ~/.agents/skills"
    echo "   2. 在 ~/.claude/skills 中创建相应的 symlink"
    echo "   3. 将新增技能同步到 GitHub Repo"
    echo "   4. 将 Repo 中更新的技能同步到本地"
    echo ""
    read -p "确认执行? (yes/no): " confirm

    if [ "$confirm" != "yes" ]; then
        log "已取消"
        exit 0
    fi

    echo ""

    # 执行三个阶段
    phase1_migrate_structure
    phase2_sync_new_to_repo
    phase3_sync_repo_to_local
    verify_result
}

# 运行主程序
main "$@"
