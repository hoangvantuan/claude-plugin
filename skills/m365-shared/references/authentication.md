# Authentication Methods

## 1. Browser Flow (Default — Recommended)

```bash
m365 login
# or explicitly:
m365 login --authType browser
```

Opens browser for interactive sign-in. Works with MFA and conditional access policies.

## 2. Device Code Flow

```bash
m365 login --authType deviceCode
```

Displays a code + URL (`https://aka.ms/devicelogin`). User enters code in browser. Useful for remote/headless environments where browser cannot open automatically.

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

For automation. NOTE: Does NOT work for SharePoint operations — use certificate instead.

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

Common permission sets:

| Service | Delegated | Application |
|---------|-----------|-------------|
| Teams (read) | `Team.ReadBasic.All`, `Channel.ReadBasic.All` | `Team.ReadBasic.All`, `Channel.ReadBasic.All` |
| Teams (write) | `Team.Create`, `Channel.Create` | `Team.Create`, `Channel.Create` |
| Teams (messages) | `ChannelMessage.Send`, `ChatMessage.Send` | `ChannelMessage.Read.All` (read only) |
| SharePoint | `AllSites.Read`, `AllSites.Write` | `Sites.Read.All`, `Sites.ReadWrite.All` |
| OneDrive | `MyFiles.Read`, `MyFiles.ReadWrite` | `Files.Read.All`, `Files.ReadWrite.All` |
