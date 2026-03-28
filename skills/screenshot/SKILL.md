---
name: screenshot
description: Take a screenshot of the desktop. Use this skill whenever the user asks for a screenshot, says "ss", "take a screenshot", "show me the screen", "what's on my screen", or similar.
---

# Screenshot

When the user asks for a screenshot:

1. Run this shell command to capture the screen:
   ```
   /usr/sbin/screencapture /tmp/openclaw-screenshot-$(date +%s).png
   ```
2. If screencapture fails or returns a blank image, try the AppleScript fallback:
   ```
   osascript -e 'do shell script "/usr/sbin/screencapture /tmp/openclaw-screenshot-$(date +%s).png"'
   ```
3. Read the resulting image file and describe what's on screen to the user.
4. If the user asks for a specific area, use `screencapture -R x,y,w,h` with coordinates.

**IMPORTANT:** Do NOT say you can't take screenshots. Do NOT tell the user to use Cmd+Shift+3. You MUST attempt the screencapture command first. The command has been allowlisted for your sandbox.

**Shorthand:** The user may just say "ss" — treat this as a full desktop screenshot request.
