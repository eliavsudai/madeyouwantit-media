import json
TAGS = "#smallbusinessmarketing #instagramtips #reelstips #contentstrategy #smallbusiness"
PAY = [
 {"say": "That's what we build into every account we run.", "scene": {"kind": "work", "title": "Our work"}},
 {"say": "Want it done for you? DM *DAILY*. Your first ad is free.", "scene": {"kind": "end"}},
]
def cap(hook, lesson, source):
    return "\n".join([hook, "", *lesson, "", f"Source: {source}", "", "This is exactly what we build into every account we run.",
                      "Save this for your next post.", "First ad free · DM 'DAILY'", "", TAGS])
S = []
S.append({
 "id": "s01", "type": "reach", "audience": "Small brands",
 "hook": "Followers don't decide your reach. 3 signals do.",
 "lines": [
  {"say": "Followers don't decide who sees your reel. *Three* signals do.",
   "scene": {"kind": "hook", "label": "Small brands", "headline": "Followers don't decide your reach. *3* signals do."}},
  {"say": "Adam Mosseri, the head of Instagram, named them in January.",
   "scene": {"kind": "quote", "quote": "The top three signals that matter most for ranking are *watch time,* *likes* and *sends.*",
             "who": "Adam Mosseri", "role": "Head of Instagram · Jan 2025"}},
  {"say": "*Watch* *time*. *Likes* per reach. And *sends* per reach.",
   "scene": {"kind": "icons", "kinds": ["clock", "heart", "send"], "names": {"clock": "watch time", "heart": "likes / reach", "send": "sends / reach"}, "highlight": None}},
  {"say": "So which one puts you in front of strangers?",
   "scene": {"kind": "feed", "speed": 1100}},
  {"say": "*Sends*. A share in someone's DMs.",
   "scene": {"kind": "icons", "kinds": ["clock", "heart", "send"], "names": {"clock": "watch time", "heart": "likes / reach", "send": "sends / reach"}, "highlight": "send", "hl_at": 0.1}},
  {"say": "He says likes count slightly more with your *followers*, and sends count slightly more with people who *don't* follow you yet.",
   "scene": {"kind": "icons", "kinds": ["heart", "send"], "names": {"heart": "likes / your followers", "send": "sends / new people"}, "highlight": "send", "hl_at": 3.2, "title": "Where each counts more", "title_size": 80, "note": "Per Adam Mosseri, Jan 2025"}},
  {"say": "So before you post, ask one question.",
   "scene": {"kind": "statement", "font": "anton", "text": "Before you post:"}},
  {"say": "Would someone *send* this to a friend?",
   "scene": {"kind": "statement", "font": "anton", "size": 150, "text": "Would someone *send* this to a friend?"}},
  *PAY],
 "sources": [
  {"claim": "Top three ranking signals: watch time, likes, sends; track average watch time, likes per reach, sends per reach.",
   "source": "Adam Mosseri, via Social Media Today", "url": "https://www.socialmediatoday.com/news/instagram-shares-algorithm-2025/738034/", "date": "2025-01-22"},
  {"claim": "Likes slightly more important for connected content, sends slightly more important for unconnected content.",
   "source": "Adam Mosseri, via Social Media Today", "url": "https://www.socialmediatoday.com/news/instagram-shares-algorithm-2025/738034/", "date": "2025-01-22"}],
 "work": ["a_pin.jpg", "b_forever.jpg", "c_holdsup.jpg"],
 "caption": cap("Followers don't decide your reach. 3 signals do.",
   ["1. Watch time  2. Likes per reach  3. Sends per reach",
    "Likes weigh a bit more with your followers. Sends weigh a bit more with people who don't follow you yet.",
    "Before you post, ask: would someone send this to a friend?"],
   "Adam Mosseri, Head of Instagram (via Social Media Today, Jan 2025)")})
S.append({
 "id": "s02", "type": "hooks", "audience": "Product businesses",
 "hook": "Your reel gets judged in 3 seconds. Here's what decides it.",
 "lines": [
  {"say": "Your reel gets judged in *three* seconds.",
   "scene": {"kind": "hook", "label": "Product businesses", "headline": "Your reel gets judged in *3* seconds."}},
  {"say": "Instagram actually measures it.",
   "scene": {"kind": "quote", "size": 68, "quote": "Skip rate is the percentage of views from people who decided to skip your reel during those *first 3 seconds.*",
             "who": "Instagram", "role": "Reels insights · Aug 2025"}},
  {"say": "It's called *skip* *rate*. It's in your Insights, next to every reel.",
   "scene": {"kind": "timeline", "max": 10, "mark": 3, "mark_label": "SKIP ZONE", "title": "Skip rate", "play_speed": 1.2}},
  {"say": "So what makes someone stay past second *three*?",
   "scene": {"kind": "feed", "speed": 1300, "stop_at": 1.6, "stop_card": 4, "labels": {"4": "3 MISTAKES"}}},
  {"say": "Not your logo. Not a slow hello.",
   "scene": {"kind": "compare", "weak": "Hi everyone! Welcome back to our page, today we want to share", "strong": "*3* mistakes that make people skip your bakery", "verdict_at": 1.0}},
  {"say": "Three things, in the very first frame.",
   "scene": {"kind": "list", "title": "In the first frame", "items": ["Say who it's *for*", "Put a *number* in the headline", "Flip a *belief* they hold"]}},
  {"say": "Say who it's *for*."},
  {"say": "Put a *number* in the headline."},
  {"say": "And flip a *belief* they already hold."},
  {"say": "Look at the first frame of this reel. It did all three.",
   "scene": {"kind": "list", "reveal": "time", "every": 0.7, "title": "This reel's first frame", "items": ["Who: *product businesses*", "Number: *3* seconds", "Belief flipped: *you have time*"]}},
  *PAY],
 "sources": [
  {"claim": "Skip rate = percentage of views that skipped the reel in the first 3 seconds; replaced view rate (Aug 2025).",
   "source": "Instagram, via Social Media Today", "url": "https://www.socialmediatoday.com/news/instagram-adds-retention-insights-reels/758464/", "date": "2025-08-24"},
  {"claim": "Instagram's tip for reaching new audiences: hook viewers fast, within the first few seconds.",
   "source": "Instagram Creators blog", "url": "https://creators.instagram.com/blog/instagram-recommendations-eligibility-tips-creators", "date": "2023-04-25"}],
 "work": ["a_pin.jpg", "b_forever.jpg", "c_holdsup.jpg"],
 "caption": cap("Your reel gets judged in 3 seconds.",
   ["Instagram's skip rate = % of viewers who swipe away in the first 3 seconds. It's in your Insights for every reel.",
    "In the very first frame: say who it's for, put a number in the headline, flip a belief they hold.",
    "No logo intro. No slow hello."],
   "Instagram reel insights (via Social Media Today, Aug 2025); Instagram Creators")})
json.dump({"scenarios": S}, open("/home/claude/lessons/scen/s01_02.json", "w"), indent=1, ensure_ascii=False)
