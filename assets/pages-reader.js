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
  const bookLinks = [...document.querySelectorAll("[data-book]")];
  const one = el("choose-book");
  const search = el("search-metric");
  const status = el("table-status");
  const body = el("measurement-rows");
  const out = el("export-button");
  const leftSelect = el("pair-left");
  const rightSelect = el("pair-right");
  const pairMetric = el("pair-metric");
  let data;
  let currentBook = "anna";
  let currentChart = "fantlab.dialogue.share_percent";

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
        doc.counts?.work_count !== 10 ||
        doc.counts?.measured_works !== 6 ||
        doc.counts?.awaiting_measurement !== 4 ||
        doc.counts?.metrics_total !== 153 ||
        doc.counts?.numeric_total !== 129 ||
        doc.counts?.unavailable_total !== 24 ||
        doc.language_modules?.en?.state !== "planned_not_measured" ||
        doc.language_modules?.en?.measured_work_count !== 0 ||
        !Array.isArray(doc.books) || doc.books.length !== 10) {
      throw Error("Русский каталог или научный статус изменён");
    }
    const census = {anna:[28,23],waves:[27,23],silver:[29,24],
                    karamazov:[29,24],hyperboloid:[29,24],beketova:[11,11]};
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
    if (seen.size !== 10 || Object.keys(census).some(x=>!seen.has(x)) ||
        observed !== 129 || missing !== 24 ||
        doc.books.filter(b=>b.text_status === "measured").length !== 6 ||
        doc.books.filter(b=>b.translator).length !== 2) throw Error("Подмена итогов каталога");
    const measured = doc.books.filter(b=>b.text_status === "measured");
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
  function makeTableRow(m) {
    const tr=document.createElement("tr");
    const th=insertText(tr,"th",label(m.id));
    th.scope="row";
    insertText(th,"code",m.id);
    insertText(tr,"td",m.actual===null?m.status.toUpperCase():exact(m.actual));
    insertText(tr,"td",m.kind==="extension"?"N/A":exact(m.reference));
    insertText(tr,"td",unit(m.id));
    insertText(tr,"td",m.kind==="extension"?"Расширение Scriptorium":
               m.actual===null?m.status.toUpperCase():"Диагностика · несовпавший источник");
    return tr;
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
      td.colSpan=5; nodes.appendChild(row);
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

  function updateChart() {
    const conf=metrics[currentChart];
    if (!conf) throw Error("Показатель диаграммы не разрешён");
    const rows=data.books.filter(b=>b.text_status==="measured").map(b=>{
      const item=lookup(b,currentChart);
      if (!item||!isNumeric(item.actual)) throw Error("Нет числа для диаграммы");
      return {title:b.display_title,value:item.actual};
    });
    const high=Math.max(...rows.map(x=>x.value));
    const nodes=document.createDocumentFragment();
    for (const row of rows) {
      const container=document.createElement("div");container.className="chart-row";
      insertText(container,"span",row.title);
      const track=insertText(container,"div","");
      track.className="bar-track";track.setAttribute("aria-hidden","true");
      const inner=insertText(track,"span","");
      inner.style.width=(high>0?100*row.value/high:0).toFixed(2)+"%";
      insertText(container,"strong",pretty(row.value,conf[2])+(conf[1]==="%"?"%":""));
      nodes.appendChild(container);
    }
    el("chart-series").replaceChildren(nodes);
    el("chart-unit").textContent=conf[0]+" · "+conf[1]+" · подписи округлены до 2 знаков";
    for (const b of chartButtons) {
      b.setAttribute("aria-pressed",String(b.dataset.chart===currentChart));
    }
  }

  const pairedIds = [
    "fantlab.dialogue.share_percent",
    "fantlab.dialogue.author_text_inside_dialogue_percent",
    "fantlab.general.mean_sentence_length_chars",
    "fantlab.general.mean_word_length_chars",
    "fantlab.punctuation.comma.per_1000_words",
    "fantlab.punctuation.dash.per_1000_words",
    "fantlab.punctuation.question.per_1000_words"
  ];
  function updatePair() {
    const a=getBook(leftSelect.value),b=getBook(rightSelect.value);
    if (!a||!b) throw Error("Книга отсутствует в измеренном корпусе");
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
    const rows=pairedIds.flatMap(id=>{
      const av=lookup(a,id),bv=lookup(b,id);
      return (av&&bv&&isNumeric(av.actual)&&isNumeric(bv.actual))?
        [{id,left:av.actual,right:bv.actual}]:[];
    });
    const fragment=document.createDocumentFragment();
    for (const m of rows) {
      const tr=document.createElement("tr");
      insertText(tr,"th",label(m.id)).scope="row";
      insertText(tr,"td",exact(m.left));
      insertText(tr,"td",exact(m.right));
      const d=m.right-m.left;
      insertText(tr,"td",(d>0?"+":"")+pretty(d,3));
      insertText(tr,"td",unit(m.id)+(unit(m.id)==="%"?" · Δ в п.п.":""));
      fragment.appendChild(tr);
    }
    el("pair-rows").replaceChildren(fragment);
    el("pair-caption").textContent=a.display_title+" → "+b.display_title+" · правая минус левая";
    el("pair-status").textContent=rows.length+" совместно измеренных нормированных метрик. "+
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
    updatePair();
    const share = el("share-pair");
    if (left === right) {
      share.hidden = true;
      share.removeAttribute("href");
      return;
    }
    share.hidden = false;
    share.href = "?left=" + encodeURIComponent(left) +
                 "&right=" + encodeURIComponent(right) + "#pairs";
    share.textContent = "Прямая ссылка: «" + getBook(left).display_title +
                        "» и «" + getBook(right).display_title + "» ↗";
    if (addHistory) {
      const url = new URL(window.location.href);
      url.searchParams.set("left", left);
      url.searchParams.set("right", right);
      url.hash = "pairs";
      window.history.pushState(null, "", url);
    }
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
  async function initialize() {
    try {
      const res=await fetch(file,{cache:"no-store",credentials:"omit"});
      if (!res.ok) throw Error("HTTP "+res.status);
      const incoming=await res.json();
      verify(incoming); data=incoming;
      const inputs=[one,search,out,leftSelect,rightSelect,pairMetric,...chartButtons];
      for(const input of inputs)input.disabled=false;
      for(const btn of chartButtons) {
        btn.addEventListener("click",()=>{currentChart=btn.dataset.chart;updateChart();});
      }
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
      one.addEventListener("change",()=>selectBook(one.value,true));
      window.addEventListener("popstate",()=>{
        selectBook(bookFromUrl());
        const [left,right] = pairFromUrl();
        selectPair(left,right);
      });
      search.addEventListener("input",updateSingle);
      out.addEventListener("click",exportSelected);
      leftSelect.addEventListener("change",()=>selectPair(leftSelect.value,rightSelect.value,true));
      rightSelect.addEventListener("change",()=>selectPair(leftSelect.value,rightSelect.value,true));
      pairMetric.addEventListener("change",updatePair);
      updateChart();
      const [left,right] = pairFromUrl();
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
