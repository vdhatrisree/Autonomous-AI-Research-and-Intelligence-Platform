def display_results(results):
    for i, item in enumerate(results, start=1):
        print(f"\n[{i}] {item['title']} ({item['source']})")
        print(item['summary'][:200] + "...")
        print(f"URL: {item['url']}")
        chunks = item.get('chunks', [])
        if chunks:
            print(f"PDF chunks extracted: {len(chunks)}")