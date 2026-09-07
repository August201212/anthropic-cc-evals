# Interactive shell configuration
export PATH="/opt/homebrew/bin:$PATH"

export HISTSIZE=10000
setopt SHARE_HISTORY

# Homebrew mirrors
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.ustc.edu.cn/homebrew-bottles"
export HOMEBREW_NO_AUTO_UPDATE=1

# Node
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
