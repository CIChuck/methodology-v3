RGDIR=/opt/homebrew/lib/node_modules/@openai/codex/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/codex-path
export PATH="$RGDIR:$PATH"
unalias rg 2>/dev/null; unset -f rg 2>/dev/null
export UV_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1
export TMPDIR=/var/folders/dh/wfnmsgpn1yl83xlbmc109sf40000gn/T/v3-skills-council-round4-lk4zdm_d/claude/tmp/
cd /Users/chuckrussell/Dev/gendev/methodology-v3
