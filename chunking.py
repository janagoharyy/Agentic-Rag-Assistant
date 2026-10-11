def create_chunks(text, chunk_size=800, overlap=150):

    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        # If adding this paragraph keeps the chunk small enough
        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += paragraph + "\n\n"

        else:
            # Save the current chunk
            if current_chunk:
                chunks.append(current_chunk.strip())

            # Start a new chunk
            current_chunk = paragraph + "\n\n"

    # Save the final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks