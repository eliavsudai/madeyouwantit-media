import json
TAGS = "#smallbusinessmarketing #instagramtips #reelstips #contentstrategy #smallbusiness"
WORK = ["a_pin.jpg", "b_forever.jpg", "c_holdsup.jpg"]
PAY = [
 {"say": "That's what we build into every account we run.", "scene": {"kind": "work", "title": "Our work"}},
 {"say": "Want it done for you? DM *DAILY*. Your first ad is free.", "scene": {"kind": "end"}},
]
SRC = {
 "SMT25": ("Adam Mosseri, via Social Media Today", "https://www.socialmediatoday.com/news/instagram-shares-algorithm-2025/738034/", "2025-01-22"),
 "SEJ24": ("Adam Mosseri, via Search Engine Journal", "https://searchenginejournal.com/instagram-algorithm-shift-why-sends-matter-more-than-ever/", "2024-07-03"),
 "ORIG": ("Instagram Creators: Helping creators find new audiences (originality)", "https://creators.instagram.com/recommendations-and-Originality", "2024-04-30"),
 "TC24": ("TechCrunch, on Instagram's ranking update", "https://techcrunch.com/2024/04/30/instagram-is-updating-its-ranking-systems-to-surface-more-original-content/", "2024-04-30"),
 "SMT26": ("Adam Mosseri, via Social Media Today", "https://www.socialmediatoday.com/news/instagram-chief-shares-algorithm-insights-and-posting-tips/", "2026-09-24"),
 "SMTQA": ("Adam Mosseri Q&A, via Social Media Today", "https://www.socialmediatoday.com/news/instagram-chief-answers-creator-questions/744813/", "2025-04-08"),
 "ELIG": ("Instagram Creators: recommendations eligibility tips", "https://creators.instagram.com/blog/instagram-recommendations-eligibility-tips-creators", "2023-04-25"),
 "RET": ("Instagram reel insights, via Social Media Today", "https://www.socialmediatoday.com/news/instagram-adds-retention-insights-reels/758464/", "2025-08-24"),
 "BIZ": ("Instagram for Business: Get discovered with Reels", "https://business.instagram.com/instagram-reels", "checked 2026-10"),
 "NIELSEN": ("Instagram Business blog citing Nielsen (c. 2015)", "https://business.instagram.com/blog/coming-soon-view-counts-on-videos", "c. 2015"),
 "FB16": ("Meta Newsroom (Facebook research, 2016)", "https://about.fb.com/es/news/2016/02/capta-la-atencion-con-nuevas-funcionalidades-para-anuncios-de-video/", "2016-02-10"),
 "BI": ("Adam Mosseri interview, Business Insider", "https://www.yahoo.com/news/instagram-head-adam-mosseri-paradigm-100002931.html", "2026"),
 "TRIAL": ("Instagram Creators: Trial reels", "https://creators.instagram.com/blog/instagram-trial-reels", "2024-12-10"),
 "TRIAL25": ("Instagram, via Social Media Today", "https://socialmediatoday.com/news/instagram-trial-reels-increase-reach-tests/750121/", "2025-06-08"),
 "TRIAL1K": ("Adam Mosseri, via Social Media Today", "https://www.socialmediatoday.com/news/instagram-expands-access-trial-reels/752895/", "2025-07-13"),
 "BUFFER": ("Buffer, analysis of 2.1M posts", "https://buffer.com/resources/how-often-to-post-on-instagram/", "2025-08-13"),
 "SPROUT24": ("Sprout Social 2024 Content Strategy Report", "https://sproutsocial.com/insights/data/2024-social-content-strategy-report/", "2024"),
 "SPROUT25": ("Sprout Social Index 2025", "https://sproutsocial.com/insights/index/", "2025"),
 "HASH": ("Instagram, via Social Media Today", "https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808300/", "2025-12-18"),
 "LEN": ("Adam Mosseri, via Storyboard18", "https://www.storyboard18.com/digital/instagram-extends-reels-to-three-minutes-and-updates-profile-grid/", "2025-01-21"),
}


def src(*keys):
    return [{"source": SRC[k][0], "url": SRC[k][1], "date": SRC[k][2]} for k in keys]


def cap(hook, lesson, source):
    return "\n".join([hook, "", *lesson, "", f"Source: {source}", "", "This is exactly what we build into every account we run.",
                      "Save this for your next post.", "First ad free · DM 'DAILY'", "", TAGS])


def S(id, type, audience, hook, lines, sources, caption):
    return {"id": id, "type": type, "audience": audience, "hook": hook, "lines": lines + PAY, "sources": sources,
            "work": WORK, "caption": caption}


def H(label, headline, say):
    return {"say": say, "scene": {"kind": "hook", "label": label, "headline": headline}}


def L(say, **scene):
    return {"say": say, "scene": scene} if scene else {"say": say}


SC = []

# s03 — retention: the retention chart
SC.append(S("s03", "retention", "Small brands", "1 line in your Insights shows exactly where people leave.", [
  H("Small brands", "*1* line in your Insights shows where people *leave*.", "One line in your Insights shows exactly where people leave your reel."),
  L("It's the *retention* chart. Every reel has one.", kind="curve", pts=[[0, 100], [3, 55], [10, 40], [20, 31], [30, 25]], title="Retention", note="Illustration"),
  L("Instagram says it will always slope *down*."),
  L("But the *flatter* the line, the more engaged your audience is.", kind="curve", title="Flatter = more engaged",
    curves=[{"pts": [[0, 100], [3, 45], [10, 28], [20, 18], [30, 12]], "color": "ink", "label": "steep"},
            {"pts": [[0, 100], [3, 78], [10, 66], [20, 58], [30, 52]], "color": "red", "label": "flat"}], note="Illustration"),
  L("And it matters. Watch time is one of Instagram's top *three* ranking signals.", kind="icons", kinds=["clock", "heart", "send"],
    names={"clock": "watch time", "heart": "likes / reach", "send": "sends / reach"}, highlight="clock", hl_at=1.2),
  L("So where does yours drop?", kind="curve", pts=[[0, 100], [3, 50], [12, 44], [16, 26], [30, 21]], title="Read the drop",
    marks=[{"x": 2, "label": "hook", "at": 0.6}, {"x": 14, "label": "the wait", "at": 2.4}], note="Illustration"),
  L("A cliff in the first seconds means the *hook* missed."),
  L("A slide in the middle means you made them *wait*."),
  L("Fix the second where it drops. Not the whole video.", kind="statement", font="anton", size=140, text="Fix the *second* it drops."),
 ], src("RET", "SMT25"),
 cap("1 line in your Insights shows exactly where people leave your reel.",
     ["It's the Retention chart. Instagram: it always slopes down, but the flatter the line, the more engaged your audience.",
      "Cliff at the start = the hook missed. Slide in the middle = you made them wait.",
      "Watch time is one of Instagram's top 3 ranking signals."],
     "Instagram reel insights (Aug 2025); Adam Mosseri (Jan 2025), via Social Media Today")))

# s04 — shares: sends per reach
SC.append(S("s04", "shares", "Product businesses", "Instagram's boss keeps pointing at 1 number.", [
  H("Product businesses", "Instagram's boss keeps pointing at *1* number.", "Instagram's boss keeps pointing at *one* number."),
  L("*Sends* per *reach*.", kind="statement", font="anton", size=170, text="*Sends* ÷ reach"),
  L("Out of everyone who saw your post, how many sent it to a friend in a DM?", kind="quote", size=66,
    quote="One of the most important signals we use in ranking is *sends per reach.*", who="Adam Mosseri", role="Head of Instagram · 2024"),
  L("And DMs are where sharing lives now.", kind="list", reveal="time", every=0.6, title="Where posts get shared most", items=["*DMs*", "Stories", "Feed"]),
  L("He says way more posts get shared into *DMs* than into Stories, and more into Stories than into the feed."),
  L("So what makes someone hit *send*?", kind="feed", speed=1200, stop_at=1.4, stop_card=4, labels={"4": "THIS IS YOU"}),
  L("Something *useful* they'll need later. Or something that's *exactly* their friend."),
  L("Make the post someone sends with three words: *this* *is* *you*.", kind="statement", font="anton", size=150, text="“This is *you*.”"),
 ], src("SEJ24", "BI"),
 cap("Instagram's boss keeps pointing at 1 number: sends per reach.",
     ["Out of everyone who saw your post, how many sent it to a friend in a DM?",
      "Mosseri: way more posts get shared into DMs than into Stories, and more into Stories than into the feed.",
      "Make the post someone sends with 3 words: this is you."],
     "Adam Mosseri (Search Engine Journal, 2024; Business Insider interview)")))

# s05 — teach, don't sell
SC.append(S("s05", "teach", "Small brands", "2 in 3 people say the best brand content isn't an ad.", [
  H("Small brands", "*2 in 3* people say the best brand content *isn't an ad*.", "Two in three people say the most engaging brand content isn't an ad."),
  L("In a Sprout Social survey of more than *four thousand five hundred* people,", kind="counter", to=4500, suffix="+", label="people surveyed · Sprout Social", over=1.4),
  L("two-thirds picked content that *educates* and *entertains*.", kind="statement", font="anton", size=150, text="*Educate* + entertain"),
  L("In Sprout's 2025 Index, *polished*, *product-centric* content ranked *least* important.", kind="list", reveal="time", every=0.6,
    title="What people value (2025)", items=["*Relatable*", "*Authentic*", "*Entertaining*", "Polished & product-centric: last"]),
  L("And salesy messaging made the list of turn-offs."),
  L("So what do you post instead?", kind="feed", speed=1100),
  L("Teach the thing you know better than anyone.", kind="statement", font="serif", size=110, text="Teach what you know *better than anyone.*"),
  L("A florist: how to keep tulips standing. A bakery: why the crust crackles.", kind="compare", weak="New bouquets in store now! Come visit us", strong="Why your tulips *droop* (and the *1* fix)", weak_label="AD", strong_label="LESSON", verdict_at=1.4),
  L("The product shows up at the end, as the *answer*."),
 ], src("SPROUT24", "SPROUT25"),
 cap("2 in 3 people say the most engaging brand content isn't an ad.",
     ["Two-thirds of 4,500+ people chose content that educates AND entertains.",
      "In the 2025 Index, polished, product-centric content ranked least important; salesy messaging turns people off.",
      "Teach what you know best. Let the product be the answer at the end."],
     "Sprout Social 2024 Content Strategy Report; Sprout Social Index 2025")))

# s06 — testing & consistency
SC.append(S("s06", "testing", "Small brands", "Posting 3–5 times a week: about 12% more reach per post.", [
  H("Small brands", "Post *3–5x* a week: about *+12%* reach per post.", "Posting three to five times a week got about *twelve* percent more reach per post."),
  L("That's from Buffer's analysis of *2.1 million* posts.", kind="counter", to=2.1, decimals=1, suffix="M", label="posts analyzed · Buffer, 2025", over=1.2),
  L("Compared with posting once or twice a week, reach per post climbed.", kind="bars", title="Reach per post vs 1–2 posts/week", unit="%",
    bars=[{"label": "1–2 posts a week", "value": 0.001, "text": "baseline"}, {"label": "3–5 posts a week", "value": 12, "text": "+12%"},
          {"label": "10+ posts a week", "value": 24, "text": "+24%", "color": "red"}], maxv=30, note="Source: Buffer, Aug 2025"),
  L("About *twelve* percent at three to five. About *twenty-four* at ten or more."),
  L("Weekly follower growth more than *doubled*.", kind="bars", title="Weekly follower growth", bars=[
    {"label": "1–2 posts a week", "value": 0.12, "text": "0.12%"}, {"label": "3–5 posts a week", "value": 0.26, "text": "0.26%", "color": "red"}], maxv=0.35, note="Source: Buffer, Aug 2025"),
  L("So is it just volume?", kind="statement", font="anton", size=160, text="Just volume?"),
  L("Not quite. Mosseri's advice: *experiment*, and post as much as you can without burning out.", kind="statement", font="serif", size=104, text="Experiment. Post as much as you can. *Avoid burnout.*", sub="Adam Mosseri's advice, 2026 (paraphrased)"),
  L("Every post is a try. The tries are how you find the one that *takes* *off*."),
 ], src("BUFFER", "SMT26"),
 cap("Posting 3–5 times a week: about 12% more reach per post.",
     ["Buffer looked at 2.1M posts: vs 1–2 posts/week, reach per post was ~+12% at 3–5 and ~+24% at 10+.",
      "Weekly follower growth more than doubled (0.12% → 0.26%).",
      "Mosseri: experiment, post as much as you can, avoid burnout."],
     "Buffer (Aug 2025); Adam Mosseri via Social Media Today (2026)")))

# s07 — product example: candle shop
SC.append(S("s07", "product", "Candle shops", "How a candle shop turns 1 candle into 3 reels people send.", [
  H("Candle shops", "*1* candle. *3* reels people actually *send*.", "Here's how a candle shop could turn *one* candle into *three* reels people send."),
  L("Reel one: a fix. 'Why your candle tunnels, and how to stop it.'", kind="compare", weak="Our new candle is here! Shop now", strong="Why your candle *tunnels* (and the fix)", weak_label="AD", strong_label="REEL 1", verdict_at=1.6),
  L("Reel two: a myth. 'Three things that shorten a candle's life.'", kind="compare", weak="20% off all candles this weekend", strong="*3* things that shorten your candle's life", weak_label="AD", strong_label="REEL 2", verdict_at=1.6),
  L("Reel three: a number from your own shop. 'How long one batch really takes.'", kind="compare", weak="Handmade with love", strong="One batch takes *X* hours. Here's why", weak_label="AD", strong_label="REEL 3", verdict_at=1.6),
  L("Notice what's missing? The pitch.", kind="statement", font="anton", size=160, text="No pitch."),
  L("Each one teaches first, and the candle appears at the end, as the *answer*."),
  L("Why it works: sends count slightly more with people who *don't* follow you yet.", kind="icons", kinds=["heart", "send"],
    names={"heart": "likes / your followers", "send": "sends / new people"}, highlight="send", hl_at=1.0, title="Where each counts more", title_size=80),
  L("People send tips. They don't send ads.", kind="statement", font="serif", size=120, text="People send *tips.* Not ads."),
 ], src("SMT25"),
 cap("1 candle → 3 reels people send.",
     ["1) A fix: why your candle tunnels. 2) A myth: 3 things that shorten its life. 3) Your own number: how long one batch takes.",
      "Teach first; the candle is the answer at the end.",
      "Sends weigh slightly more with people who don't follow you yet. People send tips, not ads."],
     "Adam Mosseri, Head of Instagram (via Social Media Today, Jan 2025)")))

# s08 — hooks: name the audience + number
SC.append(S("s08", "hooks", "Founders", "Same reel, 2 hooks. Only 1 gets watched.", [
  H("Founders", "Same reel. *2* hooks. Only *1* gets watched.", "Same reel, *two* hooks. Only one gets watched."),
  L("Instagram's own tip for reaching new people: hook viewers *fast*.", kind="quote", size=72, quote="Hook viewers fast: capture attention within the *first few seconds.*", who="Instagram Creators", role="Tips for reaching new audiences"),
  L("Here's the weak one.", kind="compare", weak="Hey guys, so today I wanted to talk a little about our coffee", strong="", verdict_at=99),
  L("Here's the strong one.", kind="compare", weak="Hey guys, so today I wanted to talk a little about our coffee", strong="Café owners: *3* reasons your latte photos get skipped", verdict_at=1.2),
  L("What changed? *Three* things.", kind="list", title="What changed", items=["It names *who* it's for", "It has a *number*", "It promises a *payoff*"]),
  L("It names *who* it's for."),
  L("It has a *number*."),
  L("And it promises a *payoff* you can only get by staying."),
  L("Write the hook last. It's the only part *everyone* sees.", kind="statement", font="anton", size=140, text="Write the hook *last.*"),
 ], src("ELIG", "RET"),
 cap("Same reel, 2 hooks. Only 1 gets watched.",
     ["Weak: 'Hey guys, so today I wanted to talk about…'",
      "Strong: 'Café owners: 3 reasons your latte photos get skipped.'",
      "Name who it's for. Use a number. Promise a payoff. Instagram's own tip: hook viewers in the first few seconds."],
     "Instagram Creators (recommendation tips); Instagram reel insights")))

# s09 — reach: originality
SC.append(S("s09", "reach", "Small brands", "Post 2 identical videos and Instagram recommends only 1.", [
  H("Small brands", "*2* identical videos? Instagram recommends only *1*.", "Post the same video as someone else, and Instagram recommends only *one* of them."),
  L("Its own words: when it finds identical content, it recommends only the *original*.", kind="quote", size=66,
    quote="When we find two or more identical pieces of content on Instagram, we will only recommend *the original one.*", who="Instagram Creators", role="Originality update · Apr 2024"),
  L("And accounts that keep reposting other people's videos can be left out of recommendations *entirely*.", kind="feed", speed=1000),
  L("Visible *watermarks* from other apps hurt too.", kind="statement", font="anton", size=140, text="No *watermarks.*"),
  L("Here's the part that helps you.", kind="statement", font="serif", size=110, text="Here's the part that *helps you.*"),
  L("Instagram said big accounts and repost pages used to get most of the reach,"),
  L("and it changed ranking to give smaller, *original* creators an *equal* footing.", kind="bars", title="Reach goes to the original", bars=[
    {"label": "Reposted copy", "value": 1, "text": "replaced"}, {"label": "Your original", "value": 3, "text": "recommended", "color": "red"}], maxv=4.2, note="Illustration · per Instagram, Apr 2024"),
  L("So film your own product. Your way. Small is not a disadvantage anymore."),
 ], src("ORIG", "TC24"),
 cap("Post 2 identical videos and Instagram recommends only 1: the original.",
     ["Accounts that mostly repost others' content can be excluded from recommendations; visible watermarks hurt eligibility.",
      "Instagram changed ranking (Apr 2024) to give smaller, original creators an equal footing.",
      "Make your own. Small is not a disadvantage."],
     "Instagram Creators (Apr 2024); TechCrunch")))

# s10 — retention: first 3 and 10 seconds (Nielsen, dated)
SC.append(S("s10", "retention", "Product businesses", "Up to 47% of a video's value lands in the first 3 seconds.", [
  H("Product businesses", "Up to *47%* of a video's value lands in the first *3* seconds.", "Up to *forty-seven* percent of a video's value can land in the first *three* seconds."),
  L("That's from Nielsen data Instagram shared on its business blog, back in 2015.", kind="quote", size=70, quote="Up to *47%* of the value of a video campaign was delivered in the *first three seconds.*", who="Instagram Business blog", role="Citing Nielsen · c. 2015"),
  L("And up to *seventy-four* percent in the first *ten*.", kind="bars", title="Share of value delivered", unit="%", bars=[
    {"label": "First 3 seconds", "value": 47, "text": "up to 47%", "color": "red"}, {"label": "First 10 seconds", "value": 74, "text": "up to 74%"}], maxv=100, note="Nielsen via Instagram, c. 2015"),
  L("Old numbers. But Instagram still measures the first three seconds today, with *skip* *rate*.", kind="timeline", max=10, mark=3, mark_label="SKIP RATE", title="Still measured today"),
  L("So what goes in those seconds?", kind="statement", font="anton", size=160, text="So what goes there?"),
  L("Your *best* *moment*. Not your setup.", kind="compare", weak="So I started this business back in 2019 and", strong="This is what *0.5 seconds* of crema looks like", weak_label="SETUP", strong_label="BEST MOMENT", verdict_at=1.4),
  L("Lead with the result, then show how you got there."),
 ], src("NIELSEN", "RET"),
 cap("Up to 47% of a video's value can land in the first 3 seconds.",
     ["Nielsen data via Instagram (c. 2015): up to 47% of a video campaign's value in the first 3 s; up to 74% in the first 10 s.",
      "Today Instagram still tracks those first 3 seconds as 'skip rate'.",
      "Lead with your best moment, not your setup."],
     "Instagram Business blog citing Nielsen (c. 2015); Instagram reel insights (2025)")))

# s11 — product example: bakery
SC.append(S("s11", "product", "Bakeries", "Your bakery doesn't need more product shots. It needs 1 question answered.", [
  H("Bakeries", "Your bakery doesn't need more product shots. It needs *1* answer.", "Your bakery doesn't need more product shots. It needs *one* question answered."),
  L("The question your customers already ask you at the counter.", kind="statement", font="serif", size=110, text="What do they ask you *at the counter?*"),
  L("'Why is your sourdough so sour?' 'How do I keep a croissant crisp?'", kind="list", reveal="time", every=1.0, title="Questions = reels",
    items=["Why is sourdough *sour*?", "How do I keep it *crisp*?", "Why does bread go *stale*?"]),
  L("Each answer is a reel."),
  L("Hook: the question, with a number. 'Croissants: *three* mistakes that make them soggy.'", kind="compare", weak="Fresh croissants every morning!", strong="Croissants: *3* mistakes that make them *soggy*", weak_label="PRODUCT SHOT", strong_label="ANSWER", verdict_at=1.4),
  L("Then the answer, step by step. Then your croissant, at the end, as the proof."),
  L("Instagram's own business advice says it plainly: connect by teaching people something *new*.", kind="quote", size=74, quote="Connect with your audience by *teaching them something new.*", who="Instagram for Business", role="Get discovered with Reels"),
  L("Your counter is a list of reels waiting to be made.", kind="statement", font="anton", size=140, text="Your counter = your *content plan.*"),
 ], src("BIZ"),
 cap("Your bakery doesn't need more product shots. It needs 1 question answered.",
     ["The questions customers ask at the counter are your next reels.",
      "Hook = the question + a number. Body = the answer. Ending = your product as proof.",
      "Instagram's business advice: connect by teaching people something new."],
     "Instagram for Business, 'Get discovered with Reels'")))

# s12 — shares: what makes a post worth sending
SC.append(S("s12", "shares", "Small brands", "Likes reach your followers. Sends reach everyone else.", [
  H("Small brands", "Likes reach your *followers*. Sends reach *everyone else*.", "Likes help you reach your followers. *Sends* help you reach everyone else."),
  L("Mosseri's words: likes are slightly more important for connected content,", kind="quote", size=64,
    quote="Likes are slightly more important for connected content, and *sends* are slightly more important for *unconnected content.*", who="Adam Mosseri", role="Head of Instagram · Jan 2025"),
  L("and *sends* are slightly more important for people who don't know you yet."),
  L("So the question isn't 'will they like it?'", kind="statement", font="anton", size=150, text="Not: will they *like* it?"),
  L("It's 'who would they send it *to*?'", kind="statement", font="anton", size=150, text="But: who would they *send* it *to*?"),
  L("Three kinds of posts get sent.", kind="list", title="Posts that get sent", items=["A *fix* they need", "A *truth* about their life", "A *plan* to share"]),
  L("A fix someone needs."),
  L("A truth about someone's life."),
  L("Or a plan to do together. 'We should go here.'"),
 ], src("SMT25", "SEJ24"),
 cap("Likes reach your followers. Sends reach everyone else.",
     ["Mosseri: likes weigh slightly more for connected content; sends weigh slightly more for unconnected content.",
      "Ask 'who would they send this to?' instead of 'will they like it?'",
      "Posts that get sent: a fix they need, a truth about their life, a plan to share."],
     "Adam Mosseri (Social Media Today, Jan 2025; Search Engine Journal, 2024)")))

# s13 — hooks: sound-off / captions
SC.append(S("s13", "hooks", "Product businesses", "41% of video ads made no sense without sound.", [
  H("Product businesses", "*41%* of video ads made no sense *without sound*.", "In a Facebook study, *forty-one* percent of video ads made no sense with the sound off."),
  L("That was Facebook's own research, in 2016.", kind="counter", to=41, suffix="%", label="of video ads meaningless on mute · Facebook, 2016", over=1.2),
  L("The same research found *captions* raised view time by about *twelve* percent.", kind="bars", title="Captions vs no captions", unit="%", bars=[
    {"label": "No captions", "value": 100, "text": "view time"}, {"label": "With captions", "value": 112, "text": "+12%", "color": "red"}], maxv=130, note="Facebook internal tests, 2016"),
  L("So what does your reel say on mute?", kind="feed", speed=1100, stop_at=1.2, stop_card=4, labels={"4": "ON MUTE?"}),
  L("Instagram's business guide says: use *voiceover* and *timed* *text* to reinforce your message.", kind="quote", size=74, quote="Use *voiceover and timed text* to reinforce your message.", who="Instagram for Business", role="Get discovered with Reels"),
  L("Notice this reel. Every line I say is on screen.", kind="statement", font="anton", size=150, text="Every word. *On screen.*"),
  L("If it works on mute, it works everywhere."),
 ], src("FB16", "BIZ"),
 cap("41% of video ads made no sense without sound.",
     ["Facebook's 2016 research: 41% of video ads were meaningless on mute; captions raised view time ~12%.",
      "Instagram's business guide: use voiceover AND timed text.",
      "If it works on mute, it works everywhere."],
     "Meta Newsroom (Facebook research, 2016); Instagram for Business")))

# s14 — teach: Instagram's own advice to businesses
SC.append(S("s14", "teach", "Small brands", "Instagram's own advice for businesses isn't 'post your product'.", [
  H("Small brands", "Instagram's own advice for businesses *isn't* 'post your product'.", "Instagram's own advice for businesses isn't 'post your product'."),
  L("Its business site says *entertaining* *storytelling* drives discovery.", kind="quote", size=80, quote="*Entertaining storytelling* drives discovery for your business.", who="Instagram for Business", role="Get discovered with Reels"),
  L("And to connect, *teach* people something new.", kind="statement", font="serif", size=120, text="*Teach* them something new."),
  L("Meanwhile, in Sprout Social's 2025 survey, people ranked *polished*, product-centric content *last*.", kind="list", reveal="time", every=0.6, title="What people want (2025)", items=["Relatable", "Authentic", "Entertaining", "*Polished product posts: last*"]),
  L("So why do most small brands still post product shots?", kind="feed", speed=1000),
  L("Because they're easy. And easy is what everyone else is posting too."),
  L("Try this: one lesson your product *proves*. Then show the product.", kind="compare", weak="New collection now available. Link in bio", strong="Why your white tee turns *yellow* (and how to stop it)", weak_label="PRODUCT POST", strong_label="LESSON", verdict_at=1.4),
 ], src("BIZ", "SPROUT25"),
 cap("Instagram's own advice for businesses isn't 'post your product'.",
     ["Instagram for Business: entertaining storytelling drives discovery; teach people something new.",
      "Sprout Social Index 2025: people ranked polished, product-centric content least important.",
      "Post one lesson your product proves. Then show the product."],
     "Instagram for Business; Sprout Social Index 2025")))

# s15 — reach: small creators shown to non-followers
SC.append(S("s15", "reach", "Small brands", "Small account? Instagram says it tests you on people who don't follow you.", [
  H("Small brands", "Small account? Instagram tests your posts on *strangers*.", "Small account? Instagram says it shows your public posts to people who *don't* follow you."),
  L("In 2026 Mosseri described it as one of *four* ranking principles.", kind="list", reveal="time", every=0.6, title="Mosseri's 4 principles (2026)", items=["Originality", "Recency", "*Breaking new creators*", "Bigger models"]),
  L("Instagram shows small creators' posts to non-followers to see how people *respond*."),
  L("Your first audience isn't your followers. It's *strangers*.", kind="feed", speed=900),
  L("Which means your post has to make sense to someone who's *never* heard of you.", kind="compare", weak="Restock day!! You know what that means", strong="The *1* sweater rule nobody tells you", weak_label="INSIDE JOKE", strong_label="STRANGER-READY", verdict_at=1.4),
  L("No inside jokes. No 'you know what day it is'."),
  L("Write every reel for the person seeing you for the *first* *time*.", kind="statement", font="anton", size=140, text="Write for the *first* time."),
 ], src("SMT26"),
 cap("Small account? Instagram shows your public posts to people who don't follow you, to see how they respond.",
     ["Mosseri (2026): 'breaking new creators' is one of four ranking principles, with originality, recency and bigger models.",
      "Your first audience is strangers. Make every reel make sense to someone who's never heard of you.",
      "No inside jokes."],
     "Adam Mosseri, via Social Media Today (Sep 2026)")))

# s16 — testing: trial reels
SC.append(S("s16", "testing", "Small brands", "80% of creators who tried this saw more reach from non-followers.", [
  H("Small brands", "*80%* of creators who tried this got more reach from *strangers*.", "Eighty percent of creators who tried this saw more reels reach from non-followers."),
  L("It's called *trial* *reels*. Instagram launched it in December 2024.", kind="statement", font="anton", size=170, text="Trial *reels*"),
  L("A trial reel goes to people who *don't* follow you first. Your followers don't see it.", kind="feed", speed=900),
  L("After about *twenty-four* hours you see how it did.", kind="timeline", max=72, mark=24, mark_label="RESULTS", label_every=12, title="Trial reel timeline", play_speed=20),
  L("If it does well within *seventy-two* hours, it can be shared with your followers automatically."),
  L("Instagram says *forty* percent of creators who tried it started posting reels more often.", kind="bars", title="Creators who tried trial reels", unit="%", bars=[
    {"label": "Posted reels more often", "value": 40, "text": "40%"}, {"label": "More reach from non-followers", "value": 80, "text": "80%", "color": "red"}], maxv=100, note="Instagram, Jun 2025"),
  L("The catch: you need a public account with at least *one* *thousand* followers.", kind="counter", to=1000, label="followers to unlock trial reels", over=1.0),
  L("Until then, every normal post is your trial. Treat it like one."),
 ], src("TRIAL", "TRIAL25", "TRIAL1K"),
 cap("80% of creators who tried trial reels saw more reach from non-followers.",
     ["Trial reels go to non-followers first. Results after ~24 h; can auto-share to followers if it does well within 72 h.",
      "Instagram: 40% of creators who tried them started posting reels more often.",
      "Needs a public account with 1,000+ followers. Until then, every post is your trial."],
     "Instagram Creators (Dec 2024); Instagram via Social Media Today (Jun & Jul 2025)")))

# s17 — product example: an app
SC.append(S("s17", "product", "App makers", "Your app demo gets skipped. Here's the 1 change.", [
  H("App makers", "Your app demo gets skipped. Here's the *1* change.", "Your app demo gets skipped. Here's the *one* change that fixes it."),
  L("Most app reels start with the app. Logo, home screen, features.", kind="compare", weak="Introducing our new app! Here's the home screen", strong="", weak_label="TYPICAL DEMO", verdict_at=99),
  L("But viewers don't care about your app yet. They care about their *problem*."),
  L("So start with the problem, as a hook with a number.", kind="compare", weak="Introducing our new app! Here's the home screen", strong="You've opened *4* apps to plan *1* dinner", weak_label="TYPICAL DEMO", strong_label="PROBLEM FIRST", verdict_at=1.4),
  L("Then teach the fix in *three* steps."),
  L("Your app shows up at step three, doing the boring part for them."),
  L("Instagram measures the first *three* seconds as skip rate. The problem is what makes people stay.", kind="timeline", max=10, mark=3, mark_label="SKIP ZONE", title="Problem in the skip zone"),
  L("Problem first. App last.", kind="statement", font="anton", size=170, text="Problem *first.* App *last.*"),
 ], src("RET", "ELIG"),
 cap("Your app demo gets skipped. Here's the 1 change: start with the problem.",
     ["Hook = their problem + a number ('You've opened 4 apps to plan 1 dinner').",
      "Teach the fix in 3 steps; your app appears at step 3.",
      "Instagram's skip rate measures the first 3 seconds; the problem is what makes people stay."],
     "Instagram reel insights (Aug 2025); Instagram Creators")))

# s18 — retention: what makes people wait (curiosity line)
SC.append(S("s18", "retention", "Founders", "The flatter your retention line, the more engaged your audience. 1 sentence flattens it.", [
  H("Founders", "*1* sentence in the middle keeps people watching.", "*One* sentence in the middle of your reel keeps people watching."),
  L("Instagram's retention chart always slopes down. The *flatter*, the better.", kind="curve", title="The middle is where people drift",
    curves=[{"pts": [[0, 100], [3, 70], [12, 58], [16, 38], [30, 26]], "color": "ink", "label": "no hook mid-way"}], marks=[{"x": 14, "label": "the drift", "at": 1.6}], note="Illustration"),
  L("Most reels lose people in the *middle*. The hook worked. Then nothing new happens."),
  L("The fix is a *curiosity* *line*. A question you promise to answer.", kind="statement", font="serif", size=110, text="“So what actually makes someone *stop*?”"),
  L("Like: 'So what actually makes someone stop?'"),
  L("It resets attention, because now they want the answer.", kind="curve", title="With a curiosity line",
    curves=[{"pts": [[0, 100], [3, 70], [12, 58], [16, 38], [30, 26]], "color": "ink", "label": "without"},
            {"pts": [[0, 100], [3, 70], [12, 58], [16, 54], [30, 46]], "color": "red", "label": "with"}], marks=[{"x": 14, "label": "curiosity line", "at": 1.0}], note="Illustration"),
  L("Then answer it. Don't fake it."),
  L("This reel had one. You just watched it work.", kind="statement", font="anton", size=140, text="You just watched it *work.*"),
 ], src("RET"),
 cap("1 sentence in the middle of your reel keeps people watching.",
     ["Instagram's retention chart always slopes down; the flatter, the more engaged your audience.",
      "Reels lose people mid-way when nothing new happens. Add a curiosity line: a question you promise to answer.",
      "Then actually answer it."],
     "Instagram reel insights, via Social Media Today (Aug 2025)")))

# s19 — hooks: 0.25 seconds recall
SC.append(S("s19", "hooks", "Product businesses", "People can remember your post after 0.25 seconds.", [
  H("Product businesses", "People can remember your post after *0.25* seconds.", "People can remember a post they saw for a quarter of a second."),
  L("That's from Facebook's 2016 research on mobile feeds.", kind="counter", to=0.25, decimals=2, suffix="s", label="enough to recall feed content · Facebook, 2016", over=1.0),
  L("Even when they scroll right past, your *first* *frame* gets a fraction of a second in their head.", kind="feed", speed=1500),
  L("So what's in yours?", kind="statement", font="anton", size=170, text="What's in yours?"),
  L("If it's a blurry pan or a black screen, that's what they remember.", kind="compare", weak="", strong="Florists: *1* trick for longer-lasting tulips", weak_label="BLURRY PAN", strong_label="READABLE FRAME", verdict_at=1.4),
  L("Make the first frame readable on its own. Who it's for, a *number*, a *claim*."),
  L("Even the people who scroll will leave with your *idea*.", kind="statement", font="serif", size=120, text="Even scrollers leave with your *idea.*"),
 ], src("FB16"),
 cap("People can remember a post they saw for just 0.25 seconds.",
     ["Facebook's 2016 mobile feed research: content could be recalled after a quarter of a second.",
      "Your first frame works even on people who scroll past.",
      "Make it readable on its own: who it's for, a number, a claim."],
     "Meta Newsroom (Facebook research, 2016)")))

# s20 — shares: DMs paradigm shift
SC.append(S("s20", "shares", "Small brands", "More posts get shared in DMs than in Stories. Most brands design for the wrong one.", [
  H("Small brands", "More posts get shared in *DMs* than in *Stories*.", "More posts get shared into DMs than into Stories."),
  L("That's Adam Mosseri. He calls it a *paradigm* *shift*.", kind="quote", size=70, quote="There are *way more* photos and videos shared into DMs than into stories.", who="Adam Mosseri", role="Head of Instagram · interview"),
  L("And more into Stories than into the feed.", kind="list", reveal="time", every=0.6, title="Where sharing happens", items=["*DMs*", "Stories", "Feed"]),
  L("So picture your post landing in a group chat.", kind="feed", speed=900),
  L("Does it need *you* to explain it? Then it won't get sent."),
  L("Make it *self-explaining*: the hook, the point, and the proof, all inside the post.", kind="list", title="Group-chat ready", items=["Hook says *who* it's for", "Point fits *one* line", "Proof is *in* the post"]),
  L("A friend should get it without opening your profile."),
 ], src("BI"),
 cap("More posts get shared into DMs than into Stories.",
     ["Mosseri: way more photos and videos are shared into DMs than Stories, and more into Stories than the feed.",
      "Picture your post landing in a group chat. Does it explain itself?",
      "Hook says who it's for. Point fits one line. Proof is inside the post."],
     "Adam Mosseri, Business Insider interview")))

# s21 — product example: clothing brand
SC.append(S("s21", "product", "Clothing brands", "Stop posting the outfit. Post the 1 mistake it fixes.", [
  H("Clothing brands", "Stop posting the outfit. Post the *1* mistake it fixes.", "Stop posting the outfit. Post the *one* mistake it fixes."),
  L("A flat lay says 'new arrival'. Nobody sends that to a friend.", kind="compare", weak="New arrivals. Shop the drop", strong="", weak_label="FLAT LAY", verdict_at=99),
  L("A mistake says 'this is you'. People send that.", kind="compare", weak="New arrivals. Shop the drop", strong="*3* fit mistakes that make jeans look *cheap*", weak_label="FLAT LAY", strong_label="THE MISTAKE", verdict_at=1.2),
  L("Here's the format.", kind="list", title="The format", items=["Hook: the *mistake* + a number", "Show *why* it happens", "The *fix*: your piece"]),
  L("Hook: the mistake, with a number."),
  L("Then *why* it happens, in plain words."),
  L("Then the fix. That's where your piece appears."),
  L("And sends matter: Mosseri says sends count slightly more with people who *don't* follow you yet.", kind="icons", kinds=["heart", "send"],
    names={"heart": "likes / your followers", "send": "sends / new people"}, highlight="send", hl_at=1.6, title="Where each counts more", title_size=80),
 ], src("SMT25"),
 cap("Stop posting the outfit. Post the 1 mistake it fixes.",
     ["Hook: the mistake + a number ('3 fit mistakes that make jeans look cheap').",
      "Then why it happens. Then the fix: your piece.",
      "Sends weigh slightly more with people who don't follow you yet, and people send mistakes, not flat lays."],
     "Adam Mosseri, Head of Instagram (via Social Media Today, Jan 2025)")))

# s22 — reach: eligibility checklist
SC.append(S("s22", "reach", "Small brands", "4 things that quietly stop Instagram from recommending your reel.", [
  H("Small brands", "*4* things that quietly stop Instagram from *recommending* you.", "*Four* things quietly stop Instagram from recommending your reel to new people."),
  L("All from Instagram's own creator guidelines.", kind="list", title="Not recommended if…", items=["Your account is *private*", "It's *longer* than 3 minutes", "It has *watermarks*", "It's a *copy*"]),
  L("One. A *private* account can't be recommended to non-followers."),
  L("Two. Reels have to be *three* minutes or less."),
  L("Three. Visible *watermarks* from other apps."),
  L("Four. Copies. Instagram recommends the *original*, not the repost."),
  L("You can check this yourself. Professional accounts have an *Account* *Status* page that shows if anything isn't eligible.", kind="statement", font="anton", size=130, text="Settings → *Account Status*"),
  L("Two minutes. Check it today."),
 ], src("ELIG", "ORIG"),
 cap("4 things that quietly stop Instagram from recommending your reel.",
     ["1) Private account 2) Reel longer than 3 minutes 3) Visible watermarks 4) Reposted copies (only the original gets recommended).",
      "Professional accounts can check Account Status to see if any content isn't eligible.",
      "Check it today."],
     "Instagram Creators (recommendation eligibility; originality, Apr 2024)")))

# s23 — teach: why lessons beat ads (originality + sprout)
SC.append(S("s23", "teach", "Product businesses", "The #2 thing that makes a brand stand out isn't price. It's originality.", [
  H("Product businesses", "The *#2* thing that makes a brand stand out? *Originality*.", "The number *two* thing people say makes a brand stand out on social is *originality*."),
  L("In Sprout Social's 2025 Index, only *product* *quality* ranked higher.", kind="list", reveal="time", every=0.7, title="What makes a brand stand out", items=["Product quality", "*Originality of content*"]),
  L("And original doesn't mean expensive. It means *yours*.", kind="statement", font="serif", size=120, text="Original means *yours.*"),
  L("Your process. Your numbers. The questions your customers ask you."),
  L("A lesson only *you* can teach is original by default.", kind="compare", weak="Trending audio + product shot", strong="What *we* learned from *300* orders this month", weak_label="COPYABLE", strong_label="ONLY YOU", verdict_at=1.4),
  L("And Instagram rewards that too. When content is identical, it recommends only the *original*."),
 ], src("SPROUT25", "ORIG"),
 cap("The #2 thing that makes a brand stand out on social: originality.",
     ["Sprout Social Index 2025: only product quality ranked higher.",
      "Original doesn't mean expensive. It means yours: your process, your numbers, your customers' questions.",
      "Instagram only recommends the original when content is identical."],
     "Sprout Social Index 2025; Instagram Creators (Apr 2024)")))

# s24 — hooks: the 1.7 second context (dated)
SC.append(S("s24", "hooks", "Small brands", "1.7 seconds: the average time people gave a mobile post (2016).", [
  H("Small brands", "*1.7* seconds. That's how long a mobile post got.", "One point seven seconds. That's how long people spent, on average, with a post on mobile."),
  L("Facebook measured it in 2016. On desktop it was *two* *point* *five*.", kind="bars", title="Avg time per post (2016)", unit="s", bars=[
    {"label": "Mobile", "value": 1.7, "text": "1.7s", "color": "red"}, {"label": "Desktop", "value": 2.5, "text": "2.5s"}], maxv=3.2, note="Facebook research, 2016"),
  L("That's an average, not a deadline. But it shows how *little* room you get.", kind="feed", speed=1500),
  L("So what fits in under *two* seconds?", kind="statement", font="anton", size=160, text="What fits in *1.7s*?"),
  L("Not a sentence. A *headline*.", kind="compare", weak="We are so excited to finally share something we've been working on", strong="*Bakers:* stop doing *this*", weak_label="SENTENCE", strong_label="HEADLINE", verdict_at=1.4),
  L("Six words or fewer. Big enough to read without stopping."),
  L("If they read it while scrolling, you've already *won* the first round."),
 ], src("FB16"),
 cap("1.7 seconds: the average time people spent with a mobile post (vs 2.5 s on desktop).",
     ["That's Facebook's 2016 average, not a deadline, but it shows how little room you get.",
      "Under 2 seconds fits a headline, not a sentence.",
      "Six words or fewer, readable mid-scroll."],
     "Facebook research (2016), via Social Media Today")))

# s25 — testing: reach swings are normal
SC.append(S("s25", "testing", "Founders", "Reach dropped today? Instagram's boss says the algorithm is probably not why.", [
  H("Founders", "Reach dropped today? It's *probably not* the algorithm.", "Reach dropped today? Instagram's boss says it's *probably* not the algorithm."),
  L("Mosseri says ranking changes in small ways every single day.", kind="statement", font="serif", size=104, text="Ranking changes a little *every day.*", sub="Adam Mosseri, Apr 2025 (paraphrased)"),
  L("Big swings usually come from the *world*. Holidays. News. Events."),
  L("So one bad day tells you almost *nothing*.", kind="curve", title="Look at the week, not the day", xmax=7, ticks=[0, 1, 2, 3, 4, 5, 6, 7],
    curves=[{"pts": [[0, 40], [1, 62], [2, 30], [3, 55], [4, 48], [5, 70], [6, 52], [7, 64]], "color": "red"}], note="Illustration"),
  L("What tells you something? *Patterns* across many posts."),
  L("Mosseri's advice: *experiment*, and post as much as you can without burning out."),
  L("Judge the *week*. Not the day.", kind="statement", font="anton", size=170, text="Judge the *week.*"),
 ], src("SMTQA", "SMT26"),
 cap("Reach dropped today? Instagram's boss says it's probably not the algorithm.",
     ["Mosseri: ranking changes in small ways daily; big day-to-day swings are more likely the world changing (holidays, events).",
      "One bad day tells you almost nothing. Patterns across many posts do.",
      "Experiment. Post as much as you can without burning out. Judge the week."],
     "Adam Mosseri, via Social Media Today (Apr 2025; Sep 2026)")))

# s26 — retention: length limit and the payoff promise
SC.append(S("s26", "retention", "Small brands", "Reels can be 3 minutes now. That doesn't mean yours should be.", [
  H("Small brands", "Reels can be *3 minutes* now. Yours probably *shouldn't*.", "Reels can be *three* minutes long now. Yours probably shouldn't be."),
  L("Instagram raised the limit from *ninety* seconds to *three* minutes in January 2025.", kind="bars", title="Max reel length", unit="s", bars=[
    {"label": "Before Jan 2025", "value": 90, "text": "90s"}, {"label": "Since Jan 2025", "value": 180, "text": "3 min", "color": "red"}], maxv=220, note="Adam Mosseri, Jan 2025"),
  L("But watch time is one of its top *three* signals.", kind="icons", kinds=["clock", "heart", "send"],
    names={"clock": "watch time", "heart": "likes / reach", "send": "sends / reach"}, highlight="clock", hl_at=0.8),
  L("A longer reel only helps if people *stay*."),
  L("So the rule isn't short or long.", kind="statement", font="anton", size=150, text="Not short. Not long."),
  L("It's *one* lesson, and not a second more.", kind="statement", font="anton", size=150, text="*One* lesson. Then stop."),
  L("Check your retention chart. Where the line drops, you've said enough."),
 ], src("LEN", "SMT25", "RET"),
 cap("Reels can be 3 minutes now. Yours probably shouldn't be.",
     ["Instagram raised the max from 90 s to 3 min in Jan 2025.",
      "Watch time is one of the top 3 ranking signals, so length only helps if people stay.",
      "One lesson, then stop. Your Retention chart shows where you've said enough."],
     "Adam Mosseri (Jan 2025, via Storyboard18 & Social Media Today); Instagram reel insights")))

# s27 — product example: coffee roaster / café
SC.append(S("s27", "product", "Cafés", "Your café's best reel isn't the latte art. It's the 1 number behind it.", [
  H("Cafés", "Your best reel isn't the latte art. It's the *1* number behind it.", "Your café's best reel isn't the latte art. It's the *one* number behind it."),
  L("Latte art is pretty. And every café posts it.", kind="compare", weak="Latte art of the day", strong="", weak_label="EVERY CAFÉ", verdict_at=99),
  L("A number is *yours*. 'We pour X test shots every morning. Here's why.'", kind="compare", weak="Latte art of the day", strong="We pour *X* test shots every morning. Here's why", weak_label="EVERY CAFÉ", strong_label="ONLY YOU", verdict_at=1.2),
  L("Use your *real* number. Grams, minutes, shots. Whatever you actually do."),
  L("Then teach the why. Then show the cup.", kind="list", title="The format", items=["Your *real* number", "The *why*", "The cup, as *proof*"]),
  L("Instagram recommends the *original*. Your numbers can't be copied.", kind="statement", font="anton", size=140, text="Your numbers can't be *copied.*"),
 ], src("ORIG"),
 cap("Your café's best reel isn't the latte art. It's the 1 number behind it.",
     ["Every café posts latte art. Only you have your numbers: grams, minutes, test shots.",
      "Format: your real number → the why → the cup as proof.",
      "Instagram recommends the original, and your numbers can't be copied."],
     "Instagram Creators (originality update, Apr 2024)")))

# s28 — shares: predicted responses
SC.append(S("s28", "shares", "Product businesses", "Instagram predicts if someone will send your post before they see it.", [
  H("Product businesses", "Instagram predicts if someone will *send* your post.", "Instagram predicts whether each person will *send* your post to a friend."),
  L("Mosseri describes ranking as predicting how *each* person will respond.", kind="list", reveal="time", every=0.6, title="What it predicts", items=["Will they *watch*?", "Will they *like*?", "Will they *send* it?"]),
  L("Will they watch it? Like it? *Pass* it to a friend?"),
  L("Those predictions come from what people actually did with posts like yours.", kind="feed", speed=1000),
  L("So every send teaches Instagram who *else* might want it."),
  L("Which means the best growth tactic isn't a hashtag.", kind="statement", font="anton", size=150, text="Not a hashtag."),
  L("It's a post people *pass* *on*.", kind="statement", font="anton", size=150, text="A post people *pass on.*"),
 ], src("SMT26", "SMT25"),
 cap("Instagram predicts whether each person will send your post to a friend.",
     ["Mosseri: ranking predicts how each person will respond: watch, like, pass it on.",
      "Sends per reach is one of the signals he tells creators to track.",
      "The best growth tactic isn't a hashtag. It's a post people pass on."],
     "Adam Mosseri, via Social Media Today (Jan 2025; Sep 2026)")))

# s29 — reach: hashtags vs keywords
SC.append(S("s29", "reach", "Small brands", "You can only use 5 hashtags now. And they won't grow your reach.", [
  H("Small brands", "You get *5* hashtags now. They won't *grow* your reach.", "You can only use *five* hashtags now. And they won't grow your reach."),
  L("Since December 2025, Instagram limits posts and reels to *five*.", kind="counter", to=5, label="hashtags max · since Dec 2025", over=0.8, size=380),
  L("Mosseri: hashtags are no longer a primary way to increase reach.", kind="quote", size=72, quote="Hashtags are *no longer a primary way* to increase your reach on Instagram.", who="Adam Mosseri", role="Head of Instagram · Apr 2025"),
  L("They just tell people what a post is *about*."),
  L("So what helps people find you? *Keywords*.", kind="statement", font="anton", size=160, text="*Keywords.*"),
  L("Instagram's advice: put relevant keywords in your *caption*, not the comments,", kind="list", title="Be findable", items=["Keywords in the *caption*", "Bio matches your *content*", "Up to *5* targeted hashtags"]),
  L("and make your name and bio match what you post."),
 ], src("HASH", "SMTQA", "ELIG"),
 cap("You can only use 5 hashtags now. And they won't grow your reach.",
     ["Since Dec 2025 Instagram limits posts and reels to 5 hashtags; it recommends fewer, more targeted ones.",
      "Mosseri: hashtags are no longer a primary way to increase reach.",
      "Put keywords in your caption (not comments) and make your name and bio match your content."],
     "Instagram via Social Media Today (Dec 2025); Adam Mosseri (Apr 2025); Instagram Creators")))

# s30 — hooks: weak vs strong, same product (jewelry)
SC.append(S("s30", "hooks", "Jewelry brands", "Same necklace. 2 first frames. Only 1 stops the scroll.", [
  H("Jewelry brands", "Same necklace. *2* first frames. Only *1* stops the scroll.", "Same necklace. *Two* first frames. Only one stops the scroll."),
  L("First frame A: a slow pan across the necklace.", kind="compare", weak="(slow pan across the necklace)", strong="", weak_label="FRAME A", verdict_at=99),
  L("First frame B: '*Three* signs your gold is fake.'", kind="compare", weak="(slow pan across the necklace)", strong="*3* signs your 'gold' necklace is fake", weak_label="FRAME A", strong_label="FRAME B", verdict_at=1.4),
  L("B wins, because it gives a *reason* to stay."),
  L("It names a *fear*, it has a number, and the answer is coming."),
  L("Instagram measures who skips in the first *three* seconds. Frame A loses them there.", kind="timeline", max=10, mark=3, mark_label="SKIP ZONE", title="Where A loses them"),
  L("And the necklace? It shows up at sign three, as the real thing.", kind="statement", font="serif", size=110, text="The product: the *real thing,* at the end."),
 ], src("RET", "ELIG"),
 cap("Same necklace. 2 first frames. Only 1 stops the scroll.",
     ["A: a slow pan. B: '3 signs your gold necklace is fake.'",
      "B names a fear, has a number, and promises an answer. A loses people in the 3-second skip window Instagram measures.",
      "Your product shows up at the end, as the real thing."],
     "Instagram reel insights (Aug 2025); Instagram Creators")))

base = json.load(open("/home/claude/lessons/scen/s01_02.json"))["scenarios"]
allsc = base + SC
for s in allsc:
    s["status"] = "unused"
json.dump({"campaign": "lessons", "created": "2026-10-27",
           "voice": "Kokoro af_heart @0.92", "rotation_rule": "never the same lesson type twice in a row",
           "scenarios": allsc}, open("/home/claude/lessons/scen/scenarios.json", "w"), indent=1, ensure_ascii=False)
print(len(allsc), [s["type"] for s in allsc])
