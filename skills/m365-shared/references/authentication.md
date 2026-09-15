# Authentication Methods

## 1. Browser Flow (Recommended)

```bash
m365 login --authType browser
```

Opens browser for interactive sign-in. Works with MFA and conditional access policies.

Always pass `--authType browser` explicitly. A bare `m365 login` falls back to the device code
flow, and a private app registration often has that flow switched off, in which case the login
fails with a bare `invalid_client` that names neither the flow nor the registration. It reads like
a broken install; it is a one-flag fix.

## 2. Device Code Flow

```bash
m365 login --authType deviceCode
```

Displays a code + URL (`https://aka.ms/devicelogin`). User enters code in browser. Useful for remote/headless environments where browser cannot open automatically. This is also what a bare `m365 login` does.

## 3. Username + Password

```bash
m365 login --authType password --userName user@contoso.com --password 'P@ssw0rd'
```

Only works for accounts WITHOUT MFA. Not recommended for production.

## 4. Certificate (App-only)

```bash
m365 login --authType certificate \
  --appId "APP_ID" \
  --tenant "TENANT_ID" \
  --certificateFile /path/to/cert.pfx \
  --password 'pfx-password'
```

For automation and CI/CD. Requires Azure Entra app registration with certificate uploaded.

PEM format also supported:

```bash
m365 login --authType certificate \
  --appId "APP_ID" \
  --tenant "TENANT_ID" \
  --certificateFile /path/to/cert.pem \
  --certificateBase64Encoded
```

## 5. Client Secret (App-only)

```bash
m365 login --authType secret \
  --appId "APP_ID" \
  --tenant "TENANT_ID" \
  --secret 'CLIENT_SECRET'
```

For automation. NOTE: Does NOT work for SharePoint operations, use certificate instead.

## Custom App Registration

By default, m365 CLI uses PnP's multi-tenant app. For custom app:

```bash
m365 login --appId "YOUR_APP_ID" --tenant "YOUR_TENANT_ID"
```

Or set up via:

```bash
m365 setup
```

## Managing Sessions

```bash
# Check current session
m365 status

# Log out
m365 logout

# Switch tenant (login to different tenant)
m365 login --appId "APP_ID" --tenant "OTHER_TENANT_ID"
```

## Permissions

Each command requires specific Microsoft Graph permissions. Check with:

```bash
m365 <command> --help permissions
```

### Two consent traps

Both of these look like a broken login and are not. Recognising them saves an hour of
re-authenticating against a wall that re-authenticating cannot move.

**A token only carries what was consented, not what was declared.** The CLI requests scopes with
`.default`, which means "everything already consented for this app". A permission added to the app
registration but never consented to is simply absent from the token. The call then fails with a
permission error while the Azure portal shows the permission sitting right there.

**Adding a permission does not re-prompt.** Entra shows the consent dialog the first time an app
asks for something. Once an admin has consented to the app, newly added permissions are granted
silently or not at all, and either way there is no prompt on your next sign-in. So logging out and
back in changes nothing, and the absence of a consent screen is not evidence that the permission
went through.

How to tell them apart, and what to do:

```bash
# What you actually hold right now, which is the only thing that decides a request
m365 util accesstoken get --resource https://graph.microsoft.com -o text | python3 -c '
import sys, base64, json
p = sys.stdin.read().strip().split(".")[1]
print(json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4)))["scp"].replace(" ", "\n"))'
```

The `=` padding matters: a JWT payload is base64url without padding, and a plain `base64 -d` fails
on it with a decode error that looks like a corrupt token.

If a scope is missing, ask an admin to **add the permission and click Grant admin consent** in the
same request. Reading the app registration yourself to check which half is missing needs
`Application.Read.All`, which an ordinary user does not have (it returns 403), so asking for both
at once is the fastest route.

Common permission sets:

| Service | Delegated | Application |
|---------|-----------|-------------|
| Teams (read) | `Team.ReadBasic.All`, `Channel.ReadBasic.All` | `Team.ReadBasic.All`, `Channel.ReadBasic.All` |
| Teams (write) | `Team.Create`, `Channel.Create` | `Team.Create`, `Channel.Create` |
| Teams (messages) | `ChannelMessage.Send`, `ChatMessage.Send` | `ChannelMessage.Read.All` (read only) |
| SharePoint | `AllSites.Read`, `AllSites.Write` | `Sites.Read.All`, `Sites.ReadWrite.All` |
| OneDrive | `MyFiles.Read`, `MyFiles.ReadWrite` | `Files.Read.All`, `Files.ReadWrite.All` |
