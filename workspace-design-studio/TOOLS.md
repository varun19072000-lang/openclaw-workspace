# TOOLS.md - DesignStudio Tools

## Image Generation (FREE - Hugging Face FLUX.1)

Generate an image:
```bash
HF_TOKEN="YOUR_HF_TOKEN_HERE" python3 /Users/varun_ssd/.openclaw/workspace/skills/generate_image_free.py \
  --prompt "YOUR DETAILED PROMPT" \
  --filename "/Users/varun_ssd/.openclaw/media/content/STORY-slide-N.png"
```

## Prompt Tips
- Include: "social media post design, clean modern layout"
- For text on image: describe the text you want rendered
- For carousels: "slide N of M, consistent design style"
- Dark backgrounds + bold text = best results
- Be specific: colors, style, layout, mood

## Output Directory
All content: /Users/varun_ssd/.openclaw/media/content/
