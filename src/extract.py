#This pulls out only the title, summary text and URL we actually care about.
def extract_info(raw_summary):
    if raw_summary is None:
        return None
    return {
        "title": raw_summary.get("title", ""),
        "summary": raw_summary.get("extract", ""),
        "url": raw_summary.get("content_urls", {}).get("desktop", {}).get("page", ""),
    }