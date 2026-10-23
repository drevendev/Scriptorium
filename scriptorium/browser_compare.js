/* Scriptorium Reader: browser-only comparison of canonical local-analysis JSON.
 * Canonical metadata is compiled from the Python analyzer at build time.
 * No manuscript text, uploads, requests, telemetry or persistent browser storage.
 */
(function (global) {
  'use strict';
  const CONTRACT = /*SCRIPTORIUM_METRIC_CONTRACT*/ null;
  const REPORT_LIMIT = 8 * 1024 * 1024;
  const SOURCE_LIMIT = 32 * 1024 * 1024;
  const CALIBRATION_FLOOR = 300000;
  const COMPARISON_SCHEMA = 'scriptorium-private-comparison-v1';
  const DICTIONARY_IDS = new Set([
    'fantlab.vocabulary.active_dictionary',
    'fantlab.vocabulary.active_nondictionary',
    'fantlab.vocabulary.uasz_3000',
    'fantlab.vocabulary.uasz_10000',
    'fantlab.vocabulary.uasz_100000'
  ]);
  const REQUIRED_COUNTS = [
    'fantlab.general.words', 'scriptorium.general.sentences',
    'fantlab.vocabulary.unique_words'
  ];
  const has = (v, k) => Object.prototype.hasOwnProperty.call(v, k);
  function fail(message) { throw new Error(message); }

  /* Each JSON numeric token survives parsing without binary64 rounding. This also
   * distinguishes integer tokens (3) from float tokens (3.0, 3e0). */
  class NumberToken {
    constructor(lexeme) {
      this.lexeme = lexeme;
      this.integer = !/[.eE]/.test(lexeme);
      if (this.integer && lexeme.length > 16) fail('Integer literal exceeds bounds');
      if (!this.integer && lexeme.length > 72) fail('Decimal literal exceeds bounds');
      const match = /^(-?)([0-9]+)(?:\.([0-9]+))?(?:[eE]([+-]?[0-9]+))?$/.exec(lexeme);
      if (!match) fail('Invalid numeric literal');
      const fractional = match[3] || '';
      const declaredExponent = match[4] ? Number(match[4]) : 0;
      if (!Number.isSafeInteger(declaredExponent)) fail('Decimal exponent exceeds bounds');
      this.exponent = declaredExponent - fractional.length;
      if (!this.integer && Math.abs(this.exponent) > 40) fail('Decimal exponent exceeds bounds');
      this.negative = match[1] === '-';
      this.digits = (match[2] + fractional).replace(/^0+(?=.)/, '');
      this.coefficient = BigInt(this.digits) * (this.negative ? -1n : 1n);
      // Preserve the sign of a JSON decimal negative zero: Python Decimal('-0.0')
      // serializes that observed value as '-0.0', even though it compares equal to zero.
      this.adjusted = this.exponent + this.digits.length - 1;
    }
  }

  function parseStrictJSON(source) {
    if (typeof source !== 'string' || new TextEncoder().encode(source).length > REPORT_LIMIT) {
      fail('Report exceeds the 8 MiB UTF-8 limit');
    }
    let i = 0;
    let nodes = 0;
    function whitespace() { while (/[\x20\t\n\r]/.test(source[i] || '\uFFFF')) i++; }
    function string() {
      const start = i++;
      let done = false;
      while (i < source.length) {
        const c = source.charCodeAt(i);
        if (c === 34) { i++; done = true; break; }
        if (c < 32) fail('Invalid JSON string');
        if (c === 92) {
          i++;
          const escaped = source[i];
          if (escaped === 'u') {
            if (!/^[0-9a-fA-F]{4}$/.test(source.slice(i + 1, i + 5))) fail('Invalid JSON escape');
            i += 5;
          } else if ('"\\/bfnrt'.includes(escaped || '\uFFFF')) i++;
          else fail('Invalid JSON escape');
          continue;
        }
        i++;
      }
      if (!done) fail('Unterminated JSON string');
      return JSON.parse(source.slice(start, i));
    }
    function value(depth) {
      if (depth > 48 || ++nodes > 50000) fail('JSON nesting exceeds bounds');
      whitespace();
      const c = source[i];
      if (c === '"') return string();
      if (c === '{') {
        i++;
        const out = Object.create(null);
        whitespace();
        if (source[i] === '}') { i++; return out; }
        for (;;) {
          whitespace();
          if (source[i] !== '"') fail('Invalid JSON object');
          const key = string();
          if (has(out, key)) fail('Duplicate JSON object key');
          whitespace();
          if (source[i++] !== ':') fail('Invalid JSON object');
          out[key] = value(depth + 1);
          whitespace();
          const end = source[i++];
          if (end === '}') return out;
          if (end !== ',') fail('Invalid JSON object');
        }
      }
      if (c === '[') {
        i++;
        const out = [];
        whitespace();
        if (source[i] === ']') { i++; return out; }
        for (;;) {
          out.push(value(depth + 1));
          whitespace();
          const end = source[i++];
          if (end === ']') return out;
          if (end !== ',') fail('Invalid JSON array');
        }
      }
      if (c === '-' || (c >= '0' && c <= '9')) {
        const match = /^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/.exec(source.slice(i));
        if (!match) fail('Invalid JSON number');
        i += match[0].length;
        return new NumberToken(match[0]);
      }
      for (const [literal, parsed] of [['true', true], ['false', false], ['null', null]]) {
        if (source.startsWith(literal, i)) { i += literal.length; return parsed; }
      }
      fail('Invalid JSON value');
    }
    const result = value(0);
    whitespace();
    if (i !== source.length) fail('Trailing JSON data');
    return result;
  }

  function object(value, fields, label) {
    if (value === null || typeof value !== 'object' || Array.isArray(value) || value instanceof NumberToken ||
        Object.keys(value).length !== fields.length || !fields.every(key => has(value, key))) {
      fail('Invalid ' + label + ' contract');
    }
    return value;
  }
  function text(value, label, limit = 160) {
    if (typeof value !== 'string' || !value.trim() || value.length > limit) fail('Invalid ' + label + ' identity');
    return value;
  }
  function digest(value, label) {
    if (typeof value !== 'string' || !/^[a-f0-9]{64}$/.test(value)) fail('Invalid ' + label + ' digest');
    return value;
  }
  function integer(value, label, limit = 1000000000) {
    if (!(value instanceof NumberToken) || !value.integer ||
        value.coefficient < 0n || value.coefficient > BigInt(limit)) fail('Invalid ' + label + ' count');
    return Number(value.coefficient);
  }
  function decimal(value, label) {
    if (value === null) return null;
    if (!(value instanceof NumberToken) || value.coefficient < 0n ||
        value.adjusted > 12 || value.adjusted < -40) fail('Invalid ' + label + ' numeric domain');
    if (value.integer) integer(value, label);
    return value;
  }
  function decimalString(value) {
    if (value === null) return null;
    const negative = value.coefficient < 0n || (value.negative && !value.integer);
    const digits = (value.coefficient < 0n ? -value.coefficient : value.coefficient).toString();
    const exp = value.exponent;
    const adjusted = digits.length - 1 + exp;
    let answer;
    if (exp <= 0 && adjusted >= -6) {
      const point = digits.length + exp;
      answer = point > 0 ? digits.slice(0, point) + (exp < 0 ? '.' + digits.slice(point) : '')
        : '0.' + '0'.repeat(-point) + digits;
    } else {
      const mantissa = digits.length === 1 ? digits : digits[0] + '.' + digits.slice(1);
      answer = mantissa + 'E' + (adjusted >= 0 ? '+' : '') + adjusted;
    }
    return (negative ? '-' : '') + answer;
  }
  function compareNumbers(a, b) {
    if (a === null || b === null) fail('Incomparable decimal values');
    const exp = Math.min(a.exponent, b.exponent);
    const first = a.coefficient * 10n ** BigInt(a.exponent - exp);
    const second = b.coefficient * 10n ** BigInt(b.exponent - exp);
    return first < second ? -1 : first > second ? 1 : 0;
  }
  function exactDifference(a, b) {
    const exp = Math.min(a.exponent, b.exponent);
    const coefficient = b.coefficient * 10n ** BigInt(b.exponent - exp) -
      a.coefficient * 10n ** BigInt(a.exponent - exp);
    return decimalString({coefficient, exponent: exp});
  }
  function sameNumber(a, b) {
    return a === null || b === null ? a === b : compareNumbers(a, b) === 0;
  }
  function plainInteger(value, label, limit) { return integer(value, label, limit); }
  function validReport(report) {
    const snapshot = CONTRACT;
    const doc = object(report, ['schema_version', 'metric_contract_id', 'source', 'analyzer',
      'representativeness', 'metrics'], 'top-level');
    if (doc.schema_version !== 'scriptorium-local-analysis-v1' ||
        doc.metric_contract_id !== snapshot.metric_contract_id) fail('Unsupported local analysis contract');
    const source = object(doc.source, ['raw_sha256', 'byte_count', 'normalized_sha256',
      'normalized_character_count', 'source_text_embedded'], 'source');
    if (source.source_text_embedded !== false) fail('Source text must not be embedded');
    digest(source.raw_sha256, 'raw');
    digest(source.normalized_sha256, 'normalized');
    const bytes = integer(source.byte_count, 'source bytes', SOURCE_LIMIT);
    const length = integer(source.normalized_character_count, 'normalized characters', SOURCE_LIMIT);
    if (length > bytes) fail('Inconsistent source size');
    const analyzer = object(doc.analyzer, ['scriptorium_revision', 'profiles', 'dependencies'], 'analyzer');
    if (analyzer.scriptorium_revision !== null) text(analyzer.scriptorium_revision, 'revision');
    const profiles = object(analyzer.profiles, Object.keys(snapshot.profiles), 'profiles');
    for (const key of Object.keys(profiles)) text(profiles[key], key + ' profile');
    const dependencies = object(analyzer.dependencies, ['vocabulary_dictionary'], 'dependencies');
    let dictionary = dependencies.vocabulary_dictionary;
    if (dictionary !== null) {
      dictionary = object(dictionary, ['profile', 'normalized_lexemes_sha256', 'lexeme_count'], 'dictionary');
      text(dictionary.profile, 'dictionary profile');
      digest(dictionary.normalized_lexemes_sha256, 'dictionary');
      integer(dictionary.lexeme_count, 'dictionary lexemes');
    }
    const representative = object(doc.representativeness,
      ['calibration_threshold_characters', 'meets_calibration_threshold', 'note'], 'representativeness');
    if (integer(representative.calibration_threshold_characters, 'calibration floor') !== CALIBRATION_FLOOR ||
        typeof representative.meets_calibration_threshold !== 'boolean' ||
        representative.meets_calibration_threshold !== (length >= CALIBRATION_FLOOR)) {
      fail('Invalid representativeness status');
    }
    text(representative.note, 'representativeness note', 1000);
    const metrics = object(doc.metrics, Object.keys(snapshot.metrics), '29 metrics');
    for (const [id, standard] of Object.entries(snapshot.metrics)) {
      const row = object(metrics[id], Object.keys(standard.row), 'metric row');
      for (const field of ['unit', 'compatibility_status', 'definition_evidence']) {
        if (row[field] !== standard.row[field]) fail('Metric evidence or unit contract mismatch');
      }
      const number = decimal(row.value, id);
      if (number !== null) {
        if (standard.row.unit === 'percent' && compareNumbers(number, new NumberToken('100')) > 0) {
          fail('Invalid percent domain');
        }
        if (['characters', 'words', 'sentences'].includes(standard.row.unit) && !number.integer) {
          fail('Count must be an exact JSON integer');
        }
      }
      if (has(row, 'raw_count')) integer(row.raw_count, 'punctuation raw count');
    }
    const rows = doc.metrics;
    if (integer(rows['fantlab.general.characters'].value, 'characters') !== length) {
      fail('Character metric contradicts source identity');
    }
    for (const id of REQUIRED_COUNTS) integer(rows[id].value, id);
    const words = integer(rows['fantlab.general.words'].value, 'words');
    const sentences = integer(rows['scriptorium.general.sentences'].value, 'sentences');
    const unique = integer(rows['fantlab.vocabulary.unique_words'].value, 'unique words');
    if (words > length || unique > words || sentences > length) fail('Inconsistent word/sentence statistics');
    for (const [id, denominator] of [
      ['fantlab.general.mean_word_length_chars', words],
      ['fantlab.general.mean_sentence_length_chars', sentences]
    ]) {
      const mean = decimal(rows[id].value, id);
      if (denominator === 0 ? mean !== null :
          (mean === null || compareNumbers(mean, new NumberToken('1')) < 0 ||
           compareNumbers({coefficient: mean.coefficient * BigInt(denominator), exponent: mean.exponent},
             new NumberToken(String(length + 1))) > 0)) fail('Mean contradicts source budget');
    }
    for (const [id, row] of Object.entries(rows)) {
      if (!id.startsWith('fantlab.punctuation.')) continue;
      const count = integer(row.raw_count, 'punctuation count');
      if (count > length) fail('Punctuation count exceeds characters');
      const rate = decimal(row.value, id);
      // Python metrics._per_1000 uses binary64 arithmetic. Its shortest
      // round-trip decimal spelling has the same exact value as JS Number.toString.
      const expected = words === 0 ? null : new NumberToken(String(count * 1000.0 / words));
      if (!sameNumber(rate, expected)) fail('Punctuation rate contradicts raw count');
    }
    if (dictionary === null) {
      if ([...DICTIONARY_IDS].some(id => rows[id].value !== null)) fail('Dictionary value without dependency');
    } else {
      const active = integer(rows['fantlab.vocabulary.active_dictionary'].value, 'dictionary words');
      const inactive = integer(rows['fantlab.vocabulary.active_nondictionary'].value, 'out-of-dictionary words');
      const lexemes = integer(dictionary.lexeme_count, 'dictionary lexemes');
      if (active > lexemes || active + inactive !== unique) fail('Dictionary partition mismatch');
      for (const windowSize of [3000, 10000, 100000]) {
        const measured = decimal(rows['fantlab.vocabulary.uasz_' + windowSize].value, 'dictionary window');
        if ((measured === null) !== (words < windowSize) ||
            (measured !== null && compareNumbers(measured, new NumberToken(String(Math.min(windowSize, lexemes)))) > 0)) {
          fail('Dictionary window contradicts counts');
        }
      }
    }
    return doc;
  }
  function canonicalMetadata(report) {
    const source = report.source;
    const analyzer = report.analyzer;
    const dict = analyzer.dependencies.vocabulary_dictionary;
    const profiles = Object.create(null);
    for (const [key, value] of Object.entries(analyzer.profiles)) profiles[key] = value;
    return {
      raw_sha256: source.raw_sha256,
      normalized_sha256: source.normalized_sha256,
      bytes: integer(source.byte_count, 'bytes'),
      normalized_characters: integer(source.normalized_character_count, 'characters'),
      meets_calibration_threshold: report.representativeness.meets_calibration_threshold,
      scriptorium_revision: analyzer.scriptorium_revision,
      profiles,
      dictionary: dict === null ? null : {
        profile: dict.profile,
        normalized_lexemes_sha256: dict.normalized_lexemes_sha256,
        lexeme_count: integer(dict.lexeme_count, 'dictionary lexemes')
      }
    };
  }
  function equalJSON(left, right) {
    if (left instanceof NumberToken && right instanceof NumberToken) return compareNumbers(left, right) === 0;
    if (left === null || right === null || typeof left !== 'object' || typeof right !== 'object') return left === right;
    if (Array.isArray(left) || Array.isArray(right)) return Array.isArray(left) && Array.isArray(right) &&
      left.length === right.length && left.every((v, i) => equalJSON(v, right[i]));
    const keys = Object.keys(left);
    return keys.length === Object.keys(right).length && keys.every(key => has(right, key) && equalJSON(left[key], right[key]));
  }
  function crossIdentity(left, right) {
    const la = left.source;
    const ra = right.source;
    const le = left.analyzer;
    const re = right.analyzer;
    const sameRaw = la.raw_sha256 === ra.raw_sha256;
    const sameNormalized = la.normalized_sha256 === ra.normalized_sha256;
    if (sameRaw && integer(la.byte_count, 'bytes') !== integer(ra.byte_count, 'bytes')) {
      fail('Same raw digest has inconsistent sizes');
    }
    if (sameRaw && le.profiles.normalization === re.profiles.normalization && !sameNormalized) {
      fail('Same raw digest has different normalized digest');
    }
    if (sameNormalized && integer(la.normalized_character_count, 'characters') !==
        integer(ra.normalized_character_count, 'characters')) fail('Same normalized digest has inconsistent lengths');
    if (sameNormalized && equalJSON(le.profiles, re.profiles)) {
      const dictionariesEqual = equalJSON(le.dependencies, re.dependencies);
      for (const id of Object.keys(CONTRACT.metrics)) {
        if (DICTIONARY_IDS.has(id) && !dictionariesEqual) continue;
        const a = left.metrics[id];
        const b = right.metrics[id];
        if (!sameNumber(a.value, b.value) || (has(a, 'raw_count') &&
            integer(a.raw_count, 'raw') !== integer(b.raw_count, 'raw'))) {
          fail('Same normalized input and method have contradictory measurements');
        }
      }
    }
  }
  function compareReports(left, right) {
    validReport(left);
    validReport(right);
    crossIdentity(left, right);
    const profilesEqual = equalJSON(left.analyzer.profiles, right.analyzer.profiles);
    const dictionariesEqual = equalJSON(left.analyzer.dependencies, right.analyzer.dependencies);
    const rows = Object.keys(CONTRACT.metrics).sort().map(id => {
      const standard = CONTRACT.metrics[id];
      const a = decimal(left.metrics[id].value, id);
      const b = decimal(right.metrics[id].value, id);
      let status = 'comparable';
      let reason = 'Both derived values use the same declared method';
      if (!profilesEqual) { status = 'incomparable'; reason = 'Algorithm profiles differ'; }
      else if (DICTIONARY_IDS.has(id) && !dictionariesEqual) {
        status = 'incomparable'; reason = 'Dictionary identities differ';
      } else if (a === null || b === null) {
        status = 'unavailable'; reason = 'At least one measurement is not run or undefined';
      }
      const unit = standard.row.unit;
      return {
        metric_id: id, label: standard.label, unit,
        definition_evidence: standard.row.definition_evidence,
        compatibility_status: standard.row.compatibility_status,
        left: decimalString(a), right: decimalString(b),
        difference: status === 'comparable' ? exactDifference(a, b) : null,
        difference_unit: status === 'comparable' ? (unit === 'percent' ? 'percentage_points' : unit) : null,
        comparison_status: status, reason
      };
    });
    return {
      schema_version: COMPARISON_SCHEMA,
      metric_contract_id: left.metric_contract_id,
      direction: 'right_minus_left',
      scientific_boundary: 'Inferred/extension local measurements only; not verified FantLab parity (M2 0/5).',
      left_source: canonicalMetadata(left), right_source: canonicalMetadata(right), metrics: rows
    };
  }
  function csvText(value) {
    if (!value) return value;
    if (/^[\t\r\n\u0000]/.test(value)) return "'" + value;
    const first = value.replace(/^[\s\p{Cf}]+/u, '')[0] || '';
    return /^[=+\-@＝＋－＠]$/.test(first) ? "'" + value : value;
  }
  function csvCell(value) {
    if (/[",\r\n]/.test(value)) return '"' + value.replace(/"/g, '""') + '"';
    return value;
  }
  function renderCSV(comparison) {
    const fields = ['metric_id', 'label', 'unit', 'compatibility_status', 'definition_evidence',
      'left', 'right', 'difference', 'difference_unit', 'comparison_status', 'reason',
      'left_sha256', 'right_sha256'];
    const lines = [fields.join(',')];
    for (const row of comparison.metrics) {
      const values = fields.slice(0, 11).map(key => row[key]);
      values.push(comparison.left_source.raw_sha256, comparison.right_source.raw_sha256);
      lines.push(values.map((value, index) => {
        const raw = value === null || value === undefined ? '' : String(value);
        return csvCell(index >= 5 && index <= 7 ? raw : csvText(raw));
      }).join(','));
    }
    return lines.join('\n') + '\n';
  }
  function sortedKeys(value) {
    if (Array.isArray(value)) return value.map(sortedKeys);
    if (value && typeof value === 'object') {
      const sorted = {};
      for (const key of Object.keys(value).sort()) sorted[key] = sortedKeys(value[key]);
      return sorted;
    }
    return value;
  }
  function renderJSON(comparison) { return JSON.stringify(sortedKeys(comparison), null, 2) + '\n'; }

  function browserReady() {
    const left = document.getElementById('report-left');
    const right = document.getElementById('report-right');
    const compareButton = document.getElementById('run-comparison');
    const status = document.getElementById('comparison-message');
    const result = document.getElementById('comparison-result');
    const tbody = document.getElementById('comparison-rows');
    const sourceInfo = document.getElementById('source-summary');
    const saveJSON = document.getElementById('save-comparison-json');
    const saveCSV = document.getElementById('save-comparison-csv');
    if (![left, right, compareButton, status, result, tbody, sourceInfo, saveJSON, saveCSV].every(Boolean)) return;
    let generation = 0;
    let current = null;
    function invalidate() {
      generation++;
      current = null;
      result.hidden = true;
      saveJSON.disabled = true;
      saveCSV.disabled = true;
      compareButton.disabled = !(left.files.length && right.files.length);
      status.textContent = 'Choose two Reader analysis JSON files. Nothing is sent to a server.';
    }
    left.addEventListener('change', invalidate);
    right.addEventListener('change', invalidate);
    async function load(file) {
      if (file.size > REPORT_LIMIT) fail('One report exceeds the 8 MiB limit');
      const buffer = await file.arrayBuffer();
      if (buffer.byteLength > REPORT_LIMIT) fail('One report exceeds the 8 MiB limit');
      const raw = new TextDecoder('utf-8', {fatal: true}).decode(buffer);
      return parseStrictJSON(raw);
    }
    compareButton.addEventListener('click', async () => {
      const token = ++generation;
      current = null;
      result.hidden = true;
      saveJSON.disabled = true;
      saveCSV.disabled = true;
      compareButton.disabled = true;
      status.textContent = 'Validating both private reports…';
      try {
        const [a, b] = await Promise.all([load(left.files[0]), load(right.files[0])]);
        if (token !== generation) return;
        const value = compareReports(a, b);
        const fragment = document.createDocumentFragment();
        for (const row of value.metrics) {
          const tr = document.createElement('tr');
          const heading = document.createElement('th');
          heading.scope = 'row';
          heading.textContent = row.label + ' (' + row.metric_id + ')';
          tr.appendChild(heading);
          for (const field of ['left', 'right', 'unit', 'difference', 'difference_unit', 'comparison_status']) {
            const cell = document.createElement('td');
            cell.textContent = row[field] === null ? 'Not available' : row[field];
            tr.appendChild(cell);
          }
          const why = document.createElement('td');
          why.textContent = row.reason;
          tr.appendChild(why);
          fragment.appendChild(tr);
        }
        tbody.replaceChildren(fragment);
        sourceInfo.textContent = 'Left normalized characters: ' + value.left_source.normalized_characters +
          ' · SHA-256: ' + value.left_source.raw_sha256 + '\nRight normalized characters: ' +
          value.right_source.normalized_characters + ' · SHA-256: ' + value.right_source.raw_sha256;
        current = value;
        result.hidden = false;
        saveJSON.disabled = false;
        saveCSV.disabled = false;
        status.textContent = '29 measurements validated. Difference: right minus left; percent changes in percentage points.';
      } catch (_error) {
        if (token !== generation) return;
        status.textContent = 'Comparison rejected: invalid, inconsistent or unsupported analysis JSON. ' +
          'Check the reports using the installed Reader CLI; filenames and private contents are not shown.';
      } finally {
        if (token === generation) compareButton.disabled = !(left.files.length && right.files.length);
      }
    });
    function download(content, name, type) {
      const blob = new Blob([content], {type});
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement('a');
      anchor.href = url;
      anchor.download = name;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    }
    saveJSON.addEventListener('click', () => { if (current) download(renderJSON(current), 'scriptorium-comparison.json', 'application/json'); });
    saveCSV.addEventListener('click', () => { if (current) download(renderCSV(current), 'scriptorium-comparison.csv', 'text/csv;charset=utf-8'); });
    invalidate();
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {NumberToken, parseStrictJSON, validReport, compareReports, renderJSON, renderCSV, exactDifference};
  }
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', browserReady, {once: true});
    else browserReady();
  }
})(typeof globalThis === 'object' ? globalThis : this);