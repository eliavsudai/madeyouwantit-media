"""Reel scoreboard for the lesson campaign.

Usage: IG_TOKEN=... python3 publisher/insights.py [--save] [--all]
Reads scenarios.json (scenario -> post_id once scheduled) + published.json, pulls lifetime
insights for each published lesson Reel, prints a table and (with --save) writes scoreboard.csv.
--all also includes every published Reel on the account (older campaign) for context.
Never prints the token.
"""
import csv, json, os, sys, urllib.parse, urllib.request, datetime as dt

API = "https://graph.instagram.com/v23.0"
TOKEN = os.environ.get("IG_TOKEN", "")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "views,reach,likes,comments,shares,saved,total_interactions,ig_reels_avg_watch_time"
EXTRA = ["profile_visits", "follows"]


def get(path, **p):
    p["access_token"] = TOKEN
    try:
        with urllib.request.urlopen(f"{API}/{path}?{urllib.parse.urlencode(p)}", timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode(errors="replace").replace(TOKEN, "***")}


def metrics(mid):
    vals = {}
    r = get(f"{mid}/insights", metric=BASE)
    for d in r.get("data", []):
        vals[d["name"]] = d["values"][0]["value"]
    for m in EXTRA:                       # not available for every media type; ignore errors
        r = get(f"{mid}/insights", metric=m)
        for d in r.get("data", []):
            vals[d["name"]] = d["values"][0]["value"]
    return vals


def main():
    pub = json.load(open(os.path.join(ROOT, "published.json")))
    sc_path = os.path.join(ROOT, "scenarios.json")
    scs = json.load(open(sc_path))["scenarios"] if os.path.exists(sc_path) else []
    rows = []
    targets = [(s.get("post_id"), s) for s in scs if s.get("post_id") in pub]
    if "--all" in sys.argv:
        used = {t[0] for t in targets}
        targets += [(k, {"id": k, "type": "older", "hook": ""}) for k in pub if "reel" in pub[k]["permalink"] and k not in used]
    for pid, s in targets:
        v = metrics(pub[pid]["media_id"])
        reach = v.get("reach", 0) or 0
        length = s.get("length_s") or 0
        avg = (v.get("ig_reels_avg_watch_time", 0) or 0) / 1000
        rows.append(dict(post_id=pid, scenario=s.get("id"), type=s.get("type"), hook=s.get("hook", "")[:60],
                         published=pub[pid]["published_at"][:16], length_s=length, views=v.get("views", 0), reach=reach,
                         avg_watch_s=round(avg, 1), watch_pct=round(100 * avg / length, 1) if length else "",
                         saves=v.get("saved", 0), shares=v.get("shares", 0), likes=v.get("likes", 0), comments=v.get("comments", 0),
                         profile_visits=v.get("profile_visits", ""), follows=v.get("follows", ""),
                         saves_shares_per100=round(100 * ((v.get("saved", 0) or 0) + (v.get("shares", 0) or 0)) / reach, 1) if reach else 0,
                         permalink=pub[pid]["permalink"]))
    me = get("me", fields="followers_count")
    print(f"followers {me.get('followers_count')} | {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC")
    for r in rows:
        print(f"{r['post_id']:<28} reach {r['reach']:>6} views {r['views']:>6} avg {r['avg_watch_s']}s/{r['length_s']}s "
              f"saves {r['saves']} shares {r['shares']} visits {r['profile_visits']} follows {r['follows']}")
    if "--save" in sys.argv and rows:
        with open(os.path.join(ROOT, "scoreboard.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main()
