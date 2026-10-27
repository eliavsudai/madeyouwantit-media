"""Pull Reel insights for the 15-day format test and print/save a scoreboard.

Usage: IG_TOKEN=... python3 publisher/insights.py [--save]
Reads test15.json (which post id = which format) + published.json (media ids),
fetches lifetime insights per Reel and writes test15_scoreboard.csv with --save.
Never prints the token.
"""
import csv, json, os, sys, urllib.parse, urllib.request, datetime as dt

API = "https://graph.instagram.com/v23.0"
TOKEN = os.environ.get("IG_TOKEN", "")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METRICS = "views,reach,likes,comments,shares,saved,total_interactions,ig_reels_avg_watch_time,ig_reels_video_view_total_time"


def get(path, **p):
    p["access_token"] = TOKEN
    url = f"{API}/{path}?{urllib.parse.urlencode(p)}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode(errors="replace").replace(TOKEN, "***")}


def main():
    test = json.load(open(os.path.join(ROOT, "test15.json")))
    pub = json.load(open(os.path.join(ROOT, "published.json")))
    me = get("me", fields="followers_count,media_count")
    rows = []
    for post in test["posts"]:
        pid = post["id"]
        if pid not in pub:
            continue
        mid = pub[pid]["media_id"]
        ins = get(f"{mid}/insights", metric=METRICS)
        vals = {d["name"]: d["values"][0]["value"] for d in ins.get("data", [])}
        if "error" in ins:
            print("insights error", pid, ins["error"][:200], file=sys.stderr)
        length = post.get("length_s") or 0
        avg = (vals.get("ig_reels_avg_watch_time", 0) or 0) / 1000.0
        reach = vals.get("reach", 0) or 0
        row = dict(day=post["day"], format=post["format"], id=pid, permalink=pub[pid]["permalink"],
                   published=pub[pid]["published_at"][:16], length_s=length,
                   views=vals.get("views", 0), reach=reach,
                   avg_watch_s=round(avg, 1), watch_pct=round(100 * avg / length, 1) if length else "",
                   likes=vals.get("likes", 0), comments=vals.get("comments", 0),
                   shares=vals.get("shares", 0), saves=vals.get("saved", 0),
                   share_save_per100=round(100 * ((vals.get("shares", 0) or 0) + (vals.get("saved", 0) or 0)) / reach, 1) if reach else 0,
                   dms_daily=post.get("dms_daily", ""))
        rows.append(row)
    print(f"followers {me.get('followers_count')} | {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC")
    for r in rows:
        print(f"D{r['day']:>2} {r['format'][:22]:<22} views {r['views']:>5} reach {r['reach']:>5} "
              f"avg {r['avg_watch_s']:>4}s/{r['length_s']}s ({r['watch_pct']}%) sh+sv/100 {r['share_save_per100']} "
              f"likes {r['likes']} com {r['comments']}")
    if "--save" in sys.argv and rows:
        with open(os.path.join(ROOT, "test15_scoreboard.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main()
