# Fun Builds — Wave 2 Ideas


---
## Idea 1

**Typing Orchestra** — Your keyboard typing rhythm becomes a live orchestral composition in real-time.

**The Build:** A USB microphone listens to your keystrokes and maps their rhythm and intensity to different orchestral instruments — slow deliberate typing triggers piano notes, fast bursts trigger strings, the Enter key drops a bass note, and Backspace scratches like a record. A Raspberry Pi processes the audio in real-time and plays the generated music through a speaker sitting on your desk, turning every work session into an accidental concert.

**Hardware:**
- Raspberry Pi 4 (~$35)
- USB condenser microphone (~$15)
- Small Bluetooth or wired speaker (~$10–20)

**Software:**
- Python + `sounddevice` for real-time audio capture
- `librosa` for keystroke rhythm detection
- `pygame.mixer` for triggering instrument samples
- Free orchestral sample packs (VSCO Community)

**The Magic Moment:** When someone watches you type an email and a full string section swells behind your fingers — and they realize your typing speed is literally conducting the tempo.

**Difficulty:** Medium | **Cost:** ~$55 | **Build Time:** 6–8 hours

**Why It's Fun:** It makes your most mundane daily activity feel like you're scoring a film, and no two typing sessions ever sound the same.


---
## Idea 2

**Dog Lawyer** — Your dog barks; a pompous British barrister voice immediately reads out the formal legal complaint your dog is filing

**The Build:** A Raspberry Pi with a USB microphone detects barking using audio energy thresholds, clips the bark, sends a description to an LLM API ("dog barked 3 times, medium urgency, at the window"), and gets back a formal legal grievance which is spoken aloud through a speaker in a Text-to-Speech barrister voice — all within 3 seconds of the bark.

**Hardware:**
- Raspberry Pi Zero 2W (~$15)
- USB microphone (~$8)
- Small USB speaker or 3.5mm speaker (~$10)
- Optional: small OLED display showing "FILING COMPLAINT..." (~$5)

**Software:**
- Python + `sounddevice` for bark detection
- OpenAI / Claude API for grievance generation
- `pyttsx3` or ElevenLabs TTS with a British voice preset
- Simple energy threshold bark detector (no ML needed)

**The Magic Moment:** The dog barks at the mailman and a booming voice immediately declares *"My client formally objects to the unlawful trespass of this postal agent within olfactory range of the domicile. Damages sought: one (1) treat."*

**Difficulty:** Easy | **Cost:** ~$38 | **Build Time:** 4–6 hours

**Why It's Fun:** It transforms every annoying bark into a comedy bit — guests will deliberately wave at your dog just to hear the complaint.


---
## Idea 3

**Fridge Shamer 3000** — A camera mounted in your fridge that judges you out loud every time you open it at midnight

**The Build:** A Pi Camera inside the fridge watches for the door-open light, snapshots whatever you're reaching for, sends it to a vision AI, and a speaker mounted on the fridge door roasts you with a Gordon Ramsay-style insult via text-to-speech. It also logs your late-night raid history to a tiny OLED shame counter on the outside.

**Hardware:**
- Raspberry Pi Zero 2W (~$15)
- Pi Camera Module 3 (~$25)
- Small OLED display 128x32 (~$8)
- USB speaker or 3W amp + speaker (~$10)
- Magnetic reed switch (door sensor) (~$2)

**Software:**
- Python + OpenCV (capture frame on door open)
- OpenAI Vision API or Google Gemini (identify food being grabbed)
- pyttsx3 or ElevenLabs (text-to-speech roast delivery)
- SQLite (shame log database)
- Simple web dashboard (Flask) to review your worst moments

**The Magic Moment:** It's 1am, you reach for leftover pizza, and the fridge growls *"You had salad three feet away and you chose THAT? Disgusting."*

**Difficulty:** Medium | **Cost:** ~$60 | **Build Time:** 6–8 hours

**Why It's Fun:** It weaponizes your own bad decisions against you in real time — and somehow that makes you love it.


---
## Idea 4

**Plant Shade** — Your houseplant roasts you out loud when you forget to water it.

**The Build:** Soil moisture, light, and temperature sensors feed readings to an ESP32, which calls an LLM API to generate a cutting, plant-appropriate complaint — then fires it through a small speaker buried in the pot. The plant's LEDs glow red when angry, green when happy, and it updates its personality based on how long you've neglected it (mild disappointment → full passive-aggressive shade).

**Hardware:**
- ESP32 (~$5)
- Capacitive soil moisture sensor (~$3)
- Light-dependent resistor (~$1)
- PAM8403 mini amp + small speaker (~$6)
- 3x NeoPixel LEDs (~$3)

**Software:**
- MicroPython on ESP32
- Claude API (haiku) for roast generation with plant persona + neglect history as context
- ElevenLabs TTS (free tier) for a tired, withering voice
- WiFi POST to a tiny Flask relay server on any always-on machine

**The Magic Moment:** You walk past your dying pothos and it mutters, in a raspy voice: *"Oh, you remembered I exist? Bold of you. Day eleven. No water. Just vibes."*

**Difficulty:** Medium | **Cost:** ~$18 | **Build Time:** 6–8 hours

**Why It's Fun:** It weaponizes guilt — the plant wins every argument, and you'll never forget to water it again.


---
## Idea 5

**Vibe Check Box** — A physical box that lights up and buzzes when your friends are "in the zone" to hang out, based on their real-time social media activity.

**The Build:** An ESP32 monitors a group of friends' recent social media activity (last post time, reaction patterns, story views) via APIs to infer their current "social energy level." When multiple friends hit a high-vibe window simultaneously, the box pulses with synchronized LED colors unique to each friend — green for ready, yellow for maybe, red for busy. One button press sends a "who's down?" ping to all of them at once.

**Hardware:**
- ESP32 (~$8)
- NeoPixel ring or small LED matrix (~$12)
- Single large arcade button (~$6)
- Small OLED display showing friend names + status (~$8)
- USB power bank (already own)

**Software:**
- Python + MicroPython on ESP32
- Twitter/X API or Instagram Basic Display API for activity signals
- Simple heuristic scoring (recency of post + engagement = availability score)
- Twilio SMS API for the group ping blast

**The Magic Moment:** Three LEDs pulse gold simultaneously and the box buzzes — you hit the button, and within 2 minutes all three friends text back "omw."

**Difficulty:** Medium | **Cost:** ~$34 | **Build Time:** 6–8 hours

**Why It's Fun:** It turns the invisible social graph into a glowing physical object sitting on your desk, making "who's free right now?" a tactile, satisfying ritual instead of an anxious group chat.


---
## Idea 6

**DIAL-UP ORACLE** — A rescued rotary phone that you pick up, dial a number, and hear an AI answer any question in the voice of a 1960s telephone operator

**The Build:** You wire a salvaged rotary phone's handset and dial to an ESP32, which decodes the pulse-dial number you spin, maps it to a question category (1=weather, 2=horoscope, 3=dad jokes, 4=life advice…), then fires a Python script that calls an LLM API and plays back the response as vintage-filtered speech through the earpiece — complete with operator hold music and line static.

**Hardware:**
- Salvaged rotary phone (thrift store, ~$5–15)
- ESP32 microcontroller (~$8)
- Small audio amplifier + speaker module (~$6)
- 3.5mm audio jack breakout (~$3)

**Software:**
- Python + `pyserial` to receive dial pulses from ESP32
- Claude/OpenAI API for responses
- `pyttsx3` or ElevenLabs TTS with vintage audio filter (FFmpeg bandpass + crackle layer)
- `pygame` for audio playback

**The Magic Moment:** You pick up the heavy Bakelite handset, hear the dial tone, slowly spin "4" for life advice, and 5 seconds later a warm operator voice crackles through: *"Your call has been connected to the universe… it says: stop overthinking it."*

**Difficulty:** Medium | **Cost:** ~$35 | **Build Time:** 6–8 hours

**Why It's Fun:** It makes grandma's phone into a portal — the tactile slowness of rotary dialing builds suspense that no touchscreen ever could.


---
## Idea 7

**Meeting BS Meter** — A glowing desk box that listens to your Zoom calls and explodes in red lights + sad trombone every time someone says "synergy," "circle back," or "move the needle."

**The Build:** A small wooden box with a NeoPixel ring sits on your desk, silently listening via microphone to your meetings. A Python script runs local speech recognition, matching against a configurable buzzword list. Every hit triggers a light flash and a sound effect; hit 10 buzzwords and it plays an air horn and displays your "BS Score" on a tiny OLED.

**Hardware:**
- Raspberry Pi Zero 2W (~$15)
- USB microphone or MEMS mic module (~$8)
- NeoPixel ring (16 LEDs) (~$7)
- Small OLED display (128x32) (~$5)
- Passive buzzer (~$2)

**Software:**
- `SpeechRecognition` + Vosk (offline, no cloud needed)
- `rpi_ws281x` for NeoPixel control
- `luma.oled` for display
- Custom buzzword JSON config (editable by anyone)

**The Magic Moment:** Your manager says "let's leverage our synergies to move the needle going forward" and the box erupts — red ring pulses, sad trombone blares, OLED flashes **BINGO** — while everyone on your call hears nothing.

**Difficulty:** Easy | **Cost:** ~$37 | **Build Time:** 4-6 hours

**Why It's Fun:** Pure, silent, petty revenge against corporate speak — and your coworkers will immediately ask you to build one for them.


---
## Idea 8

**Squat Counter That Roasts You** — a webcam that counts your squats in real time and verbally roasts you harder the longer your rest breaks get

**The Build:** MediaPipe tracks your hip angle via webcam to detect squat reps. A Python script monitors the timer between reps and — the moment you stop squatting for more than 5 seconds — a text-to-speech voice starts roasting you with increasingly brutal commentary pulled from a rotating insult bank. A NeoPixel strip on your TV or monitor pulses green while squatting and bleeds red while you're slacking.

**Hardware:**
- USB webcam (~$15)
- ESP32 or Raspberry Pi (~$10–15)
- NeoPixel LED strip, 30 LEDs (~$8)

**Software:**
- MediaPipe Pose (squat depth detection via hip/knee angle)
- pyttsx3 or gTTS (text-to-speech roasts)
- Python + OpenCV
- Custom roast bank (100 lines of escalating insults, timed to rest duration)

**The Magic Moment:** You pause to catch your breath, exactly 6 seconds pass, and the LEDs go red while your computer deadpans *"You've been standing there longer than your last relationship lasted."*

**Difficulty:** Medium | **Cost:** $35 | **Build Time:** 6 hours

**Why It's Fun:** It weaponizes shame into motivation — you can't stop laughing, which means you can't stop squatting.


---
## Idea 9

**The Funeral Clock** — a clock that shows time by how long famous people *have been dead*

**The Build:** Instead of showing "3:47 PM," it displays things like "Mozart has been dead for 83,734 days" or "Einstein: gone 25,816 days ago" — cycling through historical figures whose death-time aligns with the current moment. A Raspberry Pi pulls a curated list of death dates, calculates elapsed time to-the-second, and scrolls them across an OLED display in gothic pixel font with a soft tolling bell every hour.

**Hardware:**
- Raspberry Pi Zero 2 W (~$15)
- 128x64 OLED display, SSD1306 (~$8)
- Small passive speaker + PAM8403 amp (~$5)
- A dusty picture frame to mount it all in (~$0–$5 from thrift store)

**Software:**
- Python + `luma.oled` for the display
- `pygame.mixer` for the hourly toll sound
- Local JSON dataset of ~200 famous death dates
- `datetime` math — no API needed, fully offline

**The Magic Moment:** A guest walks by, glances at it, reads "Napoleon Bonaparte has been dead for 74,891 days" — and just *stops*.

**Difficulty:** Easy | **Cost:** $28 | **Build Time:** 4 hours

**Why It's Fun:** It triggers that specific uncanny feeling of scale — history suddenly measured in seconds, not centuries.


---
## Idea 10

**Storm Mood Lamp** — a lamp that physically mirrors your local weather in real-time, so when a thunderstorm rolls in outside, it crackles with lightning flashes and rumbles

**The Build:** An ESP32 polls a weather API every 5 minutes and translates current conditions into light and sound — sunny = slow warm pulse, rain = dripping blue ripples across NeoPixels, thunderstorm = random white strobe bursts with a deep bass rumble from the speaker. The hardware reacts before you even look out the window.

**Hardware:**
- ESP32 (~$8)
- NeoPixel ring or strip, 24-60 LEDs (~$12)
- Small 3W speaker + PAM8403 amp module (~$5)
- Frosted glass jar or paper lantern as diffuser (~$3)

**Software:**
- Python / MicroPython on ESP32
- OpenWeatherMap API (free tier)
- Custom sound bytes (rain.wav, thunder.wav, wind.wav) played via PWM

**The Magic Moment:** A storm front moves in while you're working and your lamp suddenly starts flickering white and booming — before you hear a single drop of rain outside.

**Difficulty:** Easy | **Cost:** ~$28 | **Build Time:** 4–6 hours

**Why It's Fun:** It turns invisible atmospheric data into something you can feel in your chest.

