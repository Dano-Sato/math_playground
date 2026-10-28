import test from "node:test";
import assert from "node:assert/strict";
import { selectNotes, documentRoute } from "../viewer/model.mjs";

const note = (id, score, extra = {}) => ({ id, score, title: id, fields: ["조합론"], summary: "차분 항등식", novelty: "미확인", review_status: "대기", updated: "2026-10-29", ...extra });
const notes = [note("unknown", null), note("two", 2), note("b-five", 5), note("a-five", 5), note("ten", 10), note("zero", 0)];

test("numeric scores descend; ties use stable IDs; zero differs from unscored", () => {
  assert.deepEqual(selectNotes(notes).map(n => n.id), ["ten", "a-five", "b-five", "two", "zero", "unknown"]);
  assert.equal(notes[0].id, "unknown", "must not mutate catalog order");
});
test("ascending scores still leave unscored last", () => {
  assert.deepEqual(selectNotes(notes, { sort: "score-asc" }).map(n => n.id), ["zero", "two", "a-five", "b-five", "ten", "unknown"]);
});
test("query, field, and review filters combine", () => {
  const samples = [note("first", 5), note("second", 7, { review_status: "통과", fields: ["해석학"], summary: "실수 지수" })];
  assert.deepEqual(selectNotes(samples, { query: "실수 지수", field: "해석학", review: "통과" }).map(n => n.id), ["second"]);
  assert.equal(selectNotes(samples, { query: "없는말" }).length, 0);
});
test("date ordering and Korean document paths", () => {
  assert.equal(selectNotes([note("old", 99, { updated: "2026-10-01" }), note("new", 1)], { sort: "recent" })[0].id, "new");
  assert.equal(documentRoute("wiki/한글 문서.md", "주장 1"), "#/doc/wiki/%ED%95%9C%EA%B8%80%20%EB%AC%B8%EC%84%9C.md?section=%EC%A3%BC%EC%9E%A5%201");
});
