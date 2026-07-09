# Create a GitHub Actions Bot (GitHub App)
Workflows using the default `GITHUB_TOKEN` cannot push to `development` (PR-required branch)
or create pull requests (org Actions policy). A GitHub App bot issues short-lived tokens that
can bypass branch protection, without a paid seat or a long-lived PAT.

## 1. Create the GitHub App
1. Go to the org: `https://github.com/organizations/fireballenterprise/settings/apps`
2. Click **New GitHub App**
3. Fill in:
   - **GitHub App name**: `fireball-actions-bot`
   - **Homepage URL**: `https://github.com/fireballenterprise/shopify_dawn_theme`
   - **Webhook**: uncheck **Active**
4. Set **Repository permissions**:
   - **Contents**: Read and write
5. **Where can this GitHub App be installed?**: Only on this account
6. Click **Create GitHub App**

## 2. Generate a Private Key
1. On the app's **General** page, note the **App ID**
2. Scroll to **Private keys** → **Generate a private key** (downloads a `.pem` file)

## 3. Install the App on the Repo
1. App page → **Install App** → **Install** next to `fireballenterprise`
2. Choose **Only select repositories** → `shopify_dawn_theme` → **Install**

## 4. Let the Bot Bypass Branch Protection
In `shopify_dawn_theme` → **Settings** → **Branches** → edit the `development` rule:
1. Under **Require a pull request before merging**, enable
   **Allow specified actors to bypass required pull requests**
2. Add `fireball-actions-bot` to the bypass list

## 5. Add Repo Secret and Variable
In `shopify_dawn_theme` → **Settings** → **Secrets and variables** → **Actions**:
1. **Variables** tab → **New repository variable**: `BOT_APP_ID` = the App ID
2. **Secrets** tab → **New repository secret**: `BOT_PRIVATE_KEY` = full contents of the `.pem`

## 6. Use the Bot Token in Workflows
Add a token step before any step that pushes to `development` (`deploy.yml` bump-version job,
`release.yml` version job):

```yaml
- name: Generate bot token
  id: bot-token
  uses: actions/create-github-app-token@v2
  with:
    app-id: ${{ vars.BOT_APP_ID }}
    private-key: ${{ secrets.BOT_PRIVATE_KEY }}
```

Commit with `[skip ci]` and push directly to `development` using the token:

```yaml
          git commit -m "chore: bump VERSION to $new_version [skip ci]"
          git push "https://x-access-token:${BOT_TOKEN}@github.com/${{ github.repository }}.git" HEAD:development
        env:
          BOT_TOKEN: ${{ steps.bot-token.outputs.token }}
```

## Notes
- **`[skip ci]` is the infinite-loop guard**: bot-token pushes trigger workflows (unlike
  `GITHUB_TOKEN` pushes), so an unguarded bump push to `development` would re-run Deploy forever
- Rotate the key: generate a new `.pem` on the app page, update `BOT_PRIVATE_KEY`, delete the old key
- The app token expires after 1 hour and is scoped to the installed repos only
