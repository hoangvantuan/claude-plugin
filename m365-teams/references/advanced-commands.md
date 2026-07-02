# Advanced Teams Commands

## Tabs

```bash
# List tabs in a channel
m365 teams tab list --teamId "TEAM_ID" --channelId "CHANNEL_ID" -o json \
  --query '[].{id:id, name:displayName, webUrl:configuration.websiteUrl}'

# Get tab details
m365 teams tab get --teamId "TEAM_ID" --channelId "CHANNEL_ID" --id "TAB_ID" -o json

# Remove tab
m365 teams tab remove --teamId "TEAM_ID" --channelId "CHANNEL_ID" --id "TAB_ID" --force
```

## Meetings

```bash
# List meetings for current user
m365 teams meeting list -o json --query '[].{id:id, subject:subject, start:startDateTime, end:endDateTime}'

# List meetings for another user
m365 teams meeting list --userName "user@contoso.com" -o json

# Get meeting details (identify by join URL từ lời mời lịch — lệnh KHÔNG có --id)
m365 teams meeting get --joinUrl "https://teams.microsoft.com/l/meetup-join/..." -o json

# Attendance reports
m365 teams meeting attendancereport list --meetingId "MEETING_ID" -o json

# Transcripts
m365 teams meeting transcript list --meetingId "MEETING_ID" -o json
```

## Apps

```bash
# List apps trong app catalog của tenant (lệnh này liệt kê catalog apps, KHÔNG nhận --teamId)
m365 teams app list -o json --query '[].{id:id, name:displayName}'

# Install app
m365 teams app install --teamId "TEAM_ID" --id "APP_ID"

# Remove app
m365 teams app remove --teamId "TEAM_ID" --id "APP_ID" --force
```

## Team Settings

```bash
# Member settings
m365 teams membersettings list --teamId "TEAM_ID" -o json

# Guest settings
m365 teams guestsettings list --teamId "TEAM_ID" -o json

# Update member settings
m365 teams membersettings set --teamId "TEAM_ID" --allowCreateUpdateChannels true
```

## Call Records

```bash
# List call records (option đúng là --startDateTime / --endDateTime, KHÔNG phải --fromDateTime)
m365 teams callrecord list --startDateTime "2024-01-01" --endDateTime "2024-01-31" -o json

# Get call record
m365 teams callrecord get --id "RECORD_ID" -o json
```

## Cache

```bash
# Clear Teams cache (troubleshooting)
m365 teams cache remove
```
