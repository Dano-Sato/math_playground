import { selectNotes, documentRoute } from "./model.mjs";

const main = document.querySelector("#main");
const escapeHTML = value => String(value ?? "").replace(/[&<>"']/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char]));
let data = null;
let activeDocument = null;
let routeVersion = 0;
let fetching = false;
let toastTimer;
let filters = { query: "", field: "", review: "", sort: "score-desc" };
try {
  const stored = JSON.parse(localStorage.getItem("math-wiki-sort"));
  if (["score-desc", "score-asc", "recent", "title"].includes(stored)) filters.sort = stored;
} catch { /* Storage is optional. */ }

function toast(message) {
  const element = document.querySelector("#toast");
  element.textContent = message;
  element.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { element.hidden = true; }, 2800);
}

async function api(path) {
  const response = await fetch(path, { cache: "no-store" });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || "문서를 불러오지 못했습니다.");
  return result;
}

function reviewBadge(note) {
  const kind = note.review_status === "통과" ? "" : note.review_status === "수정 필요" ? "needs-work" : "pending";
  const symbol = note.review_status === "통과" ? "✓" : "◷";
  return `<span class="review-badge ${kind}"><span aria-hidden="true">${symbol}</span>${note.review_status === "통과" ? "독립 검토 통과" : escapeHTML(note.review_status)}</span>`;
}

function warnings() {
  return data.warnings.length ? `<details class="warning"><summary>읽지 못한 파일 또는 평가 정보 ${data.warnings.length}건</summary><ul>${data.warnings.map(message => `<li>${escapeHTML(message)}</li>`).join("")}</ul></details>` : "";
}

function heading(eyebrow, title, description) {
  return `<div class="page-heading"><div><div class="eyebrow">${eyebrow}</div><h1>${title}</h1><p>${description}</p></div><div class="heading-mark" aria-hidden="true">ƒ</div></div>`;
}

function renderNotes() {
  activeDocument = null;
  document.title = "연구 노트 · 수학 연구실";
  const allFields = [...new Set(data.notes.flatMap(note => note.fields))].sort((a, b) => a.localeCompare(b, "ko"));
  if (filters.field && !allFields.includes(filters.field)) filters.field = "";
  const reviewed = data.notes.filter(note => note.review_status === "통과").length;
  main.innerHTML = `${heading("RESEARCH LIBRARY", "연구 노트", "질문에서 증명까지, 기록된 탐구를 살펴보세요.")}
    <section class="stats" aria-label="연구 현황">
      <div class="stat"><div class="stat-icon" aria-hidden="true">▤</div><div><div class="stat-label">전체 연구 노트</div><div class="stat-number">${data.notes.length}<small>편</small></div></div></div>
      <div class="stat"><div class="stat-icon" aria-hidden="true">✓</div><div><div class="stat-label">독립 검토 통과</div><div class="stat-number">${reviewed}<small>편</small></div></div></div>
      <div class="stat"><div class="stat-icon" aria-hidden="true">◇</div><div><div class="stat-label">탐구 중인 분야</div><div class="stat-number">${allFields.filter(field => field !== "미분류").length}<small>개</small></div></div></div>
    </section>${warnings()}
    <section class="library" aria-labelledby="list-title">
      <div class="library-title"><h2 id="list-title">모든 연구 노트<span class="count-label" id="result-count"></span></h2><a class="helper-link" href="${documentRoute("wiki/Scoring.md")}">점수 기준 보기 ↗</a></div>
      <div class="filters"><div class="search-wrap"><input id="search" type="search" aria-label="연구 노트 검색" placeholder="제목, 분야, 요약으로 검색" value="${escapeHTML(filters.query)}" autocomplete="off"></div>
        <select id="field-filter" aria-label="분야 필터"><option value="">모든 분야</option>${allFields.map(field => `<option value="${escapeHTML(field)}" ${filters.field === field ? "selected" : ""}>${escapeHTML(field)}</option>`).join("")}</select>
        <select id="review-filter" aria-label="검토 상태 필터"><option value="">모든 검토 상태</option>${["통과", "대기", "수정 필요"].map(review => `<option value="${review}" ${filters.review === review ? "selected" : ""}>${review === "통과" ? "검토 통과" : review}</option>`).join("")}</select>
        <select id="sort" aria-label="연구 노트 정렬">${[["score-desc", "점수 높은순"], ["score-asc", "점수 낮은순"], ["recent", "최근 수정순"], ["title", "제목순"]].map(([value, label]) => `<option value="${value}" ${filters.sort === value ? "selected" : ""}>${label}</option>`).join("")}</select>
      </div>
      <div class="list-labels" aria-hidden="true"><span>성과 점수</span><span>연구 제목 · 분야</span><span class="review-label">검토 상태</span><span class="date-label">수정일</span></div>
      <div id="note-list"></div>
      <div class="library-foot">파일 변경을 15초마다 확인합니다. 점수 미평가 노트는 점수 정렬의 마지막에 표시됩니다.</div>
    </section>
    <div class="score-note"><span aria-hidden="true">ⓘ</span><span>성과 점수는 새로운 수학적 기여에 대한 내부 평가입니다. 100점은 밀레니엄급, 80점은 필즈급의 기준점이며, 신규성 확인과 증명 검토는 별도로 기록합니다. <a href="${documentRoute("wiki/Scoring.md")}">평가 기준</a></span></div>`;
  renderNoteRows();
  document.querySelector("#search").addEventListener("input", event => { filters.query = event.target.value; renderNoteRows(); });
  for (const [id, key] of [["field-filter", "field"], ["review-filter", "review"], ["sort", "sort"]]) {
    document.getElementById(id).addEventListener("change", event => {
      filters[key] = event.target.value;
      if (key === "sort") { try { localStorage.setItem("math-wiki-sort", JSON.stringify(filters.sort)); } catch { /* optional */ } }
      renderNoteRows();
    });
  }
}

function renderNoteRows() {
  const notes = selectNotes(data.notes, filters);
  document.querySelector("#result-count").textContent = `${notes.length} / ${data.notes.length}`;
  document.querySelector("#note-list").innerHTML = notes.length ? notes.map(note => `<article class="note-row">
    <div class="score-badge ${note.score === null ? "unscored" : ""}" aria-label="${note.score === null ? "점수 미평가" : `성과 점수 ${note.score}점, 100점 만점`}"><strong>${note.score === null ? "—" : String(note.score).padStart(2, "0")}</strong><small>${note.score === null ? "미평가" : "/ 100"}</small></div>
    <div><a class="note-title" href="${documentRoute(note.path)}">${escapeHTML(note.title)}</a><p class="note-description">${escapeHTML(note.summary || note.novelty)}</p><div class="tags">${note.fields.map(field => `<span class="tag">${escapeHTML(field)}</span>`).join("")}</div></div>
    <div class="review-cell">${reviewBadge(note)}<small>${escapeHTML(note.evaluation.evaluation_status || "평가 대기")}</small></div>
    <time class="date-cell" datetime="${escapeHTML(note.updated || note.created)}">${escapeHTML(note.updated || note.created || "—")}</time>
    </article>`).join("") : `<div class="empty"><strong>${data.notes.length ? "일치하는 연구 노트가 없습니다" : "첫 연구 노트를 기다리고 있습니다"}</strong>${data.notes.length ? "검색어나 필터를 바꾸어 보세요." : "research 폴더에 note.md를 저장하면 여기에 나타납니다."}${data.notes.length ? '<br><button id="reset-filters">필터 초기화</button>' : ""}</div>`;
  document.querySelector("#reset-filters")?.addEventListener("click", () => { filters = { ...filters, query: "", field: "", review: "" }; renderNotes(); });
}

function renderPages() {
  activeDocument = null;
  document.title = "모든 문서 · 수학 연구실";
  const sections = [["wiki", "위키"], ["research", "연구 · 검토 · 계산 기록"], ["templates", "작성 양식"], ["viewer", "뷰어와 라이선스"], ["안내", "운영 안내"]];
  main.innerHTML = `${heading("WIKI DIRECTORY", "모든 문서", "연구 노트부터 검토 기록까지, 서로 이어진 문서들입니다.")}${warnings()}` + sections.map(([section, label]) => {
    const pages = data.pages.filter(page => page.section === section);
    return pages.length ? `<section class="page-group"><h2>${label} <span class="count-label">${pages.length}</span></h2><div class="page-list">${pages.map(page => `<a class="page-item" href="${documentRoute(page.path)}"><strong>${escapeHTML(page.title)} ↗</strong><small>${escapeHTML(page.path)}</small></a>`).join("")}</div></section>` : "";
  }).join("");
}

function configureMarkdown() {
  if (!window.marked || !window.DOMPurify || !window.katex) throw new Error("렌더링 파일을 불러오지 못했습니다. 서버를 다시 실행해 보세요.");
  marked.use({ extensions: [
    { name: "mathBlock", level: "block", start: src => src.indexOf("$$"), tokenizer(src) {
      const match = /^\$\$\s*\n?([\s\S]*?)\$\$(?:[^\S\n]*\n|$)/.exec(src);
      return match ? { type: "mathBlock", raw: match[0], text: match[1].trim() } : undefined;
    }, renderer: token => `<div class="math-slot math-block" data-display="true">${escapeHTML(token.text)}</div>\n` },
    { name: "mathInline", level: "inline", start: src => src.indexOf("$"), tokenizer(src) {
      const match = /^\$(?!\$)((?:\\.|[^$\n\\])+?)\$(?!\$)/.exec(src);
      return match ? { type: "mathInline", raw: match[0], text: match[1] } : undefined;
    }, renderer: token => `<span class="math-slot" data-display="false">${escapeHTML(token.text)}</span>` },
  ] });
}

function rewriteContent(article, documentPath) {
  const headingIds = new Map();
  for (const header of article.querySelectorAll("h1,h2,h3,h4,h5,h6")) {
    const base = header.textContent.toLowerCase().trim().replace(/[^\p{L}\p{N}\s_-]/gu, "").replace(/\s/g, "-") || "section";
    const number = headingIds.get(base) || 0;
    headingIds.set(base, number + 1);
    header.id = number ? `${base}-${number}` : base;
  }
  for (const anchor of article.querySelectorAll("a[href]")) {
    const raw = anchor.getAttribute("href");
    const url = new URL(raw, `${location.origin}/${documentPath}`);
    if (url.origin === location.origin) {
      const path = decodeURIComponent(url.pathname.slice(1));
      if (path.endsWith(".md")) anchor.href = documentRoute(path, decodeURIComponent(url.hash.slice(1)));
      else if (raw.startsWith("#/")) anchor.href = raw;
      else anchor.href = `/api/file?path=${encodeURIComponent(path)}`;
    } else {
      anchor.target = "_blank";
      anchor.rel = "noopener noreferrer";
    }
  }
  for (const img of article.querySelectorAll("img")) {
    const url = new URL(img.getAttribute("src") || "", `${location.origin}/${documentPath}`);
    if (url.origin === location.origin) img.src = `/api/file?path=${encodeURIComponent(decodeURIComponent(url.pathname.slice(1)))}`;
    else { img.removeAttribute("src"); img.alt = `${img.alt || "외부 이미지"} (외부 이미지는 로컬 뷰어에서 불러오지 않습니다)`; }
    img.loading = "lazy";
  }
  for (const slot of article.querySelectorAll(".math-slot")) {
    try {
      katex.render(slot.textContent, slot, { displayMode: slot.dataset.display === "true", throwOnError: false, trust: false, strict: "ignore", maxExpand: 1000 });
    } catch { slot.classList.add("math-error"); }
  }
  for (const table of article.querySelectorAll("table")) {
    const wrapper = document.createElement("div");
    wrapper.className = "table-scroll";
    table.replaceWith(wrapper);
    wrapper.append(table);
  }
}

function evaluationPanel(note) {
  const evaluation = note.evaluation;
  const items = Array.isArray(evaluation.rationale) ? evaluation.rationale : [];
  return `<details class="evaluation"><summary>성과 평가 근거 · ${note.score === null ? "미평가" : `${note.score} / 100`} ${escapeHTML(evaluation.evaluation_status || "")}</summary><p>${escapeHTML(note.novelty)}</p>${items.length ? `<ul>${items.map(item => `<li>${escapeHTML(item)}</li>`).join("")}</ul>` : "<p>아직 평가 근거가 등록되지 않았습니다.</p>"}${evaluation.reassessment ? `<p>재평가 조건: ${escapeHTML(evaluation.reassessment)}</p>` : ""}<p class="eval-footer">${escapeHTML(evaluation.assessed_at || "평가일 미정")} · ${escapeHTML(evaluation.assessor || "평가자 미정")} · 기준 ${escapeHTML(evaluation.scoring_version || "미정")} · <a href="/api/file?path=${encodeURIComponent(note.path.replace(/note\.md$/, "meta.json"))}" target="_blank" rel="noopener">평가 원본 JSON ↗</a></p></details>`;
}

async function renderDocument(path, section, version, preservePosition = false) {
  const preserveScroll = activeDocument === path;
  const oldScroll = window.scrollY;
  if (!preserveScroll) main.innerHTML = '<div class="loading">문서를 불러오는 중…</div>';
  const document = await api(`/api/document?path=${encodeURIComponent(path)}`);
  if (version !== routeVersion) return;
  const note = data.notes.find(item => item.path === document.path);
  const title = data.pages.find(item => item.path === document.path)?.title || document.path;
  window.document.title = `${title} · 수학 연구실`;
  window.document.querySelector("#breadcrumb").textContent = note ? "연구 노트" : "위키 문서";
  main.innerHTML = `<div class="document-toolbar"><a class="back-link" href="${note ? "#/notes" : "#/pages"}">← ${note ? "연구 노트 목록" : "모든 문서"}</a><a class="source-link" href="/api/file?path=${encodeURIComponent(document.path)}" target="_blank" rel="noopener">Markdown 원문 ↗</a></div>
    <div class="document-layout"><div class="document-main">${note ? `<div class="document-meta"><span class="score-inline">성과 <strong>${note.score === null ? "미평가" : note.score}</strong>${note.score === null ? "" : " / 100"}</span>${reviewBadge(note)}${note.fields.map(field => `<span class="tag">${escapeHTML(field)}</span>`).join("")}<span class="meta-date">${escapeHTML(note.updated || note.created)}</span></div>` : ""}<article class="article" id="article"></article>${note ? evaluationPanel(note) : ""}</div><aside class="toc" aria-label="이 문서의 목차"><h2>ON THIS PAGE</h2><div id="toc-links"></div></aside></div>`;
  const article = window.document.querySelector("#article");
  article.innerHTML = DOMPurify.sanitize(marked.parse(document.content, { gfm: true }), { USE_PROFILES: { html: true } });
  rewriteContent(article, document.path);
  window.document.querySelector("#toc-links").innerHTML = [...article.querySelectorAll("h2,h3")].map(header => `<a class="level-${header.tagName.slice(1)}" href="${documentRoute(document.path, header.id)}">${escapeHTML(header.textContent)}</a>`).join("");
  activeDocument = document.path;
  if (preservePosition && preserveScroll) window.scrollTo(0, oldScroll);
  else if (section) window.document.getElementById(section)?.scrollIntoView({ block: "start" });
  else if (preserveScroll) window.scrollTo(0, oldScroll);
  else window.scrollTo(0, 0);
}

async function route({ preservePosition = false } = {}) {
  if (!data) return;
  const version = ++routeVersion;
  const raw = location.hash.slice(1) || "/notes";
  const [path, search = ""] = raw.split("?");
  document.querySelectorAll("[data-nav]").forEach(item => {
    const match = item.dataset.nav === (path.startsWith("/doc/") ? decodeURI(path.slice(5)) : path.slice(1));
    item.classList.toggle("active", match);
    if (match) item.setAttribute("aria-current", "page"); else item.removeAttribute("aria-current");
  });
  document.querySelector("#sidebar").classList.remove("open");
  document.querySelector("#menu-toggle").setAttribute("aria-expanded", "false");
  document.querySelector("#breadcrumb").textContent = path === "/pages" ? "모든 문서" : "연구 노트";
  try {
    if (path === "/notes" || path === "/") { renderNotes(); window.scrollTo(0, 0); }
    else if (path === "/pages") { renderPages(); window.scrollTo(0, 0); }
    else if (path.startsWith("/doc/")) await renderDocument(decodeURI(path.slice(5)), new URLSearchParams(search).get("section"), version, preservePosition);
    else throw new Error("페이지를 찾을 수 없습니다.");
  } catch (error) {
    if (version !== routeVersion) return;
    activeDocument = null;
    main.innerHTML = `<div class="error-panel"><h1>문서를 열지 못했습니다</h1><p>${escapeHTML(error.message)}</p><a href="#/notes">연구 노트 목록으로 돌아가기 →</a></div>`;
  }
}

async function refresh(manual = false) {
  if (fetching) return;
  fetching = true;
  document.querySelector("#refresh").disabled = true;
  try {
    const next = await api("/api/catalog");
    const changed = !data || data.revision !== next.revision;
    data = next;
    document.querySelector("#nav-count").textContent = data.notes.length;
    document.querySelector("#sync-status").textContent = `${new Intl.DateTimeFormat("ko", { hour: "2-digit", minute: "2-digit" }).format(new Date())} 파일 확인`;
    if (changed || manual) {
      // Keep input focus when background updates only affect the library rows.
      if (!manual && document.querySelector("#note-list") && !activeDocument) {
        const focus = document.activeElement;
        const focusedId = focus?.id;
        const selection = focusedId === "search" ? [focus.selectionStart, focus.selectionEnd] : null;
        const scroll = window.scrollY;
        renderNotes();
        const replacement = focusedId ? document.getElementById(focusedId) : null;
        replacement?.focus({ preventScroll: true });
        if (selection) replacement?.setSelectionRange(...selection);
        window.scrollTo(0, scroll);
      } else await route({ preservePosition: true });
    }
    if (manual) toast("최신 파일을 불러왔습니다.");
  } catch (error) {
    document.querySelector("#sync-status").textContent = "연결 끊김 · 서버 확인 필요";
    if (!data) main.innerHTML = `<div class="error-panel"><h1>위키를 불러오지 못했습니다</h1><p>${escapeHTML(error.message)}</p><p>open_wiki.cmd를 실행한 뒤 새로고침하세요.</p></div>`;
    else if (manual) toast("서버 연결을 확인해 주세요.");
  } finally { fetching = false; document.querySelector("#refresh").disabled = false; }
}

document.querySelector("#refresh").addEventListener("click", () => refresh(true));
document.querySelector(".skip-link").addEventListener("click", event => { event.preventDefault(); main.focus(); main.scrollIntoView({ block: "start" }); });
document.querySelector("#menu-toggle").addEventListener("click", () => {
  const open = document.querySelector("#sidebar").classList.toggle("open");
  document.querySelector("#menu-toggle").setAttribute("aria-expanded", String(open));
});
document.addEventListener("keydown", event => {
  if (event.key === "Escape") { document.querySelector("#sidebar").classList.remove("open"); document.querySelector("#menu-toggle").setAttribute("aria-expanded", "false"); }
});
window.addEventListener("hashchange", route);
try {
  configureMarkdown();
  await refresh();
  setInterval(() => { if (!document.hidden) refresh(); }, 15000);
} catch (error) {
  main.innerHTML = `<div class="error-panel"><h1>뷰어를 시작하지 못했습니다</h1><p>${escapeHTML(error.message)}</p></div>`;
}
