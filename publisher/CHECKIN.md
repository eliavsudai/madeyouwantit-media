# Made You Want It check-in routine (for Claude's scheduled check-ins)

1. Publish check: `cd /home/claude/madeyouwantit-media && git pull -q && cat published.json`.
   Any approved post in schedule.json whose `when` has passed but isn't in published.json:
   publish it with `IG_TOKEN=$(cat /home/claude/secure/mywi_ig_token) python3 publisher/publish.py`,
   then commit + push published.json. Log each permalink in
   ~/Movies/Made You Want It/_system/state/log.md on the owner's Mac.
   If graph.instagram.com is blocked, trigger GitHub instead:
   `gh api -X POST repos/eliavsudai/madeyouwantit-media/actions/workflows/publish.yml/dispatches -f ref=main -f 'inputs[dry_run]=false'`.
2. Comments: `python3 publisher/comments.py list`, then answer each in the studio's voice:
   clever, confident, warm, specific to what the person actually said; witty when it fits, straightforward
   for genuine questions; same language as the commenter; never salesy or canned. Never fabricate anything.
   Spam/bots/self-promo: `comments.py skip ID` (never delete). Never send DMs (draft them for the owner).
   Flag to the owner: business enquiries, pricing, complaints, anything legal/medical/financial/abusive.
3. One hour after a post publishes, delete its local media from the owner's Mac
   (~/Movies/Made You Want It/days/... masters and upload versions, leftover ~/Downloads copies);
   keep captions/plan text and _system. Mark deletions in the log.
4. Tell the owner only if something needs him (a failed post, a question you can't answer).
