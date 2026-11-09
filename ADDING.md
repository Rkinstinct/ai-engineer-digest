# הוספת הרצאה חדשה

1. מוסיפים אובייקט ל-`lectures.json` עם השדות: id (מזהה יוטיוב), title, speaker, org, published_est (YYYY-MM-DD), age_when_added, duration_sec, url, transcript ("available" או "missing"), added, summary_he {tldr, points[], audience, tags[]}.
2. הסיכום נכתב מהתמלול של ההרצאה עצמה. אם אין תמלול, transcript="missing" והכרטיס יציג זאת.
3. מריצים `python3 build.py`. נוצר `index.html` מחדש.
4. מעלים את `lectures.json` ואת `index.html` ל-main (GitHub Pages מתעדכן תוך דקה-שתיים).


## Supplemental data (9 November 2026)

Large legacy files are preserved. New transcript-based entries may live in
`lectures-YYYY-MM-extra.json` using exactly the existing card schema.
The full source dataset is `lectures.json` plus all `lectures-*.json` arrays,
deduplicated by YouTube `id`. Do not infer the published total from the legacy
file alone. `build.py` merges these files automatically.

`updates.js` loads the supplemental files named in its `files` array, adds
only IDs absent from the page, and updates the date links and visible count.
The existing page includes this deferred script. When adding a new shard,
add its filename to that array. Keep each shard comfortably below 200 KB
so the regular web editor can replace it without large-file input problems.

After publishing, verify the exact committed supplemental JSON and script,
then verify the rendered live card count, source links, date groups and old
card preservation. A source commit alone is not a completed update.
The six cards recovered on 9 November were prepared on 3-4 November; their
source dates remain explicitly approximate. Their `added` date is the actual
9 November publication date.
