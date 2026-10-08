# הוספת הרצאה חדשה

1. מוסיפים אובייקט ל-`lectures.json` עם השדות: id (מזהה יוטיוב), title, speaker, org, published_est (YYYY-MM-DD), age_when_added, duration_sec, url, transcript ("available" או "missing"), added, summary_he {tldr, points[], audience, tags[]}.
2. הסיכום נכתב מהתמלול של ההרצאה עצמה. אם אין תמלול, transcript="missing" והכרטיס יציג זאת.
3. מריצים `python3 build.py`. נוצר `index.html` מחדש.
4. מעלים את `lectures.json` ואת `index.html` ל-main (GitHub Pages מתעדכן תוך דקה-שתיים).
