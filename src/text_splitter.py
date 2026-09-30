def split_text(text, chunk_size=500, chunk_overlap=100):
    """
    Split text into overlapping chunks.

    chunk_size:
        Maximum approximate number of characters in each chunk.

    chunk_overlap:
        Number of characters repeated between consecutive chunks.
    """

    if not text:
        return []

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - chunk_overlap

    return chunks