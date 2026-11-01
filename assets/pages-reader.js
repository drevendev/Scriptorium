"use strict";
/* Russian-first, source-free Scriptorium Reader. Unknown is never zero.
 * English and French are different future analyzers, not silent RU aliases.
 */
(() => {
  const file = "./assets/evidence-snapshot.json";
  const metrics = {
    "fantlab.dialogue.share_percent": ["Доля диалогов","%",2],
    "fantlab.general.mean_sentence_length_chars": ["Длина предложения","символов / предложение",2],
    "fantlab.punctuation.comma.per_1000_words": ["Запятые","на 1000 слов",2],
    "fantlab.punctuation.dash.per_1000_words": ["Тире","на 1000 слов",2],
    "fantlab.general.mean_word_length_chars": ["Длина слова","символов / слово",2],
    "fantlab.dialogue.author_text_inside_dialogue_percent": ["Авторские ремарки внутри диалогов","%",2],
    "fantlab.dialogue.mean_dialogue_sentence_length_chars": ["Длина реплики","символов / предложение",2],
    "fantlab.dialogue.mean_narration_sentence_length_chars": ["Длина авторского предложения","символов / предложение",2]
  };
  const names = {
    "fantlab.general.characters":"Символы с пробелами",
    "fantlab.general.words":"Слова",
    "fantlab.vocabulary.unique_words":"Уникальные словоформы",
    "fantlab.vocabulary.active_dictionary":"Словарные формы",
    "fantlab.vocabulary.active_nondictionary":"Внесловарные формы",
    "scriptorium.general.sentences":"Количество предложений (расширение)"
  };
  const el = id => document.getElementById(id);
  const chartButtons = [...document.querySelectorAll("[data-chart]")];
  const chartSortButton = el("chart-sort");
  const chartCsvButton = el("chart-export-csv");
  const bookLinks = [...document.querySelectorAll("[data-book]")];
  const catalogCards = [...document.querySelectorAll("#books .book[data-catalog-key]")];
  const catalogFilter = el("catalog-filter");
  const catalogSearch = el("catalog-search");
  const catalogReset = el("catalog-reset");
  const one = el("choose-book");
  const search = el("search-metric");
  const status = el("table-status");
  const body = el("measurement-rows");
  const out = el("export-button");
  const singleMarkdownButton = el("export-markdown-button");
  const leftSelect = el("pair-left");
  const rightSelect = el("pair-right");
  const pairMetric = el("pair-metric");
  const pairSwapButton = el("pair-swap");
  const pairExportButton = el("pair-export");
  const pairCsvButton = el("pair-export-csv");
  const pairMarkdownButton = el("pair-export-markdown");
  const libraryCsvButton = el("library-export-csv");
  let data;
  let currentBook = "anna";
  let currentChart = "fantlab.dialogue.share_percent";
  let sortChart = false;

  function isNumeric(x) {
    return typeof x === "number" && Number.isFinite(x);
  }
  function verify(doc) {
    if (!doc || doc.schema !== "scriptorium-ru-reader-v2" ||
        doc.language_module !== "ru" ||
        doc.scientific_claim !== "DIAGNOSTIC_ONLY" ||
        doc.fantlab_input_identity !== "UNKNOWN" ||
        doc.comparability?.m2_parity_admissible !== false ||
        doc.counts?.m2_source_matched !== 0 ||
        doc.counts?.work_count !== 12 ||
        doc.counts?.measured_works !== 10 ||
        doc.counts?.awaiting_measurement !== 2 ||
        doc.counts?.metrics_total !== 269 ||
        doc.counts?.numeric_total !== 225 ||
        doc.counts?.unavailable_total !== 44 ||
        doc.language_modules?.ru?.measured_work_count !== 10 ||
        doc.language_modules?.en?.state !== "planned_not_measured" ||
        doc.language_modules?.en?.measured_work_count !== 0 ||
        !Array.isArray(doc.books) || doc.books.length !== 12) {
      throw Error("Русский каталог или научный статус изменён");
    }
    const census = {anna:[28,23],waves:[27,23],silver:[29,24],
                    karamazov:[29,24],hyperboloid:[29,24],beketova:[11,11],resurrection:[29,24],road:[29,24],oblomov:[29,24],humiliated:[29,24]};
    const seen = new Set();
    const editionKeys = new Set();
    let observed = 0, missing = 0;
    for (const book of doc.books) {
      if (typeof book.key !== "string" || seen.has(book.key) ||
          typeof book.candidate_id !== "string" || !book.candidate_id ||
          book.language !== "ru" ||
          !["ru","fr","en"].includes(book.original_language) ||
          typeof book.display_title !== "string" || !book.display_title ||
          typeof book.display_author !== "string" || !book.display_author ||
          typeof book.edition_id !== "string" || !book.edition_id ||
          typeof book.family_id !== "string" || !book.family_id ||
          typeof book.text_status !== "string" ||
          !Array.isArray(book.metrics)) throw Error("Некорректная идентичность книги");
      seen.add(book.key);
      const editionKey = book.family_id + ":" + book.edition_id + ":" + book.language;
      if (editionKeys.has(editionKey)) throw Error("Смешаны разные редакции");
      editionKeys.add(editionKey);
      if (book.original_language !== book.language &&
          (!book.translator || typeof book.translator.name !== "string" ||
           !book.translator.name.trim() || typeof book.translator.id !== "string")) {
        throw Error("Перевод без переводчика");
      }
      const expected = census[book.key];
      if (expected) {
        if (book.text_status !== "measured" ||
            book.measured !== expected[1] ||
            book.unavailable !== expected[0]-expected[1] ||
            book.metrics.length !== expected[0] ||
            typeof book.source_sha256 !== "string" ||
            !/^[a-f0-9]{64}$/.test(book.source_sha256) ||
            !/^https:\/\/github.com\/drevendev\/Scriptorium\/blob\/master\//.test(book.evidence_url)) {
          throw Error("Подмена измеренного источника или охвата");
        }
        if (book.key === "resurrection") {
          const characters=book.metrics.find(m=>m.id==="fantlab.general.characters");
          const words=book.metrics.find(m=>m.id==="fantlab.general.words");
          if (book.source_sha256 !== "2725a60a810d8aae4beff9dbc73ff85cf6da066b1c5272aaebf21addbe4ccaa0" ||
              characters?.actual !== 890835 || characters?.reference !== 881244 ||
              words?.actual !== 136129 || words?.reference !== 126457) {
            throw Error("Воскресение: подмена закреплённых измерений");
          }
        }
        if (book.key === "road") {
          const characters=book.metrics.find(m=>m.id==="fantlab.general.characters");
          const words=book.metrics.find(m=>m.id==="fantlab.general.words");
          if (book.source_sha256 !== "e33a28b8dcdb3ac339147c6587b27c182dd910784122b367db41bc93dfc2dbee" ||
              book.source_revision_id !== 5585836 ||
              book.edition_id !== "ru-wikisource-az-lib-oldid-5585836" ||
              characters?.actual !== 442656 || characters?.reference !== 438439 ||
              words?.actual !== 65072 || words?.reference !== 61299) {
            throw Error("Дорога в никуда: подмена закреплённой альтернативной редакции");
          }
        }
        if (book.key === "oblomov") {
          const chars=book.metrics.find(m=>m.id==="fantlab.general.characters");
          const words=book.metrics.find(m=>m.id==="fantlab.general.words");
          const sentences=book.metrics.find(m=>m.id==="scriptorium.general.sentences");
          if (book.candidate_id!=="goncharov-oblomov-azlib-ru" ||
              book.source_revision_id!==5724579 ||
              book.edition_id!=="ru-wikisource-az-lib-oldid-5724579" ||
              book.source_sha256!=="144a5ea17195e7ce10d69a5855a67781510dac51fd44237e1bc856536c3b3887" ||
              book.blob_sha1!=="98c9877658ab1dd7467e5a4b2fd0abb4103deb98" ||
              chars?.actual!==930248 || chars?.reference!==null ||
              words?.actual!==147447 || words?.reference!==null ||
              sentences?.actual!==14353 || sentences?.kind!=="extension" ||
              book.metrics.some(m=>m.reference!==null)) {
            throw Error("Обломов: подмена исходника или научного статуса");
          }
        }
        if (book.key === "humiliated") {
          const chars=book.metrics.find(m=>m.id==="fantlab.general.characters");
          const words=book.metrics.find(m=>m.id==="fantlab.general.words");
          const sentences=book.metrics.find(m=>m.id==="scriptorium.general.sentences");
          const dialogue=book.metrics.find(m=>m.id==="fantlab.dialogue.share_percent");
          if (book.candidate_id!=="dostoevsky-humiliated-and-insulted-azlib-ru" ||
              book.source_revision_id!==5611473 ||
              book.edition_id!=="ru-wikisource-az-lib-oldid-5611473" ||
              book.source_sha256!=="ffc6825db7f442c7df93136e8ddf90ce44be8801cdbaa727d5fe642db3fad8fa" ||
              book.blob_sha1!=="acfb3fb1cd0eb3713e45b062438253d19a68bcad" ||
              book.original_language!=="ru" || book.translator!==null ||
              chars?.actual!==713925 || words?.actual!==118157 ||
              sentences?.actual!==10381 || sentences?.kind!=="extension" ||
              dialogue?.actual!==56.66327827623132 ||
              book.metrics.some(m=>m.reference!==null)) {
            throw Error("Униженные и оскорбленные: подмена закреплённого источника или научного статуса");
          }
        }
        const fields = new Set();
        let available = 0;
        for (const m of book.metrics) {
          if (!m || typeof m.id !== "string" || fields.has(m.id) ||
              !/^(fantlab|scriptorium)\.[a-z0-9_.]+$/.test(m.id) ||
              !(m.actual === null || isNumeric(m.actual)) ||
              !(m.reference === null || isNumeric(m.reference)) ||
              !["not_run","unavailable","measured"].includes(m.status) ||
              (m.actual !== null) !== (m.status === "measured") ||
              !["candidate","extension"].includes(m.kind) ||
              (m.kind === "extension" && m.reference !== null)) {
            throw Error("Ненадёжное измерение или значение UNKNOWN");
          }
          fields.add(m.id);
          if (m.actual !== null) available++;
        }
        if (available !== expected[1]) throw Error("Изменено количество чисел");
        observed += available;
        missing += book.metrics.length-available;
      } else {
        if (book.text_status === "measured" ||
            book.metrics.length !== 0 ||
            book.measured !== 0 ||
            book.unavailable !== 0 ||
            typeof book.trace !== "string") throw Error("Нельзя считать заявку измеренной книгой");
      }
    }
    if (seen.size !== 12 || Object.keys(census).some(x=>!seen.has(x)) ||
        observed !== 225 || missing !== 44 ||
        doc.books.filter(b=>b.text_status === "measured").length !== 10 ||
        doc.books.filter(b=>b.translator).length !== 2) throw Error("Подмена итогов каталога");
    // The static cards must match the verified evidence record exactly.
    const cardKeys=catalogCards.map(card=>card.dataset.catalogKey);
    if (cardKeys.length!==doc.books.length ||
        new Set(cardKeys).size!==doc.books.length ||
        doc.books.some(book=>{
          const card=catalogCards.find(c=>c.dataset.catalogKey===book.key);
          return !card || card.dataset.status!==(
            book.text_status==="measured"?"measured":"pending");
        })) throw Error("Карточки библиотеки не соответствуют проверенным данным");
    const measured = doc.books.filter(b=>b.text_status === "measured");
    const chartProfiles=["metrics","normalization","dialogue","punctuation"];
    const baseline=measured[0]?.profiles;
    for (const book of measured) {
      if (!chartProfiles.every(k=>typeof baseline?.[k]==="string" &&
           book.profiles?.[k]===baseline[k])) {
        throw Error("Несопоставимые профили измерений");
      }
    }
    for (const book of measured) {
      const needed = Object.keys(metrics);
      if (book.key === "beketova") {
        // The distinct translated version has ten shared observed metrics but
        // not every diagnostic field in the original FantLab registry.
        if (!["fantlab.dialogue.share_percent",
               "fantlab.general.mean_sentence_length_chars",
               "fantlab.punctuation.comma.per_1000_words"].every(id=>
                 book.metrics.some(row=>row.id===id&&isNumeric(row.actual)))) {
          throw Error("Недоступна сопоставимая метрика перевода");
        }
      } else if (!needed.slice(0,3).every(id=>
                   book.metrics.some(row=>row.id===id&&isNumeric(row.actual)))) {
        throw Error("Отсутствуют проверенные значения для диаграммы");
      }
    }
  }

  function getBook(key) {
    return data.books.find(b=>b.key===key && b.text_status==="measured");
  }
  function lookup(book,id) {
    return book.metrics.find(row=>row.id===id);
  }
  function pretty(x,places=2) {
    return x === null ? "—" :
      new Intl.NumberFormat("ru-RU",{maximumFractionDigits:places}).format(x);
  }
  function exact(x) {
    return x === null ? "UNKNOWN" : String(x);
  }
  function label(id) {
    return metrics[id]?.[0] || names[id] || id.replace(/^fantlab\./,"").replaceAll("_"," ").replaceAll("."," · ");
  }
  function unit(id) {
    if (metrics[id]) return metrics[id][1];
    if (id === "scriptorium.general.sentences") return "предложения";
    if (id === "fantlab.general.characters") return "символы с пробелами";
    if (id === "fantlab.general.words") return "слова";
    if (id.startsWith("fantlab.vocabulary.")) return "словоформы / окно, по профилю";
    if (id.includes(".punctuation.")) return "на 1000 слов";
    if (id.endsWith("_percent")) return "%";
    return "кандидатные единицы";
  }
  function insertText(parent,tag,value,cls) {
    const node = document.createElement(tag);
    node.textContent = value;
    if (cls) node.className = cls;
    parent.appendChild(node);
    return node;
  }
  // Source-unmatched arithmetic only, not parity, tolerance or a pass/fail score.
  function diagnosticDelta(m) {
    if (m.kind==="extension") return "N/A";
    if (!isNumeric(m.actual)||!isNumeric(m.reference)) return "—";
    const delta=m.actual-m.reference;
    if (!Number.isFinite(delta)) return "—";
    if (delta===0) return "0";
    const whole=Number.isInteger(m.actual)&&Number.isInteger(m.reference);
    const magnitude=Math.abs(delta);
    const display=!whole&&magnitude<0.0005?"<0,001":pretty(magnitude,whole?0:3);
    return (delta>0?"+":"−")+display+(unit(m.id)==="%"?" п.п.":"");
  }
  function makeTableRow(m) {
    const tr=document.createElement("tr");
    const th=insertText(tr,"th",label(m.id));
    th.scope="row";
    insertText(th,"code",m.id);
    insertText(tr,"td",m.actual===null?m.status.toUpperCase():exact(m.actual));
    insertText(tr,"td",m.kind==="extension"?"N/A":exact(m.reference));
    insertText(tr,"td",diagnosticDelta(m),"benchmark-delta");
    insertText(tr,"td",unit(m.id));
    insertText(tr,"td",m.kind==="extension"?"Расширение Scriptorium":
               m.actual===null?m.status.toUpperCase():"Диагностика · несовпавший источник");
    return tr;
  }
  // Presentation-only filtering; never promote research leads to measured books.
  // Static provenance links remain visible when JS or verified data is unavailable.
  function updateCatalog() {
    const mode=["all","measured","pending","translated"].includes(catalogFilter.value)
      ? catalogFilter.value : "all";
    const query=catalogSearch.value.normalize("NFKC").toLocaleLowerCase("ru")
      .replace(/ё/g,"е").trim();
    let shown=0, measured=0, pending=0;
    for (const card of catalogCards) {
      const book=data.books.find(b=>b.key===card.dataset.catalogKey);
      if (!book) throw Error("Нет проверенного источника для карточки");
      const isMeasured=book.text_status==="measured";
      const isTranslation=book.original_language!==book.language;
      // Search only validated edition, author and translator metadata, never book text.
      const text=[book.display_title,book.display_author,book.translator?.name||""]
        .join(" ").normalize("NFKC").toLocaleLowerCase("ru").replace(/ё/g,"е");
      const modeMatches=mode==="all" ||
        (mode==="measured" && isMeasured) ||
        (mode==="pending" && !isMeasured) ||
        (mode==="translated" && isTranslation);
      const visible=modeMatches && (!query || text.includes(query));
      card.hidden=!visible;
      if (visible) {
        shown++;
        if (isMeasured) measured++; else pending++;
      }
    }
    el("catalog-empty").hidden=shown!==0;
    el("catalog-filter-status").textContent=shown
      ? "Показано "+shown+" из "+catalogCards.length+" книг: "+
        measured+" измерено, "+pending+" в подготовке. Переводы — отдельные редакции."
      : "Книг не найдено. Очистите поиск или измените фильтр.";
    // A share link is explicit: typing never changes history or sends a query.
    const raw=catalogSearch.value.trim();
    const share=el("share-catalog");
    share.hidden=!safeCatalogQuery(raw);
    if (!share.hidden) {
      share.href="?catalog="+encodeURIComponent(mode)+
        (raw?"&q="+encodeURIComponent(raw):"")+"#books";
      share.textContent=raw ? "Ссылка на этот поиск ↗" : "Ссылка на выбранный список ↗";
    } else {
      share.removeAttribute("href");
    }
  }

  // An explicit empty-state reset preserves unrelated work/comparison links.
  function resetCatalog() {
    catalogFilter.value="all";
    catalogSearch.value="";
    try {
      const url=new URL(window.location.href);
      url.searchParams.delete("catalog");
      url.searchParams.delete("q");
      window.history.replaceState(null,"",url);
    } catch (_) {
      // Local file previews can disallow history changes; reset still works.
    }
    updateCatalog();
    catalogSearch.focus();
  }

  function safeCatalogQuery(raw) {
    return typeof raw==="string" && raw.length<=120 &&
      !/[\u0000-\u001f\u007f]/u.test(raw);
  }

  // Reject foreign/oversized URL input, preserve all static cards on failed JSON.
  function catalogFromUrl() {
    const params=new URLSearchParams(window.location.search);
    const requested=params.get("catalog");
    const mode=["all","measured","pending","translated"].includes(requested)
      ? requested : "all";
    const raw=params.get("q")||"";
    return {mode,query:safeCatalogQuery(raw)?raw:""};
  }
  function restoreCatalogFromUrl() {
    const state=catalogFromUrl();
    catalogFilter.value=state.mode;
    catalogSearch.value=state.query;
    updateCatalog();
  }

  function updateSingle() {
    const book=getBook(currentBook);
    if (!book) return;
    const q=search.value.trim().toLocaleLowerCase("ru");
    const selected=book.metrics.filter(m=>!q||(
      m.id+" "+label(m.id)+" "+unit(m.id)).toLocaleLowerCase("ru").includes(q));
    const nodes=document.createDocumentFragment();
    for (const m of selected) nodes.appendChild(makeTableRow(m));
    if (!selected.length) {
      const row=document.createElement("tr");
      const td=insertText(row,"td","Ничего не найдено. Очистите поиск, чтобы увидеть все метрики.");
      td.colSpan=6; nodes.appendChild(row);
    }
    body.replaceChildren(nodes);
    el("table-caption").textContent=book.display_title+" · "+book.metrics.length+
      " метрик, нет подтверждённого совпадения с FantLab";
    status.textContent=selected.length+" из "+book.metrics.length+" полей; "+
      book.measured+" измерены, "+book.unavailable+" недоступны; M2 0/5";
    el("evidence-source").href=book.evidence_url;
    const fantlab=el("fantlab-reference");
    if (book.fantlab_url) {
      fantlab.hidden=false; fantlab.href=book.fantlab_url;
      fantlab.textContent="Референс FantLab ↗";
    } else {
      fantlab.hidden=true;fantlab.removeAttribute("href");
    }
  }
  // The URL identifies an allow-listed measured edition, never a data source.
  // Unknown, pending and foreign keys resolve to the honest static Anna fallback.
  function bookFromUrl() {
    const requested = new URLSearchParams(window.location.search).get("book");
    return getBook(requested) ? requested : "anna";
  }
  function selectBook(key, addHistory=false, focusHeading=false) {
    const book = getBook(key);
    if (!book) return;
    currentBook = key;
    one.value = key;
    search.value = "";
    updateSingle();
    const direct = el("share-work");
    direct.href = "?book=" + encodeURIComponent(key) + "#measurements";
    direct.textContent = "Прямая ссылка на «" + book.display_title + "» ↗";
    if (addHistory) {
      const url = new URL(window.location.href);
      url.searchParams.set("book", key);
      url.hash = "measurements";
      window.history.pushState(null, "", url);
    }
    if (focusHeading) {
      el("measurements").scrollIntoView({block:"start",behavior:"auto"});
      el("measurements-title").focus({preventScroll:true});
    }
  }

  // The frozen editions do not share every measured field; missing is not zero.
  function updateChart() {
    const conf=metrics[currentChart];
    if (!conf) throw Error("Показатель диаграммы не разрешён");
    const rows=data.books.filter(b=>b.text_status==="measured").map((b,ordinal)=>{
      const item=lookup(b,currentChart);
      return {title:b.display_title,value:item&&isNumeric(item.actual)?item.actual:null,ordinal};
    });
    // Presentation-only ordering; ties stay in catalog order and unknown is not zero.
    if (sortChart) rows.sort((a,b)=>{
      if (a.value===null) return b.value===null ? a.ordinal-b.ordinal : 1;
      if (b.value===null) return -1;
      return b.value-a.value || a.ordinal-b.ordinal;
    });
    const known=rows.filter(row=>row.value!==null);
    const high=Math.max(0,...known.map(row=>row.value));
    const nodes=document.createDocumentFragment();
    const tableNodes=document.createDocumentFragment();
    for (const row of rows) {
      const container=document.createElement("div");
      container.className="chart-row"+(row.value===null?" chart-missing":"");
      insertText(container,"span",row.title);
      const track=insertText(container,"div","");
      track.className="bar-track";track.setAttribute("aria-hidden","true");
      if (row.value!==null) {
        const inner=insertText(track,"span","");
        inner.style.width=(high>0?100*row.value/high:0).toFixed(2)+"%";
      }
      insertText(container,"strong",row.value===null?"нет данных":
                 pretty(row.value,conf[2])+(conf[1]==="%"?"%":""));
      nodes.appendChild(container);
      const tableRow=document.createElement("tr");
      insertText(tableRow,"th",row.title).scope="row";
      insertText(tableRow,"td",row.value===null?"нет данных":exact(row.value));
      insertText(tableRow,"td",conf[1]);
      tableNodes.appendChild(tableRow);
    }
    el("chart-series").replaceChildren(nodes);
    el("chart-table-rows").replaceChildren(tableNodes);
    el("chart-table-caption").textContent=conf[0]+" · "+conf[1]+
      " · "+known.length+" из "+rows.length+" измеренных книг";
    el("chart-unit").textContent=conf[0]+" · "+conf[1]+
      " · доступно для "+known.length+" из "+rows.length+
      " книг; нет данных ≠ 0. Числа округлены до "+conf[2]+" знаков.";
    for (const btn of chartButtons) {
      btn.setAttribute("aria-pressed",String(btn.dataset.chart===currentChart));
    }
    chartSortButton.setAttribute("aria-pressed",String(sortChart));
    chartSortButton.textContent=sortChart ? "Вернуть порядок каталога" : "Сортировать по значению ↓";
  }

  // Only allow-listed metric and descending order can control a shared chart.
  function chartFromUrl() {
    const requested = new URLSearchParams(window.location.search).get("metric");
    return Object.prototype.hasOwnProperty.call(metrics, requested) ? requested :
      "fantlab.dialogue.share_percent";
  }
  function chartOrderFromUrl() {
    return new URLSearchParams(window.location.search).get("chart_order")==="ranked";
  }
  function restoreChartFromUrl() {
    sortChart=chartOrderFromUrl();
    selectChart(chartFromUrl());
  }
  function selectChart(id, addHistory=false) {
    if (!Object.prototype.hasOwnProperty.call(metrics, id)) return;
    currentChart = id;
    updateChart();
    const link = el("share-chart");
    link.href = "?metric=" + encodeURIComponent(id) +
      (sortChart ? "&chart_order=ranked" : "") + "#charts";
    link.textContent = "Прямая ссылка на диаграмму «" + metrics[id][0] + "»" +
      (sortChart ? " (по убыванию)" : "") + " ↗";
    if (addHistory) {
      const url = new URL(window.location.href);
      url.searchParams.set("metric", id);
      if (sortChart) url.searchParams.set("chart_order","ranked");
      else url.searchParams.delete("chart_order");
      url.hash = "charts";
      window.history.pushState(null, "", url);
    }
  }

  const pairedIds = [
    "fantlab.dialogue.share_percent",
    "fantlab.dialogue.author_text_inside_dialogue_percent",
    "fantlab.dialogue.mean_dialogue_sentence_length_chars",
    "fantlab.dialogue.mean_narration_sentence_length_chars",
    "fantlab.general.mean_sentence_length_chars",
    "fantlab.general.mean_word_length_chars",
    "fantlab.punctuation.comma.per_1000_words",
    "fantlab.punctuation.dash.per_1000_words",
    "fantlab.punctuation.question.per_1000_words"
  ];
  function sharedPairRows(a,b) {
    return pairedIds.flatMap(id=>{
      const av=lookup(a,id),bv=lookup(b,id);
      return (av&&bv&&isNumeric(av.actual)&&isNumeric(bv.actual))?
        [{id,left:av.actual,right:bv.actual}]:[];
    });
  }
  // The visual table includes unavailable eligible metrics. Numeric exports remain
  // restricted to fields actually measured in both independently bound editions.
  function pairCoverageRows(a,b) {
    return pairedIds.map(id=>{
      const l=lookup(a,id),r=lookup(b,id);
      return {
        id,
        left:l&&isNumeric(l.actual)?l.actual:null,
        right:r&&isNumeric(r.actual)?r.actual:null
      };
    });
  }
  // Source-free, edition-bound and deterministic. The export contains only
  // allow-listed measured fields already displayed in the comparison table.
  function buildPairExport(leftKey,rightKey) {
    const a=getBook(leftKey),b=getBook(rightKey);
    if (!a||!b||a.key===b.key) return null;
    const profiles=["metrics","normalization","dialogue","vocabulary","punctuation"];
    if (!profiles.every(profile=>
      typeof a.profiles?.[profile]==="string" &&
      a.profiles[profile]===b.profiles?.[profile])) return null;
    const rows=sharedPairRows(a,b);
    if (!rows.length) return null;
    const identity=book=>({
      key:book.key,candidate_id:book.candidate_id,
      title:book.display_title,author:book.display_author,
      analysis_language:book.language,original_language:book.original_language,
      translator:book.translator||null,edition_id:book.edition_id,
      source_sha256:book.source_sha256,evidence_url:book.evidence_url
    });
    return {
      schema:"scriptorium-ru-pair-comparison-v1",
      scientific_claim:"DIAGNOSTIC_ONLY",
      fantlab_input_identity:"UNKNOWN",m2_source_matched:0,
      text_included:false,comparison_direction:"right_minus_left",
      measurement_profiles:Object.fromEntries(profiles.map(p=>[p,a.profiles[p]])),
      left:identity(a),right:identity(b),
      metrics:rows.map(row=>{
        const measurementUnit=unit(row.id);
        return {
          id:row.id,unit:measurementUnit,
          delta_unit:measurementUnit==="%"?"percentage_points":measurementUnit,
          left_actual:row.left,right_actual:row.right,
          delta_right_minus_left:row.right-row.left
        };
      })
    };
  }
  function exportPair() {
    const result=buildPairExport(leftSelect.value,rightSelect.value);
    if (!result) {
      pairExportButton.disabled=true;
      return;
    }
    const blob=new Blob([JSON.stringify(result,null,2)+"\n"],{type:"application/json"});
    const url=URL.createObjectURL(blob);
    const link=document.createElement("a");
    link.href=url;
    link.download="scriptorium-pair-"+result.left.key+"-"+result.right.key+".json";
    document.body.appendChild(link);link.click();link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }


  // Flat CSV from the same validated evidence-bound JSON comparison.
  // Text is quoted and neutralized against spreadsheet formulas.
  function csvText(value) {
    const raw=String(value??"");
    // Keep the full original text after the apostrophe. Unicode format marks
    // and full-width operators can hide spreadsheet formulas on import.
    const unsafe=/^[\t\r\n\u0000]/u.test(raw) ||
      /^[\s\p{Cf}]*[=+@＝＋－＠-]/u.test(raw);
    const safe=unsafe?"'"+raw:raw;
    return '"'+safe.replaceAll('"','""')+'"';
  }
  function serializePairCsv(report) {
    // Keep translation identity inspectable even when JSON is not retained.
    for (const edition of [report.left,report.right]) {
      if (!["ru","fr","en"].includes(edition.original_language) ||
          edition.analysis_language !== "ru" ||
          (edition.original_language !== edition.analysis_language &&
           (!edition.translator?.id || !edition.translator?.name))) {
        throw Error("Неполное происхождение редакции для CSV");
      }
    }
    const headers=[
      "schema","csv_schema","scientific_claim","fantlab_input_identity","m2_source_matched",
      "comparison_direction","measurement_profiles",
      "left_key","left_candidate_id","left_title","left_author",
      "left_original_language","left_analysis_language","left_translator_id","left_translator",
      "left_edition_id","left_source_sha256","left_evidence_url",
      "right_key","right_candidate_id","right_title","right_author",
      "right_original_language","right_analysis_language","right_translator_id","right_translator",
      "right_edition_id","right_source_sha256","right_evidence_url",
      "metric_id","unit","delta_unit","left_actual","right_actual","delta_right_minus_left"
    ];
    const lines=report.metrics.map(metric=>{
      const fields=[
        report.schema,"scriptorium-ru-pair-csv-v2",report.scientific_claim,
        report.fantlab_input_identity,report.m2_source_matched,report.comparison_direction,
        JSON.stringify(report.measurement_profiles),
        report.left.key,report.left.candidate_id,report.left.title,report.left.author,
        report.left.original_language,report.left.analysis_language,
        report.left.translator?.id||"",report.left.translator?.name||"",
        report.left.edition_id,report.left.source_sha256,report.left.evidence_url,
        report.right.key,report.right.candidate_id,report.right.title,report.right.author,
        report.right.original_language,report.right.analysis_language,
        report.right.translator?.id||"",report.right.translator?.name||"",
        report.right.edition_id,report.right.source_sha256,report.right.evidence_url,
        metric.id,metric.unit,metric.delta_unit,
        metric.left_actual,metric.right_actual,metric.delta_right_minus_left
      ];
      if (fields.length!==headers.length) throw Error("Неполная схема CSV");
      return fields.slice(0,-3).map(csvText).concat(fields.slice(-3).map(String)).join(",");
    });
    return "\uFEFF"+[headers.join(","),...lines].join("\r\n")+"\r\n";
  }
  function exportPairCsv() {
    const result=buildPairExport(leftSelect.value,rightSelect.value);
    if (!result) {
      pairCsvButton.disabled=true;
      return;
    }
    const blob=new Blob([serializePairCsv(result)],{type:"text/csv;charset=utf-8"});
    const url=URL.createObjectURL(blob);
    const link=document.createElement("a");
    link.href=url;
    link.download="scriptorium-pair-"+result.left.key+"-"+result.right.key+".csv";
    document.body.appendChild(link);link.click();link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }


  // Markdown keeps all nine eligible metric slots, including honest missing cells.
  function markdownCell(value) {
    return String(value??"")
      .replace(/[\u0000-\u001f\u007f-\u009f\u2028\u2029\u202a-\u202e\u2066-\u2069]/g," ")
      .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")
      .replace(/\\/g,"\\\\").replace(/\|/g,"\\|")
      .replace(/[\x60*_\[\]]/g,"\\$&");
  }
  function serializePairMarkdown(report, coverage) {
    if (report?.schema!=="scriptorium-ru-pair-comparison-v1" ||
        report.scientific_claim!=="DIAGNOSTIC_ONLY" ||
        report.fantlab_input_identity!=="UNKNOWN" || report.m2_source_matched!==0 ||
        report.text_included!==false || report.comparison_direction!=="right_minus_left" ||
        !Array.isArray(report.metrics) || !report.metrics.length ||
        !Array.isArray(coverage) || coverage.length!==pairedIds.length)
      throw Error("Недостоверный научный статус Markdown-сравнения");
    for (const edition of [report.left,report.right]) {
      if (!edition || edition.analysis_language!=="ru" ||
          !["ru","fr","en"].includes(edition.original_language) ||
          !["title","author","candidate_id","edition_id","evidence_url"].every(k=>
            typeof edition[k]==="string" && edition[k].length>0) ||
          !/^[a-f0-9]{64}$/.test(edition.source_sha256||"") ||
          (edition.original_language!=="ru" &&
            (!edition.translator?.id || !edition.translator?.name)))
        throw Error("Неполное происхождение редакции Markdown-сравнения");
    }
    const profileKeys=["metrics","normalization","dialogue","vocabulary","punctuation"];
    if (!profileKeys.every(k=>typeof report.measurement_profiles?.[k]==="string" &&
        report.measurement_profiles[k].length>0))
      throw Error("Нет профиля Markdown-сравнения");
    const observed=new Map(report.metrics.map(m=>[m.id,m]));
    if (observed.size!==report.metrics.length ||
        report.metrics.some(m=>!pairedIds.includes(m.id)))
      throw Error("Неизвестная метрика Markdown-сравнения");
    const table=coverage.map((row,i)=>{
      if (row.id!==pairedIds[i] ||
          ![row.left,row.right].every(n=>n===null||isNumeric(n)))
        throw Error("Неполные измерения Markdown-сравнения");
      const both=row.left!==null&&row.right!==null,m=observed.get(row.id);
      if (both!==Boolean(m) || (both &&
          (m.left_actual!==row.left || m.right_actual!==row.right ||
           m.unit!==unit(row.id) ||
           m.delta_unit!==(m.unit==="%"?"percentage_points":m.unit) ||
           m.delta_right_minus_left!==row.right-row.left)))
        throw Error("Несогласованные значения Markdown-сравнения");
      return "| "+[
        label(row.id)+" ("+row.id+")",
        row.left===null?"нет данных":String(row.left),
        row.right===null?"нет данных":String(row.right),
        both?String(m.delta_right_minus_left):"нет совместного измерения",
        unit(row.id)+(unit(row.id)==="%"?" (Δ в п.п.)":"")
      ].map(markdownCell).join(" | ")+" |";
    });
    const provenance=[
      ["Произведение","title"],["Автор","author"],["Работа (ID)","candidate_id"],
      ["Редакция (ID)","edition_id"],["Язык оригинала","original_language"],
      ["Язык анализа","analysis_language"],["SHA-256","source_sha256"],
      ["Источник измерений","evidence_url"]
    ].map(([title,key])=>"| "+[title,report.left[key],report.right[key]]
      .map(markdownCell).join(" | ")+" |");
    for (const [index,title,key] of [[6,"Переводчик (ID)","id"],[7,"Переводчик","name"]])
      provenance.splice(index,0,"| "+[
        title,report.left.translator?.[key]||"не применимо",
        report.right.translator?.[key]||"не применимо"
      ].map(markdownCell).join(" | ")+" |");
    const profiles=profileKeys.map(k=>"| "+[k,report.measurement_profiles[k]]
      .map(markdownCell).join(" | ")+" |");
    return [
      "# Scriptorium · сравнение двух измеренных русскоязычных редакций","",
      "**DIAGNOSTIC_ONLY** · вход FantLab: **UNKNOWN** · **M2: 0/5**.",
      "Описательная диагностика; разница не доказывает влияние автора или переводчика.",
      "Не сравнивает иностранный оригинал с переводом. Исходные тексты не включены.","",
      "## Редакции и происхождение","","| Поле | Левая | Правая |",
      "| --- | --- | --- |",...provenance,"",
      "## Версии алгоритмов","","| Профиль | Версия |","| --- | --- |",...profiles,"",
      "## Показатели","",
      report.metrics.length+" из "+pairedIds.length+" метрик измерены с обеих сторон. «Нет данных» не ноль.",
      "Направление Δ: **правая − левая**; проценты сравниваются в процентных пунктах.","",
      "| Метрика (ID) | Левая | Правая | Δ правая − левая | Единица |",
      "| --- | ---: | ---: | ---: | --- |",...table,""
    ].join("\n");
  }
  function exportPairMarkdown() {
    const result=buildPairExport(leftSelect.value,rightSelect.value);
    if (!result) { pairMarkdownButton.disabled=true; return; }
    const text=serializePairMarkdown(result,pairCoverageRows(
      getBook(result.left.key),getBook(result.right.key)));
    const blob=new Blob([text],{type:"text/markdown;charset=utf-8"});
    const url=URL.createObjectURL(blob);
    const link=document.createElement("a");
    link.href=url;
    link.download="scriptorium-pair-"+result.left.key+"-"+result.right.key+".md";
    document.body.appendChild(link);link.click();link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }

  // Export every verified observed/unavailable field without admitting pending works.
  // UNKNOWN is an empty numeric cell with an explicit status, never the number zero.
  // CSV never implies FantLab source/algorithm parity and contains no source text.
  function serializeLibraryCsv(doc) {
    verify(doc);
    const headers=[
      "export_schema","scientific_claim","fantlab_input_identity","m2_source_matched",
      "book_key","candidate_id","title","author","original_language","analysis_language",
      "translator_id","translator_name","edition_id","source_sha256","source_revision_id",
      "source_evidence_url","fantlab_reference_url","normalization_profile","metrics_profile",
      "dialogue_profile","vocabulary_profile","punctuation_profile",
      "metric_id","unit","actual","actual_status","fantlab_reference_display",
      "reference_status","metric_kind","comparison_class"
    ];
    const lines=[];
    for (const book of doc.books) {
      if (book.text_status!=="measured") continue;
      for (const metric of book.metrics) {
        const fields=[
          "scriptorium-ru-metric-catalog-csv-v1","DIAGNOSTIC_ONLY","UNKNOWN",0,
          book.key,book.candidate_id,book.display_title,book.display_author,
          book.original_language,book.language,book.translator?.id||"",
          book.translator?.name||"",book.edition_id,book.source_sha256,
          book.source_revision_id??"",book.evidence_url,book.fantlab_url||"",
          book.profiles.normalization,book.profiles.metrics,book.profiles.dialogue,
          book.profiles.vocabulary,book.profiles.punctuation,
          metric.id,unit(metric.id),metric.actual===null?"":metric.actual,
          metric.status,metric.reference===null?"":metric.reference,
          metric.kind==="extension"?"NOT_APPLICABLE":
            metric.reference===null?"UNKNOWN":"DISPLAY_REFERENCE_ONLY",
          metric.kind,metric.kind==="extension"?"EXTENSION_ONLY":"DIAGNOSTIC_UNMATCHED_SOURCE"
        ];
        if (fields.length!==headers.length) throw Error("Некорректная структура CSV");
        lines.push(fields.map(csvText).join(","));
      }
    }
    if (lines.length!==doc.counts.metrics_total) throw Error("Неполная таблица измерений");
    return "\uFEFF"+[headers.join(","),...lines].join("\r\n")+"\r\n";
  }
  function exportLibraryCsv() {
    const payload=serializeLibraryCsv(data);
    const blob=new Blob([payload],{type:"text/csv;charset=utf-8"});
    const url=URL.createObjectURL(blob);
    const link=document.createElement("a");
    link.href=url;
    link.download="scriptorium-ru-measured-metrics.csv";
    document.body.appendChild(link);link.click();link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }


  // Exact values behind a chart; absent field != NOT_RUN != numeric zero.
  function serializeChartCsv(doc, id, sorted) {
    if (!Object.prototype.hasOwnProperty.call(metrics,id))
      throw Error("Показатель CSV не разрешён");
    if (!doc || doc.schema!=="scriptorium-ru-reader-v2" ||
        doc.scientific_claim!=="DIAGNOSTIC_ONLY" ||
        doc.fantlab_input_identity!=="UNKNOWN" ||
        doc.counts?.m2_source_matched!==0 ||
        doc.counts?.measured_works!==10 || !Array.isArray(doc.books))
      throw Error("Не подтверждён научный статус диаграммы");
    const measured=doc.books.filter(book=>book.text_status==="measured");
    if (measured.length!==10) throw Error("Неполный измеренный каталог");
    const profiles=["metrics","normalization","dialogue","punctuation"];
    const baseline=measured[0].profiles;
    const rows=measured.map((book,ordinal)=>{
      if (!/^[a-f0-9]{64}$/.test(book.source_sha256||"") ||
          book.language!=="ru" || !["ru","fr","en"].includes(book.original_language) ||
          !book.edition_id || !book.evidence_url ||
          !profiles.every(k=>typeof book.profiles?.[k]==="string" &&
             book.profiles[k]===baseline[k]) ||
          (book.original_language!==book.language &&
             (!book.translator?.id || !book.translator?.name)))
        throw Error("CSV: неподтверждённая редакция или профиль");
      const field=lookup(book,id);
      if (field && (!["measured","not_run","unavailable"].includes(field.status) ||
                    (field.status==="measured")!==isNumeric(field.actual)))
        throw Error("CSV: неверный статус измерения");
      return {book,ordinal,value:field&&isNumeric(field.actual)?field.actual:null,
              status:field?.status||"not_recorded"};
    });
    if(sorted) rows.sort((a,b)=>{
      if(a.value===null)return b.value===null?a.ordinal-b.ordinal:1;
      if(b.value===null)return -1;
      return b.value-a.value||a.ordinal-b.ordinal;
    });
    const header=["schema","scientific_claim","fantlab_input_identity","m2_source_matched",
      "metric_id","metric_label","unit","sort_order","position","book_key",
      "title","author","original_language","analysis_language","translator_id",
      "translator","edition_id","source_sha256","evidence_url","actual","status",
      "metrics_profile","normalization_profile","dialogue_profile","punctuation_profile"];
    const lines=rows.map(({book,value,status},i)=>{
      const cells=["scriptorium-ru-chart-csv-v1",doc.scientific_claim,
        doc.fantlab_input_identity,doc.counts.m2_source_matched,id,
        metrics[id][0],metrics[id][1],sorted?"value_desc":"catalog",i+1,
        book.key,book.display_title,book.display_author,
        book.original_language,book.language,book.translator?.id||"",
        book.translator?.name||"",book.edition_id,book.source_sha256,
        book.evidence_url,value===null?"":String(value),status,
        ...profiles.map(k=>book.profiles[k])];
      if (cells.length!==header.length) throw Error("CSV: неполная строка");
      return cells.map(csvText).join(",");
    });
    return "\uFEFF"+[header.join(","),...lines].join("\r\n")+"\r\n";
  }
  function exportChartCsv() {
    const payload=serializeChartCsv(data,currentChart,sortChart);
    const blob=new Blob([payload],{type:"text/csv;charset=utf-8"});
    const url=URL.createObjectURL(blob);
    const link=document.createElement("a");
    link.href=url;
    link.download="scriptorium-chart-"+currentChart+(sortChart?"-ranked":"")+".csv";
    document.body.appendChild(link);link.click();link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }

  function pairEditionDescription(book, side) {
    const translated=book.original_language!==book.language;
    const origin={fr:"французского",en:"английского",ru:"русского"};
    const type=translated
      ? "русский перевод с "+(origin[book.original_language]||book.original_language)+
        "; переводчик: "+book.translator.name
      : "русский оригинал";
    return side+" · "+book.display_title+" — "+type+
      ". Редакция: "+book.edition_id+
      " · SHA-256: "+book.source_sha256.slice(0,12)+"…";
  }
  function updatePairEditionContext(left,right) {
    el("pair-left-edition").textContent=pairEditionDescription(left,"Слева");
    el("pair-right-edition").textContent=pairEditionDescription(right,"Справа");
    const translated=left.original_language!==left.language ||
      right.original_language!==right.language;
    el("pair-edition-caveat").textContent=translated
      ? "Сопоставляются две измеренные русскоязычные редакции, НЕ французский/английский оригинал с переводом. Разница не доказывает вклад переводчика или автора; FantLab parity неизвестна."
      : "Сопоставляются две отдельные русскоязычные редакции. Разница не доказывает влияние автора или совпадение с входом FantLab.";
  }

  function updatePair() {
    pairExportButton.disabled=true;
    pairCsvButton.disabled=true;
    pairMarkdownButton.disabled=true;
    const a=getBook(leftSelect.value),b=getBook(rightSelect.value);
    if (!a||!b) throw Error("Книга отсутствует в измеренном корпусе");
    updatePairEditionContext(a,b);
    const matchingProfiles=["metrics","normalization","dialogue","vocabulary","punctuation"];
    if (!matchingProfiles.every(profile=>
      typeof a.profiles?.[profile]==="string" &&
      a.profiles[profile]===b.profiles?.[profile])) {
      el("pair-status").textContent="Профили алгоритмов несовместимы — сравнение отключено.";
      el("pair-rows").replaceChildren();
      el("paired-graphic").replaceChildren();
      return;
    }
    if (a.key===b.key) {
      el("pair-status").textContent="Выберите две разные книги.";
      el("pair-rows").replaceChildren();
      el("paired-graphic").replaceChildren();
      return;
    }
    const rows=sharedPairRows(a,b);
    const coverage=pairCoverageRows(a,b);
    const fragment=document.createDocumentFragment();
    for (const m of coverage) {
      const tr=document.createElement("tr");
      insertText(tr,"th",label(m.id)).scope="row";
      insertText(tr,"td",m.left===null?"нет данных":exact(m.left));
      insertText(tr,"td",m.right===null?"нет данных":exact(m.right));
      const comparable=m.left!==null&&m.right!==null;
      const d=comparable?m.right-m.left:null;
      insertText(tr,"td",d===null?"— (нет совместного измерения)":
        (d>0?"+":"")+pretty(d,3));
      insertText(tr,"td",unit(m.id)+(unit(m.id)==="%"?" · Δ в п.п.":""));
      fragment.appendChild(tr);
    }
    el("pair-rows").replaceChildren(fragment);
    pairExportButton.disabled=rows.length===0;
    pairCsvButton.disabled=rows.length===0;
    pairMarkdownButton.disabled=rows.length===0;
    el("pair-caption").textContent=a.display_title+" → "+b.display_title+" · правая минус левая";
    el("pair-status").textContent=rows.length+" из "+pairedIds.length+
      " показателей измерены в обеих книгах; остальные отмечены «нет данных». "+
      (a.translator||b.translator?"Одна из версий — русский перевод. ":"")+
      "Описательная диагностика, не FantLab parity.";
    const id=pairMetric.value;
    const curr=rows.find(m=>m.id===id);
    const graph=document.createDocumentFragment();
    if (!curr) {
      insertText(graph,"p","Эта метрика недоступна хотя бы для одного текста. Подмена нулём запрещена.");
    } else {
      insertText(graph,"h3",label(curr.id)+" · "+unit(curr.id));
      const max=Math.max(curr.left,curr.right);
      const items=[
        {label:a.display_title,value:curr.left,tone:"a"},
        {label:b.display_title,value:curr.right,tone:"b"}
      ];
      for (const item of items) {
        const group=insertText(graph,"div","","pair-row");
        insertText(group,"span",item.label);
        const track=insertText(group,"div","","pair-track");
        track.setAttribute("aria-hidden","true");
        const fill=insertText(track,"span","","pair-fill-"+item.tone);
        fill.style.width=(max>0?100*item.value/max:0).toFixed(2)+"%";
        insertText(group,"strong",pretty(item.value,2)+(unit(curr.id)==="%"?"%":""));
      }
      insertText(graph,"p","Точные значения и разницы доступны в таблице ниже.","graph-caption");
    }
    el("paired-graphic").replaceChildren(graph);
  }
  // Paired links carry only selected chart options, never arbitrary input paths.
  function pairMetricFromUrl() {
    const requested = new URLSearchParams(window.location.search).get("pair_metric");
    return [...pairMetric.options].some(option=>option.value===requested)
      ? requested : "fantlab.dialogue.share_percent";
  }
  // An allow-listed measured edition is a UI key, never a network path.
  // Invalid, missing, pending and duplicate URL pairs resolve to honest defaults.
  function pairFromUrl() {
    const params = new URLSearchParams(window.location.search);
    const left = params.get("left"), right = params.get("right");
    return getBook(left) && getBook(right) && left !== right ?
      [left, right] : ["anna", "karamazov"];
  }
  function selectPair(left, right, addHistory=false) {
    if (!getBook(left) || !getBook(right)) return;
    leftSelect.value = left;
    rightSelect.value = right;
    pairSwapButton.disabled = left === right;
    updatePair();
    const share = el("share-pair");
    if (left === right) {
      share.hidden = true;
      share.removeAttribute("href");
      return;
    }
    share.hidden = false;
    share.href = "?left=" + encodeURIComponent(left) +
                 "&right=" + encodeURIComponent(right) +
                 "&pair_metric=" + encodeURIComponent(pairMetric.value) + "#pairs";
    share.textContent = "Прямая ссылка: «" + getBook(left).display_title +
                        "» и «" + getBook(right).display_title + "» ↗";
    if (addHistory) {
      const url = new URL(window.location.href);
      url.searchParams.set("left", left);
      url.searchParams.set("right", right);
      url.searchParams.set("pair_metric", pairMetric.value);
      url.hash = "pairs";
      window.history.pushState(null, "", url);
    }
  }

  function swapPair() {
    // Keep signed deltas, provenance, chart and permalink in the canonical renderer.
    if (pairSwapButton.disabled || leftSelect.value === rightSelect.value) return;
    selectPair(rightSelect.value, leftSelect.value, true);
  }

  function exportSelected() {
    const book=getBook(currentBook);
    if (!book) return;
    const result={
      schema:"scriptorium-ru-derived-export-v1",
      scientific_claim:"DIAGNOSTIC_ONLY",
      fantlab_input_identity:"UNKNOWN",m2_source_matched:0,
      candidate_id:book.candidate_id,
      original_language:book.original_language,analysis_language:book.language,
      edition_id:book.edition_id,translator:book.translator,
      source_sha256:book.source_sha256,
      source_evidence_url:book.evidence_url,
      measurement_profiles:book.profiles,
      metrics:book.metrics
    };
    const blob=new Blob([JSON.stringify(result,null,2)+"\n"],{type:"application/json"});
    const url=URL.createObjectURL(blob);
    const link=document.createElement("a");
    link.href=url;link.download="scriptorium-"+book.key+"-derived.json";
    document.body.appendChild(link);link.click();link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  // Human-readable one-edition report. Never serialize book prose or promote
  // unmatched FantLab display numbers to a passed benchmark.
  function serializeBookMarkdown(book) {
    const required=["key","candidate_id","display_title","display_author","edition_id","evidence_url"];
    const profileKeys=["normalization","metrics","dialogue","vocabulary","punctuation"];
    if (!book || book.text_status!=="measured" || book.language!=="ru" ||
        !["ru","fr","en"].includes(book.original_language) ||
        !required.every(k=>typeof book[k]==="string" && book[k].trim()) ||
        !/^[a-f0-9]{64}$/.test(book.source_sha256||"") ||
        !/^https:\/\/github.com\/drevendev\/Scriptorium\/blob\/master\//.test(book.evidence_url) ||
        (book.original_language!=="ru" &&
          (!book.translator?.id || !book.translator?.name)) ||
        !profileKeys.every(k=>typeof book.profiles?.[k]==="string" && book.profiles[k]) ||
        !Number.isInteger(book.measured) || !Number.isInteger(book.unavailable) ||
        !Array.isArray(book.metrics) || !book.metrics.length ||
        book.metrics.length!==book.measured+book.unavailable) {
      throw Error("Неполный проверенный источник Markdown-отчёта");
    }
    const seen=new Set();
    let measured=0;
    const rows=book.metrics.map(m=>{
      if (!m || typeof m.id!=="string" || seen.has(m.id) ||
          !/^(fantlab|scriptorium)\.[a-z0-9_.]+$/.test(m.id) ||
          !(m.actual===null || isNumeric(m.actual)) ||
          !(m.reference===null || isNumeric(m.reference)) ||
          !["measured","not_run","unavailable"].includes(m.status) ||
          (m.actual!==null)!==(m.status==="measured") ||
          !["candidate","extension"].includes(m.kind) ||
          (m.kind==="extension" && m.reference!==null)) {
        throw Error("Непроверенное значение Markdown-отчёта");
      }
      seen.add(m.id);
      if (m.actual!==null) measured++;
      const fields=[
        label(m.id),m.id,m.actual===null?m.status.toUpperCase():String(m.actual),
        m.kind==="extension"?"N/A":m.reference===null?"UNKNOWN":String(m.reference),
        diagnosticDelta(m),unit(m.id),
        m.kind==="extension"?"EXTENSION_ONLY":"DIAGNOSTIC_UNMATCHED_SOURCE"
      ];
      return "| "+fields.map(markdownCell).join(" | ")+" |";
    });
    if (measured!==book.measured) throw Error("Подмена числа измерений Markdown-отчёта");
    const metadata=[
      ["Название",book.display_title],["Автор",book.display_author],
      ["Кандидат (ID)",book.candidate_id],["Редакция (ID)",book.edition_id],
      ["Язык оригинала",book.original_language],["Язык анализа",book.language],
      ["Переводчик",book.translator?.name||"не применимо"],
      ["Переводчик (ID)",book.translator?.id||"не применимо"],
      ["SHA-256 источника",book.source_sha256],
      ["Свидетельство анализа",book.evidence_url],
      ["Референс FantLab",book.fantlab_url||"UNKNOWN"]
    ].map(([name,value])=>"| "+[name,value].map(markdownCell).join(" | ")+" |");
    const profiles=profileKeys.map(key=>"| "+[key,book.profiles[key]]
      .map(markdownCell).join(" | ")+" |");
    return [
      "# Scriptorium · измерения русскоязычной редакции","",
      "**DIAGNOSTIC_ONLY** · вход FantLab: **UNKNOWN** · **M2: 0/5**.",
      "Это производные результаты, не подтверждённое совпадение с FantLab.",
      "Δ S−F — диагностическая разница Scriptorium минус опубликованное значение FantLab",
      "для неустановленного соответствия редакций; для процентов — в процентных пунктах.",
      "Неизвестное значение и NOT_RUN — не ноль. Литературный текст не включён.","",
      "## Редакция и происхождение","","| Поле | Значение |","| --- | --- |",
      ...metadata,"",
      "## Профили измерений","","| Профиль | Версия |","| --- | --- |",
      ...profiles,"",
      "## Полный реестр измерений","",
      book.metrics.length+" полей: "+book.measured+" измерено; "+
        book.unavailable+" недоступно. N/A — расширение Scriptorium.","",
      "| Метрика | ID | Scriptorium | FantLab | Δ S−F | Единица | Статус |",
      "| --- | --- | ---: | ---: | ---: | --- | --- |",...rows,""
    ].join("\n");
  }
  function exportSelectedMarkdown() {
    verify(data);
    const book=getBook(currentBook);
    if (!book) { singleMarkdownButton.disabled=true; return; }
    const report=serializeBookMarkdown(book);
    const blob=new Blob([report],{type:"text/markdown;charset=utf-8"});
    const url=URL.createObjectURL(blob);
    const link=document.createElement("a");
    link.href=url;
    link.download="scriptorium-"+book.key+"-derived.md";
    document.body.appendChild(link);link.click();link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  // Print the selected metric's exact, source-backed table, even when collapsed.
  // Restore the user's disclosure state after the browser closes print preview.
  const chartPrintTable = document.querySelector(".chart-table");
  let chartPrintWasOpen = null;
  function openChartTableForPrint() {
    if (!chartPrintTable) return;
    if (chartPrintWasOpen === null) chartPrintWasOpen = chartPrintTable.open;
    chartPrintTable.open = true;
  }
  function restoreChartTableAfterPrint() {
    if (!chartPrintTable || chartPrintWasOpen === null) return;
    chartPrintTable.open = chartPrintWasOpen;
    chartPrintWasOpen = null;
  }
  window.addEventListener("beforeprint", openChartTableForPrint);
  window.addEventListener("afterprint", restoreChartTableAfterPrint);

  async function initialize() {
    try {
      const res=await fetch(file,{cache:"no-store",credentials:"omit"});
      if (!res.ok) throw Error("HTTP "+res.status);
      const incoming=await res.json();
      verify(incoming); data=incoming;
      const inputs=[catalogFilter,catalogSearch,catalogReset,one,search,out,singleMarkdownButton,leftSelect,rightSelect,pairSwapButton,pairMetric,pairExportButton,pairCsvButton,pairMarkdownButton,libraryCsvButton,chartSortButton,chartCsvButton,...chartButtons];
      for(const input of inputs)input.disabled=false;
      for(const btn of chartButtons) {
        btn.addEventListener("click",()=>selectChart(btn.dataset.chart,true));
      }
      chartSortButton.addEventListener("click",()=>{sortChart=!sortChart;selectChart(currentChart,true);});
      chartCsvButton.addEventListener("click",exportChartCsv);
      for(const anchor of bookLinks) {
        anchor.addEventListener("click",event=>{
          // Modified click still opens the source JSON, even without site JS.
          if (event.defaultPrevented || event.button !== 0 ||
              event.ctrlKey || event.metaKey || event.shiftKey || event.altKey ||
              !getBook(anchor.dataset.book)) return;
          event.preventDefault();
          selectBook(anchor.dataset.book,true,true);
        });
      }
      catalogFilter.addEventListener("change",updateCatalog);
      catalogSearch.addEventListener("input",updateCatalog);
      catalogReset.addEventListener("click",resetCatalog);
      restoreCatalogFromUrl();
      el("catalog-tools").hidden=false;
      one.addEventListener("change",()=>selectBook(one.value,true));
      window.addEventListener("popstate",()=>{
        restoreCatalogFromUrl();
        restoreChartFromUrl();
        selectBook(bookFromUrl());
        const [left,right] = pairFromUrl();
        pairMetric.value=pairMetricFromUrl();
        selectPair(left,right);
      });
      search.addEventListener("input",updateSingle);
      out.addEventListener("click",exportSelected);
      singleMarkdownButton.addEventListener("click",exportSelectedMarkdown);
      pairExportButton.addEventListener("click",exportPair);
      pairCsvButton.addEventListener("click",exportPairCsv);
      pairMarkdownButton.addEventListener("click",exportPairMarkdown);
       libraryCsvButton.addEventListener("click",exportLibraryCsv);
      leftSelect.addEventListener("change",()=>selectPair(leftSelect.value,rightSelect.value,true));
      rightSelect.addEventListener("change",()=>selectPair(leftSelect.value,rightSelect.value,true));
      pairMetric.addEventListener("change",()=>selectPair(leftSelect.value,rightSelect.value,true));
      pairSwapButton.addEventListener("click",swapPair);
      restoreChartFromUrl();
      const [left,right] = pairFromUrl();
      pairMetric.value=pairMetricFromUrl();
      selectPair(left,right);
      selectBook(bookFromUrl());
    } catch (_) {
      status.textContent="Интерактивные данные недоступны. Откройте источник через ссылку на карточке книги; никаких выдуманных значений не подставлено.";
      el("pair-status").textContent="Сравнение недоступно без проверенного JSON. Статическая таблица остаётся для чтения.";
      // Static fallback charts and tables remain visible.
    }
  }
  initialize();
})();
