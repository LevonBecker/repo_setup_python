# Repo Manager Agent

The repo module handles repository-level operations including git synchronization and cleanup tasks.

## Features

- **Repository Push/Pull**: Full git operations
- **Screenshot Cleanup**: Remove old screenshots from centralized repo screenshots/ folder
- **Automated Commits**: Timestamp-based commit messages
- **Error Handling**: Graceful handling of push/pull failures

## Commands

### `/repo push` (alias: `/push`)
Push changes to git remote from any location.

**Workflow:**
1. **Navigate to repository root** - Automatically changes to repo directory
2. **Git pull** - Fetch and merge latest changes from remote
3. **Check for local changes** - Identify uncommitted work with `git status`
4. **Stage all changes** - Run `git add .` if changes detected
5. **Commit with timestamp** - Create commit: `Push repository: Automated commit YYYY-MM-DD HH:MM:SS`
6. **Push to remote** - Upload changes to GitHub
7. **Confirm completion** - Show status summary

**Features:**
- ✅ Works from any directory in the repository
- ✅ Automatic git operations (pull, commit, push)
- ✅ Timestamp-based commit messages
- ✅ Error handling for each push step

**When to Use:**
- **End of session** - Push all work before closing
- **After making changes** - Save work to remote
- **Regular backups** - Keep work synchronized and safe
- **After major changes** - Backup important work immediately

**Error Handling:**
- Git pull failure: Stops execution
- Git push failure: Stops execution with error

**Module:** `modules.repo.push` (via `/repo push`)

### `/repo pull` (alias: `/pull`)
Pull updates from git remote from any location.

**Workflow:**
1. **Check working directory** - Stash local changes if the working tree is dirty
2. **Git pull** - Fetch and merge latest changes from remote (rebase, to handle diverged history)
3. **Restore stash** - Restore stashed changes, if any were made

**Features:**
- ✅ Works from any directory in the repository
- ✅ Stashes and restores local changes automatically around the pull
- ✅ Rebases onto latest remote history instead of merge-committing

**When to Use:**
- **Start of session** - Get latest from git remote
- **After making changes on another device** - Pull updates to local
- **Before starting work** - Ensure you have latest version

**Error Handling:**
- Stash failure: Stops execution
- Git pull failure: Stops execution; restores the stash first if one was made

**Module:** `modules.repo.pull` (via `/repo pull`)

### `/repo cleanup`
Clean up old screenshot images from centralized repository screenshots/ folder.

**Workflow:**
1. **Navigate to repository root** - Automatically changes to repo directory
2. **Scan central screenshots/** - Find all image files in `${repo_local}/screenshots/`
3. **Preserve latest.png** - Keep `latest.png` for AI viewing
4. **Count files** - Report total number of screenshot files to be deleted
5. **Calculate size** - Show total disk space to be freed
6. **Delete files** - Remove all screenshot files except `latest.png`
7. **Show git status** - Display files staged for deletion
8. **Suggest next step** - Recommend running `/push` to commit changes

**File Patterns Cleaned:**
```
*.png (except latest.png)
*.jpg
*.jpeg
*.PNG
*.JPG
*.JPEG
```

**Target Directory:**
```
${repo_local}/screenshots/
(Centralized screenshots folder at repo root)
```

**Preserved File:**
```
latest.png - Always kept for AI viewing via 'ss' command
```

**Output Example:**
```
🧹 Starting screenshot cleanup...
🔍 Scanning central screenshots/ folder...
📋 Found 15 screenshot files (excluding latest.png):
./screenshots/Screenshot 2026-01-04 at 3.00.09 PM.png
./screenshots/Screenshot 2026-01-03 at 2.15.22 PM.png
...

📏 Calculating file sizes...
Total size: 2.3 MB

🗑️ Deleting old screenshots...
   Deleted: ./screenshots/Screenshot 2026-01-04 at 3.00.09 PM.png
   Preserved: ./screenshots/latest.png
   ...

✅ Cleanup completed!
   - Files deleted: 14
   - Files preserved: 1 (latest.png)

📊 Git status (deleted files):
 D screenshots/Screenshot 2026-01-04 at 3.00.09 PM.png
   Total files staged for deletion: 14

💡 Next steps:
   Run '/push' to commit and push these changes
```

**Features:**
- ✅ Works from any directory in the repository
- ✅ Scans centralized screenshots/ folder only
- ✅ Preserves `latest.png` for AI viewing
- ✅ Case-insensitive file matching (PNG, png, JPG, jpg)
- ✅ Shows files being deleted
- ✅ Reports total cleanup statistics
- ✅ Stages deletions in git automatically
- ✅ No confirmation required (fast operation)

**Use Cases:**
- **Before major commits** - Reduce repository size
- **Storage management** - Free up disk space
- **Git LFS management** - Clean up tracked files
- **Regular maintenance** - Keep repo lightweight
- **After screenshot-heavy sessions** - Remove temporary visual references while preserving latest.png

**Important Notes:**
- Screenshots are tracked by Git LFS but still consume local space
- Cleanup stages files for deletion but doesn't commit automatically
- Run `/push` after cleanup to commit and push deletions
- `latest.png` is ALWAYS preserved for AI viewing via `ss` command
- No confirmation prompt - deletion is immediate

**Module:** `modules.repo.cleanup` (via `/repo cleanup`)

### `/repo set_screenshots`
Configure macOS to save all screenshots to the central repository `screenshots/` folder.

**Workflow:**
1. Ensure the central `screenshots/` directory exists at the repo root
2. Update macOS screenshot location via `defaults write com.apple.screencapture location`
3. Restart the macOS UI server with `killall SystemUIServer`
4. Confirm the final configured path

**When to Use:**
- After running topic or conversation scripts that point screenshots at per-topic folders
- When screenshots start showing up on Desktop or another unexpected location
- After macOS updates or settings resets that break the central screenshot flow
- Anytime you want to ensure screenshots go to the central repo folder

**Output Example:**
```
🎯 Setting macOS screenshot location to central repo folder
📂 Repository root: ${repo_local}
📸 Ensuring screenshots directory exists...
⚙️ Updating macOS screenshot location...
✅ Screenshot location configured: ${repo_local}/screenshots
💡 All new screenshots will save here. Use 'ss' to view the latest screenshot.
```

**Features:**
- ✅ Creates screenshots folder if it doesn't exist
- ✅ Sets macOS system preference for screenshot location
- ✅ Restarts UI server to apply changes immediately
- ✅ Confirms the configured path
- ✅ Works from any directory

**Use Cases:**
- **After topic initialization** - Topic scripts may change screenshot location
- **Session start** - Ensure screenshots go to central location
- **Troubleshooting** - Fix when screenshots save to wrong location
- **After macOS updates** - Reset if system updates change preferences

**Module:** `modules.repo.set_screenshots` (via `/repo set_screenshots`)

## Branch Maintenance

### `/rebase`
Rebase the current branch onto the remote default branch (`origin/main` or `origin/master`).
Optionally offers to run `/squash` first. Handles stashing local changes and interactive conflict
resolution (ours/theirs/manual) if restoring the stash conflicts.

**Module:** `modules.repo.rebase` (via `/rebase`)

### `/squash`
Anchored squash of every commit down to the repository's root commit into one commit, with an
auto-generated bulleted message. Prompts to review the message, confirm the (irreversible) local
squash, and optionally force-push (`--force-with-lease`).

**Module:** `modules.repo.squash` (via `/squash`)

## Git Integration

### Push/Pull Operations

**Pull Sequence:**
```bash
git status --porcelain  # Check for uncommitted changes, stash if dirty
git pull --rebase       # Fetch and rebase onto remote
git stash pop           # Restore stashed changes, if any
```

**Push Sequence:**
```bash
git pull                # Fetch and merge from remote
git status --porcelain  # Check for changes
git add .               # Stage all changes
git commit -m "Push repository: Automated commit 2025-12-11 01:30:45"
git push                # Upload to remote
```

**Commit Message Format:**
```
Push repository: Automated commit YYYY-MM-DD HH:MM:SS
```

### Cleanup Operations

**Detection:**
```bash
find . -type f -path "*/screenshots/*" \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \)
```

**Deletion:**
```bash
rm [screenshot files]
git status --porcelain | grep "^.D"  # Show deleted files
```

Files are staged for deletion but not committed. User must run `/push` to commit.

## Configuration

Default settings in `config.yml`:
- `repo_path`: "${repo_local}"

## Permissions Required

- `git_pull` - Pull from remote repository
- `git_push` - Push to remote repository
- `git_commit` - Create commits
- `git_status` - Check repository status
- `file_delete` - Delete screenshot files
- `directory_access` - Navigate repository directories
- `bash_execute` - Run shell scripts

## Dependencies

- `git` - Version control operations
- `find` - Locate screenshot files

## Best Practices

1. **Pull/Push Regularly**: Run `/repo pull` at start, `/repo push` at end of sessions
2. **Clean Periodically**: Run `/repo cleanup` when screenshots accumulate
3. **Check Status**: Review git status before push if concerned about changes
4. **Network Aware**: Git operations require network connectivity
5. **Backup Important**: Always push before major changes or deletions

## Workflow Examples

**Cleanup and Push:**
```
1. /repo cleanup             # Remove all screenshots (23 files)
2. /repo push                # Commit deletions and push
```

**Cross-Device Workflow:**
```
Device A:
1. /repo pull                # Pull latest before starting
   [work on content]
2. /repo push                # Push changes to remote

Device B (later):
1. /repo pull                # Pull changes from Device A
```

## Related Commands

- `/repo push` - Push all commits to remote (alias: `/push`)
- `/repo view_screenshot` - View latest screenshot from central folder (alias: `/ss`)

## Files

- `push.py` - Push to git (used by `/repo push`, alias `/push`)
- `pull.py` - Pull from git (used by `/repo pull`, alias `/pull`)
- `cleanup.py` - Screenshot cleanup module (used by `/repo cleanup`)
- `set_screenshots.py` - macOS screenshot location configuration module (used by `/repo set_screenshots`)
- `view_screenshot.py` - Copy latest screenshot to latest.png (used by `/repo view_screenshot`, alias `/ss`)
- `config.yml` - Agent configuration
- `README.md` - This file

## Command Aliases

- `/push` → Push to git
- `/pull` → Pull from git
- `/ss` → View latest screenshot
