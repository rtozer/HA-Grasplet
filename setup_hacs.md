# Setting Up HACS (Home Assistant Community Store)

HACS isn't installed by default. Here's how to enable it:

## Method 1: Using Home Assistant Terminal Add-on (Recommended)

1. **Install Terminal Add-on** (if not already installed):
   - Go to **Settings** → **Add-ons** → **Add-on Store**
   - Search for "Terminal & SSH"
   - Install and start it

2. **Download and install HACS**:
   ```bash
   cd /config
   wget -O - https://get.hacs.xyz | bash -
   ```

3. **Restart Home Assistant**:
   - Go to **Settings** → **System** → **Restart**

4. **Add HACS Integration**:
   - Go to **Settings** → **Devices & Services** → **Add Integration**
   - Search for "HACS"
   - Follow the setup wizard

## Method 2: Manual Installation

1. **Download HACS**:
   - Download the latest release from: https://github.com/hacs/integration/releases
   - Extract the `hacs` folder to `/config/custom_components/`

2. **Restart Home Assistant**

3. **Add Integration** (same as above)

## Method 3: Using Your Current Setup

Since you have a development environment, you can install HACS directly:

```bash
# From your current terminal
cd /home/coder/.homeassistant/custom_components
wget https://github.com/hacs/integration/releases/latest/download/hacs.zip
unzip hacs.zip
rm hacs.zip
```

Then restart Home Assistant.

## After HACS is Installed

1. **Configure HACS**:
   - You'll need a GitHub account
   - Follow the authentication flow
   - HACS will appear in your sidebar

2. **Add Custom Repository** (for your Grasplet integration):
   - HACS → Integrations → ⋮ (three dots) → Custom repositories
   - Add: `https://github.com/rtozer/HA-Grasplet`
   - Category: Integration

## Why You Need HACS

- **Easy Installation**: One-click installation of custom integrations
- **Automatic Updates**: Get notified when updates are available
- **Community**: Access to thousands of custom integrations
- **Distribution**: Easy way to share your Grasplet integration

Let me know if you need help with any of these steps!