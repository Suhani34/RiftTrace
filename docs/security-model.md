Authentication method:
Django sessions

Authorization model:
OrganizationMembership

Roles:
ADMIN
ANALYST
VIEWER

Tenant boundary:
Organization

Browser protection:
CSRF

Session credential storage:
HttpOnly cookie

Sensitive actions:
Require membership + role

Cross-organization references:
Rejected

Production secrets:
Environment variables

Unauthenticated API:
Denied by default
