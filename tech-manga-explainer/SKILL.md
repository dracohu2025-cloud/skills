---
name: tech-manga-explainer
description: Generates technical educational manga that explains complex technical concepts through dialogue format. Use when users request "explain tech with manga", "generate tech manga", "draw this concept as manga", "manga tutorial", "explain XXX with manga" or similar requests. Suitable for n8n, Kubernetes, AI, programming, architecture and other technical topics. Generates images via nanobanana + Gemini API.
invocable: user
---

# Tech Manga Explainer

Transforms complex technical concepts into easy-to-understand content using manga dialogue format.

## Core Features

- **Target Audience**: Adult tech learners, programming beginners, non-technical people interested in technology
- **Expression Format**: Manga dialogue, expert guides novice, Q&A style
- **Art Style Options**: Japanese manga, minimalist lines, cyberpunk, hand-drawn sketch
- **Character Combinations**: Multiple character sets supported, default Naruto mentor-student (Kakashi & Naruto)
- **Applicable Topics**: Programming, architecture, AI, automation, cloud-native, databases, and other technical concepts

## Character Consistency Rules (Important)

All manga pages must maintain completely consistent character appearances. Each page prompt automatically includes full character cards.

### Available Character Groups

| Character Group | Parameter | Mentor | Student | Style Features |
|-----------------|-----------|--------|---------|----------------|
| Naruto Mentor-Student | `--preset naruto` | Kakashi | Naruto | Passionate training, mentor-student tradition, progressive learning (default) |
| Programmer Duo | `--preset coder` | Ma Shu (Uncle Code) | Xiao Xin (Little Xin) | Workplace daily life, relaxed humor |

### Default Character Card: Naruto Mentor-Student

**Kakashi - Technical Mentor**
```
FACE & HEAD:
- Japanese male ninja, around 30 years old, tall and lean
- HAIR: Spiky SILVER/WHITE hair, gravity-defying, pointing up and left
- LEFT EYE: Covered by TILTED forehead protector (hitai-ate)
- RIGHT EYE: Relaxed, half-lidded, slightly bored
- MASK: ALWAYS wearing dark navy blue FACE MASK covering nose and mouth

CLOTHING (NEVER CHANGES):
- HEAD: Konoha forehead protector worn TILTED to cover left eye
- TOP: Green/olive JONIN VEST (flak jacket) with scroll pouches
- UNDER: Dark navy blue long-sleeve shirt with built-in mask
- PANTS: Dark navy blue ninja pants
- SHOES: Standard blue ninja sandals

Must-have features: Silver spiky hair, tilted forehead protector covering left eye, dark blue face mask, green vest, lazy gaze
```

**Naruto - Passionate Learner**
```
FACE & HEAD:
- Japanese male ninja, around 16 years old (Shippuden era)
- HAIR: Bright SPIKY BLONDE/YELLOW hair, messy, sticking out everywhere
- EYES: Big bright BLUE eyes, very expressive
- FACE: THREE WHISKER MARKS on each cheek (6 total)

CLOTHING (NEVER CHANGES - Shippuden outfit):
- HEAD: Konoha forehead protector worn on FOREHEAD (black cloth)
- TOP: Orange and BLACK TRACKSUIT jacket with zipper
- INSIDE: Black t-shirt visible at collar
- PANTS: Orange tracksuit pants
- SHOES: Black ninja sandals
- ACCESSORIES: Small green crystal necklace

Must-have features: Golden spiky hair, blue eyes, 3 whisker marks on each cheek, orange-black tracksuit, forehead protector worn straight
```

### Alternative Character Card: Programmer Duo

**Ma Shu (Uncle Code) - Technical Mentor**
```
Must-have features: Balding with hair on sides, silver-framed glasses, red-black plaid shirt, gray hoodie bunched at neck, goatee
```

**Xiao Xin (Little Xin) - Technical Newbie**
```
Must-have features: Mushroom-cut black hair, black zip-up hoodie open, white t-shirt, gray backpack with pixel robot keychain
```

## Workflow

### Step 1: Technical Concept Analysis and Page Count Determination

1. Understand the technical concept user wants explained
2. **REQUIRED: Analyze content complexity, determine appropriate page count based on standards below (never default to 6 pages)**
3. Break down knowledge points, design Q&A dialogue for each
4. Determine suitable metaphors and analogies (can use ninja techniques to analogize technical concepts)

#### Page Count Determination Standards (Mandatory)

**Core Principle**:
- DO NOT default to 6 pages without analyzing content
- MUST count core concepts first, then calculate page count with formula
- MUST include "complexity justification" in planning

**Calculation Formula**:
```
Total Pages = Introduction(1 page) + Core Concepts x 1.5 pages + Summary(1 page)

Example: 3 core concepts -> 1 + 3x1.5 + 1 = 6.5 -> round to 6-7 pages
Example: 7 core concepts -> 1 + 7x1.5 + 1 = 12.5 -> round to 12-13 pages
```

| Complexity | Page Range | Core Concepts | Criteria | Examples |
|------------|------------|---------------|----------|----------|
| Simple | 3-4 pages | 1-2 | Single concept, no deep principles needed | "What is an API", "Environment Variables" |
| Medium | 5-8 pages | 3-5 | Needs principle + application explanation | "Docker Intro", "What is RAG" |
| Complex | 9-15 pages | 6-10 | Multiple interconnected sub-concepts | "K8s Architecture Full Guide", "Transformer Principles" |
| Systematic | 15-25 pages | 10+ | Complete tutorial or paper explanation | "Understanding LLMs from Scratch", "Complete Paper Analysis" |

**Determination Process (Mandatory)**:
1. List core concepts/knowledge points to explain
2. Count how many core concepts
3. Determine complexity and page range based on table above
4. Explicitly state justification in planning

### Step 2: Manga Structure Planning

**Must output plan first, wait for user confirmation before generating images.**

#### Planning Mandatory Requirements

1. **No combining pages**: Cannot write "Pages 2-3", must plan each page individually
2. **Must include trial-and-error section**: At least 1 page of "Naruto makes mistake -> Kakashi corrects"
3. **Technical diagrams must be manga-ized**: Cannot write abstract descriptions, must translate to concrete visuals

Output planning format:

```
## Manga Plan

Topic: [Technical concept name]
Complexity: [Simple/Medium/Complex/Systematic] - [Justification]
Total Pages: [X pages]
Art Style: [manga/minimal/cyberpunk/sketch]
Character Group: [naruto/coder] - Default Naruto mentor-student

### Core Metaphor
[Main metaphor] = [Ninja technique/Naruto world element]
Reason: [Why this metaphor fits]
Example: Docker = Sealing scroll, sealing the entire environment inside, can be summoned anywhere anytime

### Knowledge Point Breakdown (each concept on separate line)
1. [Knowledge point 1] - Page X
2. [Knowledge point 2] - Page X
3. [Trial-and-error section] Naruto's misunderstanding - Page X <- Must have this line
4. ...

### Page 1 - Introduction
- Scene: [Specific scene, e.g., Konoha Village intelligence analysis room, Naruto frustrated with scrolls]
- Naruto: "[Start with catchphrase, e.g., Dammit!/Kakashi-sensei!]..."
- Kakashi: "[Start with catchphrase, e.g., Well well...]..."
- Visual elements: [Specific visual elements]

### Page 2 - [Knowledge Point 1 Title]
- Scene: [Specific scene]
- Naruto: "..."
- Kakashi: "..."
- Technical diagram: [Manga-ized description, e.g., Kakashi holding three scrolls labeled Q/K/V, arrows converging to glowing result sphere]
- Visual elements: [Specific visual elements]

### Page X - Naruto's Misunderstanding [REQUIRED]
- Scene: [Naruto confidently attempts something]
- Naruto: "Oh! I get it! It's just XXX right! (starts messing around)"
- Kakashi: "Wait... you haven't..."
- Visual elements: [Failure/explosion/error effects]

### Page X+1 - Kakashi Corrects
- Scene: [Kakashi seriously explaining]
- Kakashi: "No no no. The key point is..."
- Naruto: "So that's how it is..."
- Technical diagram: [Correct understanding visualization]
- Visual elements: [Contrast between wrong and right approach]

### Page N - Summary and Application
- Scene: [Success scene, e.g., Training ground at sunset]
- Naruto: "Oh! I get it! [Summarizes in own words with ninja analogy]"
- Kakashi: "Well, that's about right (flips open orange book)"
- Visual elements: [Achievement, growth atmosphere]
```

**After planning, ask user**:
> This is the manga structure plan, X pages total (including 1 trial-and-error learning section). Confirm to proceed with image generation, or let me know what needs adjustment.

### Step 3: Generate Manga Images

Generate page by page using script:

```bash
# Default using Kakashi & Naruto
python3 /mnt/skills/user/tech-manga-explainer/scripts/generate_tech_manga.py \
  --style manga \
  --prompt "Konoha training ground, Kakashi explaining at whiteboard" \
  --dialogue "Naruto:What exactly is this Docker thing!|Kakashi:Well well, think about why ninjas carry scrolls on missions?" \
  --tech-diagram "Docker container structure diagram" \
  --output page_01.png

# Use programmer character group
python3 /mnt/skills/user/tech-manga-explainer/scripts/generate_tech_manga.py \
  --preset coder \
  --style manga \
  --prompt "Office scene, Ma Shu at whiteboard" \
  --dialogue "Xiao Xin:What's a Pod?|Ma Shu:Think of it like a shipping container..." \
  --output page_01.png
```

## Art Style Parameters

| Style Code | Style Name | Features | Suitable Topics |
|------------|------------|----------|-----------------|
| manga | Japanese Manga | Clear lines, halftone backgrounds, dynamic expressions | Universal, most recommended |
| minimal | Minimalist Lines | Black and white, extremely simple, professional feel | Architecture, process explanations |
| cyberpunk | Cyberpunk | Neon colors, tech feel, dark tones | AI, cloud-native, future tech |
| sketch | Hand-drawn Sketch | Casual relaxed, like whiteboard drawings | Quick prototypes, brainstorming |

## Character Group Parameters

| Character Group | Parameter | Features | Dialogue Style |
|-----------------|-----------|----------|----------------|
| naruto | `--preset naruto` | Passionate training, mentor-student tradition | Naruto asks impulsively, Kakashi answers lazily |
| coder | `--preset coder` | Workplace daily, relaxed humor | Xiao Xin asks humbly, Ma Shu explains patiently |

## Script Parameters

```bash
python3 generate_tech_manga.py [options]

Required:
  --prompt       Scene description

Core Parameters:
  --dialogue     Dialogue content, format: Character:Content|Character:Content
  --preset       Character group [naruto|coder], default naruto (Kakashi & Naruto)
  --style        Art style [manga|minimal|cyberpunk|sketch], default manga

Optional:
  --tech-diagram Technical diagram description to show in image
  --output       Output filename, default tech_manga_page.png
  --size         Image size, default 1024x1024 (recommend portrait 768x1024)
  --show-prompt  Only show prompt, don't generate image
  --list-styles  List all available styles
  --list-presets List all available character groups
```

## Usage Examples

### Example 1: Kakashi & Naruto Explain Docker (Default Characters)

```bash
# Page 1 - Introduction
python3 generate_tech_manga.py \
  --style manga \
  --prompt "Konoha training ground, Naruto frustrated at computer, Kakashi walks over lazily" \
  --dialogue "Naruto:Kakashi-sensei! What the heck is this Docker! Been working on it all day with errors!|Kakashi:Well well, don't panic. Think about it, why do ninjas carry scrolls on missions?" \
  --output docker_01.png

# Page 2 - Core Metaphor
python3 generate_tech_manga.py \
  --style manga \
  --prompt "Kakashi pulls out a scroll showing seal patterns" \
  --dialogue "Naruto:Because...can summon needed weapons anytime?|Kakashi:Exactly. Docker is your sealing scroll, seal the entire runtime environment inside, can perfectly restore anywhere" \
  --tech-diagram "Inside scroll sealed: code + dependencies + config = container" \
  --output docker_02.png

# Page 3 - Understanding Confirmation
python3 generate_tech_manga.py \
  --style manga \
  --prompt "Naruto's eyes light up, fists clenched, Kakashi's eyes smiling" \
  --dialogue "Naruto:Oh! I get it! It's like sealing Shadow Clone technique in a scroll, can use it anywhere!|Kakashi:That's about right (flips open orange book)" \
  --output docker_03.png
```

### Example 2: Programmer Duo Explain Kubernetes Pod

```bash
python3 generate_tech_manga.py \
  --preset coder \
  --style manga \
  --prompt "Office scene, Xiao Xin scratching head at computer, Ma Shu walks over with coffee cup" \
  --dialogue "Xiao Xin:Uncle Ma, what exactly is a Pod? The docs are giving me a headache|Ma Shu:Let me give you an analogy" \
  --output k8s_pod_01.png
```

### Example 3: Cyberpunk Style Explaining AI Agent

```bash
python3 generate_tech_manga.py \
  --style cyberpunk \
  --prompt "Neon-lit future city background, Kakashi and Naruto standing before holographic projection" \
  --dialogue "Naruto:What's the difference between AI Agent and regular chatbots?|Kakashi:Agents can think, plan, and take action on their own, like the difference between Jonin and Genin" \
  --tech-diagram "Agent loop: Perceive->Think->Plan->Execute" \
  --output agent_01.png
```

## Dialogue Design Tips

Good technical manga dialogue should:

### Naruto Mentor-Student Style (Default)

#### Character Speech Patterns (Must Follow)

**Kakashi's speech habits:**
- Catchphrase: "Well well...", "Well, that's about right"
- Tone: Lazy, unhurried, but hits the point when needed
- Feature: Likes using rhetorical questions to guide thinking, occasionally flips orange book
- Common phrases:
  - "Well well, don't panic. Think about..."
  - "That's why...(sigh)"
  - "No no, you misunderstood. The key is..."
  - "That's about right (eyes smiling)"

**Naruto's speech habits:**
- Catchphrase: "I'm telling you!", "Dammit!", "Oh! I get it!"
- Tone: Passionate, impulsive, easily excited
- Feature: Often makes mistakes first then understands, likes summarizing in own words
- Common phrases:
  - "Kakashi-sensei! What the heck is this XXX!"
  - "Dammit! Error again!"
  - "Wait... I think I kinda get it... so it's..."
  - "Oh! I get it! It's like XXX!"

#### Trial-and-Error Learning Must Be Included

**Naruto's core is growth, every tutorial should have Naruto mistake->correction bridge:**

```
[Trial-and-Error Template]

Page X - Naruto's Misunderstanding (Must have this page)
- Scene: Naruto confidently tries, result fails
- Naruto: "I get it! It's just XXX right! (starts messing around)"
- Kakashi: "Wait... you haven't learned the basics yet..."
- Visual elements: Naruto overconfident -> explosion/error effects

Page X+1 - Kakashi Corrects
- Scene: Kakashi explains correct approach
- Kakashi: "No no no. You misunderstood the key point. XXX isn't YYY, but ZZZ."
- Naruto: "So that's how it is... then how should I do it?"
- Visual elements: Kakashi seriously explaining, Naruto humbly listening
```

### Programmer Duo Style

**Ma Shu's speech habits:**
- Tone: Patient, humorous, occasionally self-deprecating
- Feature: Likes life-like analogies, drinks coffee
- Common phrases: "Let me give you an analogy...", "I stepped on the same pitfall back then..."

**Xiao Xin's speech habits:**
- Tone: Curious, humble, occasionally silly
- Feature: Takes notes carefully, likes confirming understanding
- Common phrases: "So you're saying...", "Wait, let me sort this out..."

### Universal Principles

- **Max 3 dialogue exchanges per page**: Manga is visual medium, too much text crowds the image
- **No combining pages**: Must plan each page individually, cannot write "Pages 2-3"
- **At least 1 page per concept**: Better to split more than compress

## Technical Diagram Design (Manga-ized)

Technical diagrams cannot be too abstract, must be translated to manga scenes:

### Wrong Approach (Too Abstract)
```
Technical diagram: Attention weight calculation graph (Query, Key, Value)
```

### Correct Approach (Manga-ized)
```
Technical diagram: Three Naruto clones each holding scrolls labeled "Q/K/V",
arrows converging to a glowing result sphere in the center,
labeled "attention score" on the side
```

## Step 4: Generate Interactive HTML Manga (Mandatory)

**After all images are generated, must generate an interactive HTML file** integrating all pages into a browseable manga tutorial.

### Template Files

Template files are in `assets/` directory:

```
assets/
├── manga_template.html      # Main template (full page structure, dark tech style)
├── page_template.html       # Single page template (loop generate each page)
└── dialogue_template.html   # Dialogue template (character dialogue blocks)
```

### Generation Requirements

1. **File naming**: `[topic]_manga.html`
2. **Image references**: Use relative paths to reference generated images
3. **Code highlighting**: Wrap technical terms in `<code>` tags
4. **Technical points**: Display each page's core knowledge point separately
5. **Responsive**: Ensure mobile viewing works properly

### Completion Message

After generating HTML, inform user:
> All done! Generated [N] images and 1 interactive HTML file.
>
> Files:
> - page_01.png ~ page_0N.png (manga images)
> - [topic]_manga.html (interactive manga, open in browser)
>
> Tip: Place HTML file and all images in same folder, open HTML in browser to read the complete manga tutorial.

## Dependencies

- nanobanana skill (provides Gemini image generation capability)
- Python 3
- Environment variable: GEMINI_API_KEY configured via nanobanana
