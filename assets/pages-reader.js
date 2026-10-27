"use strict";
/* Interactive, source-free Reader for branch-based GitHub Pages.
 * This does NOT upload manuscripts or claim FantLab analyzer-input parity.
 * Data is a local, build-pinned JSON snapshot retained in the public repository.
 */
(() => {
  const snapshotUrl = "./assets/evidence-snapshot.json";
  const chartChoices = {
    "fantlab.dialogue.share_percent": {label:"Dialogue share",unit:"%",digits:2},
    "fantlab.general.mean_sentence_length_chars": {label:"Mean sentence length",unit:"characters / sentence",digits:2},
    "fantlab.punctuation.comma.per_1000_words": {label:"Commas",unit:"occurrences / 1,000 words",digits:2}
  };
  const labelNames = {
    "fantlab.general.characters":"Characters including spaces",
    "fantlab.general.words":"Word tokens",
    "fantlab.general.mean_word_length_chars":"Mean word length",
    "fantlab.general.mean_sentence_length_chars":"Mean sentence length",
    "fantlab.dialogue.share_percent":"Dialogue share",
    "fantlab.dialogue.mean_dialogue_sentence_length_chars":"Dialogue sentence length",
    "fantlab.dialogue.mean_narration_sentence_length_chars":"Narration sentence length",
    "fantlab.dialogue.author_text_inside_dialogue_percent":"Author text within dialogue",
    "fantlab.vocabulary.unique_words":"Unique word forms",
    "fantlab.vocabulary.active_dictionary":"Dictionary word forms",
    "fantlab.vocabulary.active_nondictionary":"Non-dictionary word forms",
    "scriptorium.general.sentences":"Sentence count (Scriptorium extension)"
  };
  const el = id => document.getElementById(id);
  const allCharts = [...document.querySelectorAll("[data-chart]")];
  const bookLinks = [...document.querySelectorAll("[data-book]")];
  const select = el("choose-book");
  const search = el("search-metric");
  const feedback = el("table-status");
  const tableBody = el("measurement-rows");
  const exportButton = el("export-button");
  const caption = el("table-caption");
  let doc;
  let currentBook = "anna";
  let currentChart = "fantlab.dialogue.share_percent";

  function numeric(value) {
    return typeof value === "number" && Number.isFinite(value);
  }
  function verify(data) {
    if (!data || data.schema !== "scriptorium-branch-pages-derived-v1" ||
        data.scientific_claim !== "DIAGNOSTIC_ONLY" ||
        data.fantlab_input_identity !== "UNKNOWN" ||
        data.counts?.m2_source_matched !== 0 ||
        data.counts?.metrics_total !== 113 ||
        data.counts?.numeric_total !== 94 ||
        data.counts?.unavailable_total !== 19 ||
        !Array.isArray(data.books) || data.books.length !== 4) {
      throw Error("Scientific or coverage contract mismatch");
    }
    const expected = {anna:[28,23],waves:[27,23],silver:[29,24],karamazov:[29,24]};
    const ids = new Set();
    for (const book of data.books) {
      const target = expected[book.key];
      if (!target || ids.has(book.key) || !Array.isArray(book.metrics) ||
          book.metrics.length !== target[0] || book.measured !== target[1] ||
          book.unavailable !== target[0]-target[1] ||
          typeof book.title !== "string" ||
          !/^https:\/\/github\.com\/drevendev\/Scriptorium\/blob\/master\//.test(book.evidence_url) ||
          !/^https:\/\/fantlab\.ru\/work\d+\/lp$/.test(book.fantlab_url) ||
          !/^[0-9a-f]{64}$/.test(book.source_sha256)) {
        throw Error("Book identity or measurement coverage mismatch");
      }
      ids.add(book.key);
      const fields = new Set();
      let measured = 0;
      for (const row of book.metrics) {
        if (typeof row.id !== "string" || fields.has(row.id) ||
            !/^(fantlab|scriptorium)\.[a-z0-9_.]+$/.test(row.id) ||
            !(row.actual === null || numeric(row.actual)) ||
            !(row.reference === null || numeric(row.reference)) ||
            !["measured","not_run","unavailable"].includes(row.status) ||
            (row.actual !== null) !== (row.status === "measured") ||
            !["candidate","extension"].includes(row.kind) ||
            (row.kind === "extension" && row.reference !== null)) {
          throw Error("Field observation or unknown-state mismatch");
        }
        fields.add(row.id);
        if (row.actual !== null) measured++;
      }
      if (measured !== target[1]) throw Error("Measured field count mismatch");
    }
    if (ids.size !== 4) throw Error("Duplicate or missing book");
  }
  function findBook() {
    return doc.books.find(book => book.key === currentBook);
  }
  function label(id) {
    if (labelNames[id]) return labelNames[id];
    return id.replace(/^fantlab\./,"").replaceAll("."," · ").replaceAll("_"," ");
  }
  function unit(id) {
    if (id === "scriptorium.general.sentences") return "sentences";
    if (id === "fantlab.general.characters") return "characters incl. spaces";
    if (id === "fantlab.general.words") return "word tokens";
    if (id === "fantlab.general.mean_word_length_chars") return "characters / word";
    if (id.includes("sentence_length")) return "characters / sentence";
    if (id.endsWith("_percent")) return "%";
    if (id.includes(".punctuation.")) return "occurrences / 1,000 words";
    if (id.includes("uasz_")) return "mean unique forms / token window";
    if (id.includes(".vocabulary.")) return "word forms";
    return "candidate metric units";
  }
  function exact(value) {
    if (value === null) return "UNKNOWN";
    return String(value);
  }
  function appendCell(row, tag, content) {
    const cell = document.createElement(tag);
    cell.textContent = content;
    if (tag === "th") cell.scope = "row";
    row.appendChild(cell);
    return cell;
  }
  function refreshTable() {
    const book = findBook();
    const query = search.value.toLocaleLowerCase("en").trim();
    const fragment = document.createDocumentFragment();
    const matches = book.metrics.filter(item => {
      return !query || (item.id+" "+label(item.id)+" "+unit(item.id)).toLowerCase().includes(query);
    });
    for (const item of matches) {
      const tr = document.createElement("tr");
      const th = appendCell(tr,"th",label(item.id));
      const code = document.createElement("code");
      code.textContent = item.id;
      th.appendChild(code);
      appendCell(tr,"td",item.actual === null ? item.status.toUpperCase() : exact(item.actual));
      appendCell(tr,"td",item.kind === "extension" ? "N/A (extension)" : exact(item.reference));
      appendCell(tr,"td",unit(item.id));
      appendCell(tr,"td",item.kind === "extension" ?
        "Scriptorium extension" : item.status === "measured" ?
        "Measured / source unmatched" : item.status.toUpperCase());
      fragment.appendChild(tr);
    }
    if (!matches.length) {
      const tr = document.createElement("tr");
      const td = document.createElement("td");
      td.colSpan = 5;
      td.textContent = "No metric matches your search. Clear the filter to show all fields.";
      tr.appendChild(td);
      fragment.appendChild(tr);
    }
    tableBody.replaceChildren(fragment);
    caption.textContent = book.title+" · "+book.metrics.length+
      " source-frozen diagnostic fields; no verified FantLab parity";
    feedback.textContent = matches.length+" of "+book.metrics.length+" fields shown · "+
      book.measured+" numeric, "+book.unavailable+" unavailable; M2 0/5";
    el("evidence-source").href = book.evidence_url;
    el("fantlab-reference").href = book.fantlab_url;
  }
  function refreshChart() {
    const choice = chartChoices[currentChart];
    const series = doc.books.map(book => {
      const row = book.metrics.find(item => item.id === currentChart);
      if (!row || !numeric(row.actual)) throw Error("Missing normalized chart measurement");
      return {title:book.title,actual:row.actual};
    });
    const maximum = Math.max(...series.map(item=>item.actual));
    const fragment = document.createDocumentFragment();
    for (const item of series) {
      const row = document.createElement("div");
      row.className = "chart-row";
      appendCell(row,"span",item.title);
      const track = document.createElement("div");
      track.className = "bar-track";
      track.setAttribute("aria-hidden","true");
      const fill = document.createElement("span");
      fill.style.width = (maximum > 0 ? 100*item.actual/maximum : 0).toFixed(2)+"%";
      track.appendChild(fill);
      row.appendChild(track);
      appendCell(row,"strong",item.actual.toFixed(choice.digits)+(choice.unit === "%" ? "%" : ""));
      fragment.appendChild(row);
    }
    el("chart-series").replaceChildren(fragment);
    el("chart-unit").textContent = choice.label+" · "+choice.unit+" · labels rounded to 2 decimals";
    for (const button of allCharts) button.setAttribute("aria-pressed",String(button.dataset.chart===currentChart));
  }
  function downloadSelected() {
    const book = findBook();
    const result = {
      schema:"scriptorium-branch-pages-selection-v1",
      scientific_claim:"DIAGNOSTIC_ONLY",
      fantlab_input_identity:"UNKNOWN",
      m2_source_matched:0,
      candidate_id:book.candidate_id,
      source_sha256:book.source_sha256,
      source_evidence_url:book.evidence_url,
      metrics:book.metrics
    };
    const blob = new Blob([JSON.stringify(result,null,2)+"\n"],{type:"application/json"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "scriptorium-"+book.key+"-diagnostic.json";
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  async function initialize() {
    try {
      const response = await fetch(snapshotUrl,{cache:"no-store",credentials:"omit"});
      if (!response.ok) throw Error("HTTP "+response.status);
      const data = await response.json();
      verify(data);
      doc = data;
      select.disabled = false;
      search.disabled = false;
      exportButton.disabled = false;
      for (const chartButton of allCharts) {
        chartButton.disabled = false;
        chartButton.addEventListener("click",()=>{
          currentChart = chartButton.dataset.chart;
          refreshChart();
        });
      }
      for (const anchor of bookLinks) {
        anchor.addEventListener("click",event=>{
          if (!doc.books.some(book=>book.key===anchor.dataset.book)) return;
          event.preventDefault();
          currentBook = anchor.dataset.book;
          select.value = currentBook;
          search.value = "";
          refreshTable();
          el("measurements").scrollIntoView({block:"start",behavior:"auto"});
        });
      }
      select.addEventListener("change",()=>{currentBook=select.value;search.value="";refreshTable();});
      search.addEventListener("input",refreshTable);
      exportButton.addEventListener("click",downloadSelected);
      refreshChart();
      refreshTable();
    } catch (_) {
      feedback.textContent =
        "Interactive metric data is unavailable. Use the four original JSON links in the library; no fabricated values were substituted.";
      /* The server-rendered first three observations remain a usable fallback. */
    }
  }
  initialize();
})();
