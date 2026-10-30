> Adaptation note: all application modules, file paths, component names, roles, routes, and domain states below are examples. Discover their equivalents in the current `[PROJECT_NAME]` workspace. Preserve the current project’s approved requirements rather than imposing this sample architecture or policy.

# Lifecycle and role matrix

Build the test grid from actual routes and role definitions in the current checkout. At minimum cover active, organization inactive, archived, unarchived-from-active, unarchived-from-inactive, suspended where implemented, and globally deactivated. For multi-organization identities, verify independent A/B/C membership states and global restriction across all.

Use separate local browser contexts for platform administrator, owner, organization administrator, manager, team lead, employee, and restricted role where supported. Do not treat platform Basic Auth as the employee's browser session. Verify effective Inactive and the `Restricted by [PROJECT_NAME]` explanation without exposing private reasons. Confirm owner/last-admin and self-reactivation denial.

For each state, inspect organization switcher, direct URLs, existing LiveView, refresh/back/tabs, APIs, project/team/department membership, task assignment, reports, invitations, login, and session restoration. Existing task assignees and historical report subjects remain visible to authorized viewers; new assignments to ineligible users fail. Unarchive restores the previous Active/Inactive membership without recreating intentionally removed relationships. Restriction views must not render protected tenant data beneath them.

Include the approved task: Teams → existing team → List View → Assign Users. Verify that the interface opens, an eligible active member can be assigned and persisted, duplicate and restricted targets are rejected, unauthorized and cross-tenant requests do not mutate data, and cancel/error feedback works. Record controls that are absent in the actual UI as not applicable, not passed.
