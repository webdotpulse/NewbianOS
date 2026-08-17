# ==============================================================================
# NewbianOS Zsh Developer Configuration
# ==============================================================================

# Enable colors and modern prompt
autoload -U colors && colors

# History settings
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt appendhistory
setopt sharehistory
setopt incappendhistory
setopt hist_ignore_all_dups

# Developer Aliases
alias agy="agy"
alias antigravity="antigravity-ide"
alias chrome="google-chrome-newbian"
alias figma="figma-desktop"
alias gdrive="gdrive"
alias jarvis="jarvis"
alias hud="jarvis --hud"
alias vitals="jarvis --status"

# Modern CLI enhancements
if command -v eza &>/dev/null; then
    alias ls="eza --icons --group-directories-first"
    alias ll="eza -la --icons --group-directories-first"
    alias tree="eza --tree --icons"
fi

if command -v batcat &>/dev/null; then
    alias cat="batcat --theme=TwoDark"
elif command -v bat &>/dev/null; then
    alias cat="bat --theme=TwoDark"
fi

# Git shortcuts
alias gs="git status -sb"
alias gd="git diff"
alias gl="git log --oneline --graph --decorate"
alias gco="git checkout"

# Initialize Starship Prompt if installed
if command -v starship &>/dev/null; then
    eval "$(starship init zsh)"
fi

# Environment paths
export PATH="$HOME/.local/bin:$HOME/.gemini/bin:/usr/local/go/bin:$HOME/go/bin:$HOME/.cargo/bin:$PATH"
export EDITOR="nvim"
export VISUAL="antigravity-ide"
