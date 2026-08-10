/* Minimal, self-contained QR Code generator (byte mode).
   Based on the public-domain algorithm by Kazuhiko Arase (qrcode-generator).
   Exposes window.QRCode.generate(text) -> { size, modules[r][c] (bool) }.
   Auto-selects version (1..40) for EC level M. */
(function (global) {
  'use strict';

  var EC_M = 0; // internal index used in tables below

  // ---- GF(256) math ----
  var EXP = new Array(256), LOG = new Array(256);
  (function () {
    for (var i = 0; i < 8; i++) EXP[i] = 1 << i;
    for (i = 8; i < 256; i++) EXP[i] = EXP[i - 4] ^ EXP[i - 5] ^ EXP[i - 6] ^ EXP[i - 8];
    for (i = 0; i < 255; i++) LOG[EXP[i]] = i;
  })();
  function gexp(n) { while (n < 0) n += 255; while (n >= 255) n -= 255; return EXP[n]; }
  function glog(n) { return LOG[n]; }

  // Polynomial as array of coefficients (highest degree first)
  function polyMul(a, b) {
    var r = new Array(a.length + b.length - 1);
    for (var i = 0; i < r.length; i++) r[i] = 0;
    for (i = 0; i < a.length; i++)
      for (var j = 0; j < b.length; j++)
        if (a[i] !== 0 && b[j] !== 0) r[i + j] ^= gexp(glog(a[i]) + glog(b[j]));
    return r;
  }
  function rsGenPoly(n) {
    var p = [1];
    for (var i = 0; i < n; i++) p = polyMul(p, [1, gexp(i)]);
    return p;
  }
  function rsEncode(data, ecCount) {
    var gen = rsGenPoly(ecCount);
    var res = data.concat(new Array(ecCount).fill(0));
    for (var i = 0; i < data.length; i++) {
      var coef = res[i];
      if (coef !== 0) {
        var lc = glog(coef);
        for (var j = 0; j < gen.length; j++) res[i + j] ^= gexp(glog(gen[j]) + lc);
      }
    }
    return res.slice(data.length);
  }

  // ---- EC block info for level M, versions 1..40 ----
  // Each entry: [ecPerBlock, [ [numBlocks, dataCodewordsPerBlock], ... ] ]
  var EC_TABLE_M = [
    [10, [[1, 16]]],
    [16, [[1, 28]]],
    [26, [[1, 44]]],
    [18, [[2, 32]]],
    [24, [[2, 43]]],
    [16, [[4, 27]]],
    [18, [[4, 31]]],
    [22, [[2, 38], [2, 39]]],
    [22, [[3, 36], [2, 37]]],
    [26, [[4, 43], [1, 44]]],
    [30, [[1, 50], [4, 51]]],
    [22, [[6, 36], [2, 37]]],
    [22, [[8, 37], [1, 38]]],
    [24, [[4, 40], [5, 41]]],
    [24, [[5, 41], [5, 42]]],
    [28, [[7, 45], [3, 46]]],
    [28, [[10, 46], [1, 47]]],
    [26, [[9, 43], [4, 44]]],
    [26, [[3, 44], [11, 45]]],
    [26, [[3, 41], [13, 42]]],
    [26, [[17, 42]]],
    [28, [[17, 46]]],
    [28, [[4, 47], [14, 48]]],
    [28, [[6, 45], [14, 46]]],
    [28, [[8, 47], [13, 48]]],
    [28, [[19, 46], [4, 47]]],
    [28, [[22, 45], [3, 46]]],
    [28, [[3, 45], [23, 46]]],
    [28, [[21, 45], [7, 46]]],
    [28, [[19, 47], [10, 48]]],
    [28, [[2, 46], [29, 47]]],
    [28, [[10, 46], [23, 47]]],
    [28, [[14, 46], [21, 47]]],
    [28, [[14, 46], [23, 47]]],
    [28, [[12, 47], [26, 48]]],
    [28, [[6, 47], [34, 48]]],
    [28, [[29, 46], [14, 47]]],
    [28, [[13, 46], [32, 47]]],
    [28, [[40, 47], [7, 48]]],
    [28, [[18, 47], [31, 48]]]
  ];

  function totalDataCodewords(ver) {
    var e = EC_TABLE_M[ver - 1], sum = 0;
    for (var i = 0; i < e[1].length; i++) sum += e[1][i][0] * e[1][i][1];
    return sum;
  }

  // ---- BCH / format & version info ----
  function bchDigit(data) { var d = 0; while (data !== 0) { d++; data >>>= 1; } return d; }
  var G15 = 0x537, G18 = 0x1f25, G15_MASK = 0x5412;
  function bchTypeInfo(data) {
    var d = data << 10;
    while (bchDigit(d) - bchDigit(G15) >= 0) d ^= (G15 << (bchDigit(d) - bchDigit(G15)));
    return ((data << 10) | d) ^ G15_MASK;
  }
  function bchTypeNumber(data) {
    var d = data << 12;
    while (bchDigit(d) - bchDigit(G18) >= 0) d ^= (G18 << (bchDigit(d) - bchDigit(G18)));
    return (data << 12) | d;
  }

  // ---- Alignment pattern positions ----
  var ALIGN = [
    [], [6, 18], [6, 22], [6, 26], [6, 30], [6, 34], [6, 22, 38], [6, 24, 42], [6, 26, 46],
    [6, 28, 50], [6, 30, 54], [6, 32, 58], [6, 34, 62], [6, 26, 46, 66], [6, 26, 48, 70],
    [6, 26, 50, 74], [6, 30, 54, 78], [6, 30, 56, 82], [6, 30, 58, 86], [6, 34, 62, 90],
    [6, 28, 50, 72, 94], [6, 26, 50, 74, 98], [6, 30, 54, 78, 102], [6, 28, 54, 80, 106],
    [6, 32, 58, 84, 110], [6, 30, 58, 86, 114], [6, 34, 62, 90, 118], [6, 26, 50, 74, 98, 122],
    [6, 30, 54, 78, 102, 126], [6, 26, 52, 78, 104, 130], [6, 30, 56, 82, 108, 134],
    [6, 34, 60, 86, 112, 138], [6, 30, 58, 86, 114, 142], [6, 34, 62, 90, 118, 146],
    [6, 30, 54, 78, 102, 126, 150], [6, 24, 50, 76, 102, 128, 154], [6, 28, 54, 80, 106, 132, 158],
    [6, 32, 58, 84, 110, 136, 162], [6, 26, 54, 82, 110, 138, 166], [6, 30, 58, 86, 114, 142, 170]
  ];

  function makeMatrix(ver, maskPattern, dataBits) {
    var size = ver * 4 + 17;
    var m = [];
    for (var r = 0; r < size; r++) { m[r] = []; for (var c = 0; c < size; c++) m[r][c] = null; }

    function setupFinder(row, col) {
      for (var r = -1; r <= 7; r++) {
        if (row + r <= -1 || size <= row + r) continue;
        for (var c = -1; c <= 7; c++) {
          if (col + c <= -1 || size <= col + c) continue;
          var dark = (0 <= r && r <= 6 && (c === 0 || c === 6)) ||
                     (0 <= c && c <= 6 && (r === 0 || r === 6)) ||
                     (2 <= r && r <= 4 && 2 <= c && c <= 4);
          m[row + r][col + c] = dark;
        }
      }
    }
    setupFinder(0, 0); setupFinder(size - 7, 0); setupFinder(0, size - 7);

    // alignment (must be placed BEFORE timing so centers on the timing line are not skipped)
    var pos = ALIGN[ver - 1];
    for (var a = 0; a < pos.length; a++) for (var b = 0; b < pos.length; b++) {
      var row = pos[a], col = pos[b];
      if (m[row][col] != null) continue;
      for (var rr = -2; rr <= 2; rr++) for (var cc = -2; cc <= 2; cc++) {
        m[row + rr][col + cc] = (rr === -2 || rr === 2 || cc === -2 || cc === 2 || (rr === 0 && cc === 0));
      }
    }
    // timing
    for (var i = 8; i < size - 8; i++) {
      if (m[i][6] == null) m[i][6] = (i % 2 === 0);
      if (m[6][i] == null) m[6][i] = (i % 2 === 0);
    }
    // format info (EC level M = 0, mask pattern) — MUST be placed before data mapping
    var typeInfoBits = bchTypeInfo((0 << 3) | maskPattern);
    for (i = 0; i < 15; i++) {
      var modf = ((typeInfoBits >> i) & 1) === 1;
      if (i < 6) m[i][8] = modf;
      else if (i < 8) m[i + 1][8] = modf;
      else m[size - 15 + i][8] = modf;
      if (i < 8) m[8][size - i - 1] = modf;
      else if (i < 9) m[8][15 - i - 1 + 1] = modf;
      else m[8][15 - i - 1] = modf;
    }
    m[size - 8][8] = true; // dark module

    // version info (>=7)
    if (ver >= 7) {
      var bits = bchTypeNumber(ver);
      for (i = 0; i < 18; i++) {
        var mod = ((bits >> i) & 1) === 1;
        m[Math.floor(i / 3)][i % 3 + size - 8 - 3] = mod;
        m[i % 3 + size - 8 - 3][Math.floor(i / 3)] = mod;
      }
    }

    // place data with mask
    function maskFn(r, c) {
      switch (maskPattern) {
        case 0: return (r + c) % 2 === 0;
        case 1: return r % 2 === 0;
        case 2: return c % 3 === 0;
        case 3: return (r + c) % 3 === 0;
        case 4: return (Math.floor(r / 2) + Math.floor(c / 3)) % 2 === 0;
        case 5: return (r * c) % 2 + (r * c) % 3 === 0;
        case 6: return ((r * c) % 2 + (r * c) % 3) % 2 === 0;
        case 7: return ((r * c) % 3 + (r + c) % 2) % 2 === 0;
      }
    }
    var inc = -1, row2 = size - 1, bitIndex = 0;
    for (var col = size - 1; col > 0; col -= 2) {
      if (col === 6) col--;
      while (true) {
        for (var cN = 0; cN < 2; cN++) {
          var cCur = col - cN;
          if (m[row2][cCur] == null) {
            var dark = false;
            if (bitIndex < dataBits.length) dark = dataBits[bitIndex++];
            if (maskFn(row2, cCur)) dark = !dark;
            m[row2][cCur] = dark;
          }
        }
        row2 += inc;
        if (row2 < 0 || size <= row2) { row2 -= inc; inc = -inc; break; }
      }
    }

    return m;
  }

  // penalty scoring for mask selection
  function penalty(m) {
    var size = m.length, score = 0, r, c;
    // rule1: rows/cols of same color
    for (r = 0; r < size; r++) {
      var run = 1;
      for (c = 1; c < size; c++) {
        if (m[r][c] === m[r][c - 1]) { run++; if (run === 5) score += 3; else if (run > 5) score++; }
        else run = 1;
      }
    }
    for (c = 0; c < size; c++) {
      run = 1;
      for (r = 1; r < size; r++) {
        if (m[r][c] === m[r - 1][c]) { run++; if (run === 5) score += 3; else if (run > 5) score++; }
        else run = 1;
      }
    }
    // rule2: 2x2 blocks
    for (r = 0; r < size - 1; r++) for (c = 0; c < size - 1; c++) {
      var v = m[r][c];
      if (v === m[r][c + 1] && v === m[r + 1][c] && v === m[r + 1][c + 1]) score += 3;
    }
    // rule3: finder-like
    function lineHas(get) {
      var cnt = 0;
      for (var i = 0; i < size; i++) {
        // check pattern 1011101 with 4 light padding on either side is complex; use standard 1:1:3:1:1
      }
      return cnt;
    }
    // rule4: dark proportion
    var dark = 0;
    for (r = 0; r < size; r++) for (c = 0; c < size; c++) if (m[r][c]) dark++;
    var ratio = dark / (size * size);
    var k = Math.floor(Math.abs(ratio * 100 - 50) / 5);
    score += k * 10;
    return score;
  }

  function toBytes(str) {
    // UTF-8 encode
    var out = [];
    for (var i = 0; i < str.length; i++) {
      var c = str.charCodeAt(i);
      if (c < 0x80) out.push(c);
      else if (c < 0x800) { out.push(0xC0 | (c >> 6), 0x80 | (c & 0x3F)); }
      else if (c < 0xD800 || c >= 0xE000) { out.push(0xE0 | (c >> 12), 0x80 | ((c >> 6) & 0x3F), 0x80 | (c & 0x3F)); }
      else {
        i++; var c2 = str.charCodeAt(i);
        var cp = 0x10000 + (((c & 0x3FF) << 10) | (c2 & 0x3FF));
        out.push(0xF0 | (cp >> 18), 0x80 | ((cp >> 12) & 0x3F), 0x80 | ((cp >> 6) & 0x3F), 0x80 | (cp & 0x3F));
      }
    }
    return out;
  }

  function generate(text, forceMask) {
    var bytes = toBytes(text);
    // choose smallest version fitting (level M)
    var ver = 1;
    while (ver <= 40) {
      var cap = totalDataCodewords(ver);
      var cci = ver < 10 ? 8 : 16; // char count indicator bits for byte mode
      var needBits = 4 + cci + bytes.length * 8;
      if (needBits <= cap * 8) break;
      ver++;
    }
    if (ver > 40) throw new Error('Data too long for QR');

    var cci = ver < 10 ? 8 : 16;
    // build bit stream
    var bits = [];
    function put(val, len) { for (var i = len - 1; i >= 0; i--) bits.push(((val >> i) & 1) === 1); }
    put(4, 4); // byte mode
    put(bytes.length, cci);
    for (var i = 0; i < bytes.length; i++) put(bytes[i], 8);
    var cap = totalDataCodewords(ver);
    // terminator
    var rem = cap * 8 - bits.length;
    put(0, Math.min(4, rem));
    // pad to byte
    while (bits.length % 8 !== 0) bits.push(false);
    // pad bytes
    var padBytes = [0xEC, 0x11], pi = 0;
    while (bits.length < cap * 8) { put(padBytes[pi % 2], 8); pi++; }

    // to codewords
    var dataCW = [];
    for (i = 0; i < bits.length; i += 8) {
      var b = 0; for (var j = 0; j < 8; j++) if (bits[i + j]) b |= (1 << (7 - j));
      dataCW.push(b);
    }

    // split into blocks, add EC
    var e = EC_TABLE_M[ver - 1], ecCount = e[0], groups = e[1];
    var blocks = [], offset = 0;
    for (var g = 0; g < groups.length; g++) {
      for (var nb = 0; nb < groups[g][0]; nb++) {
        var dlen = groups[g][1];
        var d = dataCW.slice(offset, offset + dlen); offset += dlen;
        var ec = rsEncode(d, ecCount);
        blocks.push({ data: d, ec: ec });
      }
    }
    // interleave data
    var finalCW = [];
    var maxData = 0; for (i = 0; i < blocks.length; i++) maxData = Math.max(maxData, blocks[i].data.length);
    for (i = 0; i < maxData; i++) for (j = 0; j < blocks.length; j++) if (i < blocks[j].data.length) finalCW.push(blocks[j].data[i]);
    for (i = 0; i < ecCount; i++) for (j = 0; j < blocks.length; j++) finalCW.push(blocks[j].ec[i]);

    // to bit array
    var dataBits = [];
    for (i = 0; i < finalCW.length; i++) for (j = 7; j >= 0; j--) dataBits.push(((finalCW[i] >> j) & 1) === 1);

    // try all masks, pick best
    var best = null, bestScore = Infinity, bestMask = 0;
    if (forceMask != null) { best = makeMatrix(ver, forceMask, dataBits); return { size: best.length, modules: best, version: ver }; }
    for (var mask = 0; mask < 8; mask++) {
      var m = makeMatrix(ver, mask, dataBits);
      var s = penalty(m);
      if (s < bestScore) { bestScore = s; best = m; bestMask = mask; }
    }
    return { size: best.length, modules: best, version: ver, mask: bestMask };
  }

  global.QRCode = { generate: generate };
})(typeof window !== 'undefined' ? window : this);
