# RiftTrace Frontend Production Quality

## Purpose

The RiftTrace frontend provides a protected
interface for interacting with the cyber-risk
environment model and simulation APIs.

Frontend hardening focuses on predictable user
experience, session security, error handling,
accessibility and build reliability.

## Authentication

RiftTrace uses Django session authentication.

The browser communicates with the backend
through the same-origin `/api` path.

During local development, Vite proxies `/api`
requests to the Django backend.

Authentication state is maintained through
HttpOnly Django session cookies.

## CSRF

Unsafe requests such as POST, PUT, PATCH and
DELETE require Django CSRF protection.

The frontend obtains a CSRF cookie through:

`/api/auth/csrf/`

and sends the token through the
`X-CSRFToken` request header.

## Protected Routes

Authenticated application routes are wrapped
with `ProtectedRoute`.

Unauthenticated users are redirected to the
login page.

The originally requested route is preserved so
the user can continue after successful login.

## Session Controls

Authenticated users can see the active username
and explicitly sign out.

Logout invalidates the Django session and
returns the user to the login route.

## API Routing

Frontend code uses the relative API prefix:

`/api`

Browser code must not directly call the local
Django development address.

Local development routing is:

Browser
→ Vite `/api`
→ Django

## Error Handling

Unexpected React rendering failures are caught
by the global application error boundary.

Expected page-level failures should use
consistent loading, error and empty-state
presentation.

Internal stack traces are not displayed to
users.

## Form Reliability

Asynchronous form submissions should disable the
submit control while the request is in progress.

This reduces accidental duplicate requests.

## Accessibility

Forms should provide associated labels.

Interactive controls must be keyboard
accessible.

Focus-visible styles are preserved for keyboard
navigation.

Status and error messages use appropriate ARIA
roles where required.

## Responsive Behaviour

RiftTrace should remain usable across desktop,
laptop and smaller viewport sizes.

Graph-intensive analysis views may retain
specialized navigation appropriate to graph
visualization.

## Quality Gate

Run:

```bash
./scripts/frontend_quality_gate.sh
