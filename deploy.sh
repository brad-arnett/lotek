#!/usr/bin/env bash
# Generic GitHub Pages Deployment Script
# Usage: ./deploy.sh [config_file]

set -e

# Configuration defaults
DEPLOY_BRANCH="gh-pages"
BUILD_DIR="output"
GITHUB_USER=""
GITHUB_EMAIL=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running in GitHub Actions
IN_GITHUB_ACTIONS="${GITHUB_ACTIONS:-false}"

# Parse configuration
if [[ -n "$1" && -f "$1" ]]; then
    while IFS='=' read -r key value; do
        key=$(echo "$key" | tr -d ' ')
        value=$(echo "$value" | tr -d ' ')
        case "$key" in
            deploy_branch) DEPLOY_BRANCH="$value" ;;
            build_dir) BUILD_DIR="$value" ;;
            github_user) GITHUB_USER="$value" ;;
            github_email) GITHUB_EMAIL="$value" ;;
        esac
    done < "$1"
    log "Loaded config from $1"
fi

# Check for required environment variables
if [[ "$IN_GITHUB_ACTIONS" != "true" ]]; then
    if [[ -z "${GITHUB_TOKEN:-}" ]]; then
        log_warn "GITHUB_TOKEN not set. Setting up auth prompt..."
        read -p "Enter GitHub username: " GITHUB_USER
        read -p "Enter GitHub email: " GITHUB_EMAIL
    fi
fi

log "=== GitHub Pages Deployment ==="
log "Build Directory: $BUILD_DIR"
log "Deploy Branch: $DEPLOY_BRANCH"
log "User: ${GITHUB_USER:-$(whoami)}"
log "Email: ${GITHUB_EMAIL:-$(git config user.email)}"

# Step 1: Build the site
log "\n--- Step 1: Build ---"
npm run build || pnpm run build || yarn build || {
    log_error "No package manager detected. Run your build command manually."
    exit 1
}
log "Build completed successfully"

# Step 2: Configure git user
log "\n--- Step 2: Configure Git User ---"
git config user.name "$GITHUB_USER"
git config user.email "$GITHUB_EMAIL"

# Step 3: Setup gh-pages remote
log "\n--- Step 3: Setup gh-pages Remote ---"
git remote add -f "$DEPLOY_BRANCH" "git@github.com:${GITHUB_REPOSITORY}.git" 2>/dev/null || true
git remote set-url --push "$DEPLOY_BRANCH" "git@github.com:${GITHUB_REPOSITORY}.git"

# Step 4: Checkout or create deploy branch
log "\n--- Step 4: Checkout Deploy Branch ---"
git fetch "$DEPLOY_BRANCH" 2>/dev/null || true

if ! git branch --list | grep -q "^*.*$DEPLOY_BRANCH$"; then
    log_warn "Branch $DEPLOY_BRANCH does not exist, creating new branch..."
    git checkout -b "$DEPLOY_BRANCH"
else
    log "Branch $DEPLOY_BRANCH exists, switching to it..."
    git checkout "$DEPLOY_BRANCH"
fi

# Step 5: Clean and copy build output
log "\n--- Step 5: Copy Build Output ---"
# Remove existing files
git ls-files -z --deleted -- "$BUILD_DIR" | xargs -0 git rm -f --quiet 2>/dev/null || true

# Copy build directory contents
rsync -av --include '*/' --include '* --exclude=' "$BUILD_DIR/" . 2>/dev/null || {
    cp -r "$BUILD_DIR"/. .
}

# Step 6: Ensure .nojekyll file exists (prevents GitHub from modifying pages)
touch .nojekyll

# Step 7: Add all changes
log "\n--- Step 6: Add Changes ---"
git add .

# Step 8: Create commit
log "\n--- Step 7: Create Commit ---"
COMMIT_MSG="${COMMIT_MSG:-"Deploy: $(git log -1 --pretty=format:'%s' HEAD 2>/dev/null || echo 'Latest changes')"}"
git commit -m "$COMMIT_MSG" || {
    log_warn "No changes to commit, skipping..."
}

# Step 9: Force push to deploy branch
log "\n--- Step 8: Push to $DEPLOY_BRANCH ---"
git push "$DEPLOY_BRANCH" HEAD --force-with-lease 2>/dev/null || {
    log_error "Failed to push to $DEPLOY_BRANCH. Check your GITHUB_TOKEN permissions."
    exit 1
}

log "\n${GREEN}=== Deployment Complete ===${NC}"
log "Your site is now available at: https://$GITHUB_USER.github.io/${GITHUB_REPOSITORY#*/}"
