export function selectNotes(notes, { query = "", field = "", review = "", sort = "score-desc" } = {}) {
  const words = query.trim().toLocaleLowerCase("ko").split(/\s+/).filter(Boolean);
  const filtered = notes.filter(note => {
    const searchable = [note.title, note.id, note.summary, note.novelty, ...note.fields].join(" ").toLocaleLowerCase("ko");
    return words.every(word => searchable.includes(word)) && (!field || note.fields.includes(field)) && (!review || note.review_status === review);
  });
  const byId = (a, b) => a.id.localeCompare(b.id, "en");
  return filtered.sort((a, b) => {
    if (sort.startsWith("score")) {
      if (a.score === null || b.score === null) {
        return a.score === b.score ? byId(a, b) : a.score === null ? 1 : -1;
      }
      return (sort === "score-asc" ? a.score - b.score : b.score - a.score) || byId(a, b);
    }
    if (sort === "title") return a.title.localeCompare(b.title, "ko") || byId(a, b);
    return (b.updated || b.created).localeCompare(a.updated || a.created) || byId(a, b);
  });
}

export function documentRoute(path, section = "") {
  return `#/doc/${encodeURI(path)}${section ? `?section=${encodeURIComponent(section)}` : ""}`;
}
