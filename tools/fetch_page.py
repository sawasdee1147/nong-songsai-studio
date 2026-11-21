#!/usr/bin/env python3
"""อ่านหน้าเว็บผ่าน proxy ของเซสชัน แล้วแปลงเป็นข้อความล้วน (ใช้แทน WebFetch ซึ่งไม่วิ่งผ่านเครือข่ายของเซสชัน)

ใช้: python3 tools/fetch_page.py <url> [--max 20000] [--grep คำ]
- ตามลิงก์ redirect อัตโนมัติ (เช่น doi.org -> สำนักพิมพ์)
- พิมพ์ URL ปลายทาง, HTTP status, ชื่อเรื่อง แล้วตามด้วยเนื้อหา
- --grep: พิมพ์เฉพาะย่อหน้าที่มีคำนั้น (ไม่สนตัวพิมพ์เล็กใหญ่) เพื่อหาข้อความที่ต้องการอ้าง
"""
import argparse, html, os, re, ssl, sys, urllib.request, urllib.error

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def ctx():
    c = ssl.create_default_context()
    for ca in (os.environ.get("SSL_CERT_FILE"), "/root/.ccr/ca-bundle.crt"):
        if ca and os.path.exists(ca):
            c.load_verify_locations(ca)
            break
    return c


class HttpsRedirect(urllib.request.HTTPRedirectHandler):
    """proxy ของเซสชันรองรับเฉพาะ HTTPS — อัปเกรด redirect ที่เป็น http:// ให้เป็น https://"""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if newurl.startswith("http://"):
            newurl = "https://" + newurl[len("http://"):]
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def to_text(raw):
    raw = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer|header)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr|section|article)>", "\n", raw)
    txt = html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))
    lines = [re.sub(r"[ \t ]+", " ", l).strip() for l in txt.splitlines()]
    return "\n".join(l for l in lines if len(l) > 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--max", type=int, default=20000)
    ap.add_argument("--grep")
    a = ap.parse_args()
    url = "https://" + a.url[len("http://"):] if a.url.startswith("http://") else a.url
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx()), HttpsRedirect())
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*",
                                                 "Accept-Language": "en,th;q=0.8"})
    try:
        r = opener.open(req, timeout=40)
        status, final, body = r.status, r.geturl(), r.read()
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} {a.url}\n(เว็บปฏิเสธ — ลองแหล่งสำรอง เช่น PubMed/PMC หรือ doi.org)")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"เชื่อมต่อไม่ได้: {e.reason} — โดเมนนี้อาจยังไม่อยู่ใน Allowed domains ของ environment")
        sys.exit(1)
    raw = body.decode(r.headers.get_content_charset() or "utf-8", "replace")
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
    text = to_text(raw)
    print(f"URL: {final}\nHTTP: {status}\nTITLE: {html.unescape(m.group(1)).strip() if m else ''}\n---")
    if a.grep:
        k = a.grep.lower()
        hits = [l for l in text.splitlines() if k in l.lower()]
        print("\n".join(hits) if hits else f"(ไม่พบ '{a.grep}')")
    else:
        print(text[: a.max])


if __name__ == "__main__":
    main()
