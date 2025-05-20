# GitHub Copilot Commit Message Instructions

This guide explains how to write effective commit messages for projects using GitHub Copilot assistance. Following these conventions ensures clarity, maintainability, and professionalism.

---

## 1. Commit Message Structure

Each commit message should follow this basic structure:

```
<type>: <short summary>

[body]

[optional footer]
```

### Components

- **type**: Describes the purpose of the commit (e.g., `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`).
- **short summary**: A concise description (imperative mood, ≤ 72 characters).
- **body**: Explain the **what** and **why** of the change.
- **footer**: (Optional) Link to issues (e.g., `Closes #123`).

---

## 2. Common Commit Types

| Type     | Description                                | Example                              |
| -------- | ------------------------------------------ | ------------------------------------ |
| feat     | A new feature                              | `feat: add user profile page`        |
| fix      | A bug fix                                  | `fix: resolve crash on login`        |
| docs     | Documentation-only changes                 | `docs: update installation guide`    |
| style    | Code style changes (formatting, no logic)  | `style: format code with Prettier`   |
| refactor | Code restructuring without behavior change | `refactor: simplify auth middleware` |
| test     | Adding or updating tests                   | `test: add unit tests for login`     |
| chore    | Maintenance tasks (build, deps, CI)        | `chore: update dependencies`         |
| revert   | Revert a previous commit                   | `revert: revert login bug fix`       |

---

## 3. Writing Good Commit Messages

- Use imperative mood: "Fix typo" not "Fixed typo".
- Be concise: Keep subject line ≤ 72 characters.
- Capitalize the first letter of the subject.
- Separate subject and body with a blank line.
- Wrap the body at 72 characters if it's long.
- Explain why, not just what, in the body.

---

## 4. Examples

### Simple Feature

```
feat: add password reset functionality
```

### Bug Fix with Body

```
fix: correct user token expiration bug

Adjusted the token generation logic to ensure that user tokens now expire exactly 24 hours after issuance. This prevents unexpected session invalidations.

Closes #456
```

### Documentation Update

```
docs: add API usage examples to README
```

---

## 5. Tips When Using Copilot

- Review suggestions: Copilot-generated messages may be generic. Edit to add context.
- Focus on clarity: Prefer being specific over brief if it improves understanding.
- Avoid mechanical commits: Group meaningful changes together logically.

> "Write commits for the future reader – including yourself."

---

## 6. Bonus: Useful Prefixes (Optional)

For even better organization, some teams use additional prefixes like:

- build: changes that affect the build system (webpack, npm, etc.)
- ci: changes to CI configuration files and scripts
- perf: changes that improve performance
- deps: dependency updates

Example:

```
build: update Dockerfile for node 20
```

---

Following this standard will keep our project history clean, helpful, and professional.
