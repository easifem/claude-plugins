# claude-plugins

Claude plugin marketplace for EASIFEM development.

| Plugin | Description |
|---|---|
| [easifem-dev](easifem-dev/README.md) | Conventions, `/new-method`, `/write-docblock`, `/write-test`, `/review`, `/refactor`, `/bug-report`, `/fix-bug`, and safety hooks for base, classes and the kernels. |

## Install (Claude Code)

From this folder (local):

```bash
claude plugin marketplace add ~/Library/CloudStorage/Dropbox/easifem/easifem-claude-plugins
claude plugin install easifem-dev@easifem
```

From GitHub (once pushed, e.g. to `easifem/claude-plugins`):

```bash
claude plugin marketplace add easifem/claude-plugins
claude plugin install easifem-dev@easifem
```

### Enable only in EASIFEM repos

The plugin adds skill and agent listings to every session it is on. To
keep it out of unrelated projects, switch it off in
`~/.claude/settings.json`:

```json
{ "enabledPlugins": { "easifem-dev@easifem": false } }
```

and switch it on in each EASIFEM repo (`base`, `classes`, `elasticity`,
`seepage`, `diffusion`, `cookbook`) in `.claude/settings.local.json`:

```json
{ "enabledPlugins": { "easifem-dev@easifem": true } }
```

## Update

After changing the plugin, bump `version` in
`easifem-dev/.claude-plugin/plugin.json` and in
`.claude-plugin/marketplace.json`, then:

```bash
claude plugin marketplace update easifem
```
