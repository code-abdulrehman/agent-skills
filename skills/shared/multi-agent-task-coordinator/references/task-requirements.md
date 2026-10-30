# Resolve the current task requirements

Find the approved issue, specification, acceptance criteria, and implementation evidence for the active `[PROJECT_NAME]` workspace. Discover their actual locations; no historical issue number or documentation filename is required. Read current source and nearby tests before treating a report as a description of present behavior.

Record scope, actor roles, resource boundaries, invariants, non-goals, dependencies, accepted behavior, and concrete validation. Derive priorities and handoff phases from that contract. If policy is missing or contradictory, identify the decision instead of inventing it. A stale test is not a new product requirement.

## Example: membership and resource access

The following illustrates the kinds of invariants to extract when the approved task concerns memberships; it does not impose these states or policies on other projects:

- Distinguish active, inactive, archived, and suspended memberships only if those states exist. Verify visibility, denied operations, restoration rules, and authentication separately.
- Distinguish organization-level restrictions from global account restrictions. Local administration should not bypass an approved global restriction or allow self-reactivation through forged requests.
- Preserve historical assignments and authorized history; require current eligibility and authorization for new assignments. Reassignment and restored visibility require explicit approved behavior.
- Check actor, tenant, and resource scope at each protected operation. Retain owner/last-admin safeguards where required by the actual domain.

Use neutral actors such as `example-user` and organizations such as `example-org` in shared examples. Preserve the current project’s correct behavior and applied migrations. Resolve new policy or irreversible changes through the task’s existing authorization rules.
