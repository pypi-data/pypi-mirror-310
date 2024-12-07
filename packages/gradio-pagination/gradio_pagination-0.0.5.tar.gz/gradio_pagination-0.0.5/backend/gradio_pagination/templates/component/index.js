const {
  SvelteComponent: x,
  append: v,
  attr: k,
  destroy_each: G,
  detach: O,
  element: m,
  empty: $,
  ensure_array_like: T,
  flush: H,
  init: ee,
  insert: M,
  listen: A,
  noop: E,
  run_all: te,
  safe_not_equal: le,
  set_data: F,
  set_input_value: K,
  space: V,
  text: I,
  toggle_class: L
} = window.__gradio__svelte__internal, { tick: Q } = window.__gradio__svelte__internal;
function U(n, e, l) {
  const c = n.slice();
  return c[16] = e[l], c;
}
function W(n, e, l) {
  const c = n.slice();
  return c[19] = e[l], c;
}
function ne(n) {
  let e, l = (
    /*pageNumber*/
    n[19] + ""
  ), c, _, s;
  function r() {
    return (
      /*click_handler_1*/
      n[11](
        /*pageNumber*/
        n[19]
      )
    );
  }
  return {
    c() {
      e = m("button"), c = I(l), k(e, "class", "page-button svelte-1bca5rq"), L(
        e,
        "selected",
        /*page*/
        n[1] === /*pageNumber*/
        n[19]
      );
    },
    m(a, d) {
      M(a, e, d), v(e, c), _ || (s = A(e, "click", r), _ = !0);
    },
    p(a, d) {
      n = a, d & /*page, max_page*/
      18 && l !== (l = /*pageNumber*/
      n[19] + "") && F(c, l), d & /*page, paginationRange, max_page*/
      18 && L(
        e,
        "selected",
        /*page*/
        n[1] === /*pageNumber*/
        n[19]
      );
    },
    d(a) {
      a && O(e), _ = !1, s();
    }
  };
}
function ie(n) {
  let e;
  return {
    c() {
      e = m("span"), e.textContent = "...", k(e, "class", "dots svelte-1bca5rq");
    },
    m(l, c) {
      M(l, e, c);
    },
    p: E,
    d(l) {
      l && O(e);
    }
  };
}
function X(n) {
  let e;
  function l(s, r) {
    return (
      /*pageNumber*/
      s[19] === "..." ? ie : ne
    );
  }
  let c = l(n), _ = c(n);
  return {
    c() {
      _.c(), e = $();
    },
    m(s, r) {
      _.m(s, r), M(s, e, r);
    },
    p(s, r) {
      c === (c = l(s)) && _ ? _.p(s, r) : (_.d(1), _ = c(s), _ && (_.c(), _.m(e.parentNode, e)));
    },
    d(s) {
      s && O(e), _.d(s);
    }
  };
}
function Y(n) {
  let e, l = (
    /*size*/
    n[16] + ""
  ), c, _, s, r;
  return {
    c() {
      e = m("option"), c = I(l), _ = I(" per page"), e.__value = s = /*size*/
      n[16], K(e, e.__value), e.selected = r = /*size*/
      n[16] === /*page_size*/
      n[2];
    },
    m(a, d) {
      M(a, e, d), v(e, c), v(e, _);
    },
    p(a, d) {
      d & /*page_size_options*/
      8 && l !== (l = /*size*/
      a[16] + "") && F(c, l), d & /*page_size_options*/
      8 && s !== (s = /*size*/
      a[16]) && (e.__value = s, K(e, e.__value)), d & /*page_size_options, page_size*/
      12 && r !== (r = /*size*/
      a[16] === /*page_size*/
      a[2]) && (e.selected = r);
    },
    d(a) {
      a && O(e);
    }
  };
}
function oe(n) {
  let e, l, c, _, s, r, a, d, h, C, w, b, q, S, j, z, J, R, u = T(Z(
    /*page*/
    n[1],
    /*max_page*/
    n[4]
  )), o = [];
  for (let t = 0; t < u.length; t += 1)
    o[t] = X(W(n, u, t));
  let g = T(
    /*page_size_options*/
    n[3]
  ), f = [];
  for (let t = 0; t < g.length; t += 1)
    f[t] = Y(U(n, g, t));
  return {
    c() {
      e = m("div"), l = m("span"), c = I("Total "), _ = I(
        /*total*/
        n[0]
      ), s = I(" Items"), r = V(), a = m("button"), d = m("div"), C = V();
      for (let t = 0; t < o.length; t += 1)
        o[t].c();
      w = V(), b = m("button"), q = m("div"), j = V(), z = m("select");
      for (let t = 0; t < f.length; t += 1)
        f[t].c();
      k(l, "class", "total svelte-1bca5rq"), k(d, "class", "arrow-prev svelte-1bca5rq"), k(a, "class", "nav-button svelte-1bca5rq"), a.disabled = h = /*page*/
      n[1] === 1, k(q, "class", "arrow-next svelte-1bca5rq"), k(b, "class", "nav-button svelte-1bca5rq"), b.disabled = S = /*page*/
      n[1] === /*max_page*/
      n[4] || /*max_page*/
      n[4] <= 0, k(z, "class", "page-size-selector svelte-1bca5rq"), k(e, "class", "pagination svelte-1bca5rq");
    },
    m(t, p) {
      M(t, e, p), v(e, l), v(l, c), v(l, _), v(l, s), v(e, r), v(e, a), v(a, d), v(e, C);
      for (let i = 0; i < o.length; i += 1)
        o[i] && o[i].m(e, null);
      v(e, w), v(e, b), v(b, q), v(e, j), v(e, z);
      for (let i = 0; i < f.length; i += 1)
        f[i] && f[i].m(z, null);
      J || (R = [
        A(
          a,
          "click",
          /*click_handler*/
          n[10]
        ),
        A(
          b,
          "click",
          /*click_handler_2*/
          n[12]
        ),
        A(
          z,
          "change",
          /*handle_page_size_change*/
          n[7]
        )
      ], J = !0);
    },
    p(t, [p]) {
      if (p & /*total*/
      1 && F(
        _,
        /*total*/
        t[0]
      ), p & /*page*/
      2 && h !== (h = /*page*/
      t[1] === 1) && (a.disabled = h), p & /*paginationRange, page, max_page, handle_page_click, Number*/
      50) {
        u = T(Z(
          /*page*/
          t[1],
          /*max_page*/
          t[4]
        ));
        let i;
        for (i = 0; i < u.length; i += 1) {
          const y = W(t, u, i);
          o[i] ? o[i].p(y, p) : (o[i] = X(y), o[i].c(), o[i].m(e, w));
        }
        for (; i < o.length; i += 1)
          o[i].d(1);
        o.length = u.length;
      }
      if (p & /*page, max_page*/
      18 && S !== (S = /*page*/
      t[1] === /*max_page*/
      t[4] || /*max_page*/
      t[4] <= 0) && (b.disabled = S), p & /*page_size_options, page_size*/
      12) {
        g = T(
          /*page_size_options*/
          t[3]
        );
        let i;
        for (i = 0; i < g.length; i += 1) {
          const y = U(t, g, i);
          f[i] ? f[i].p(y, p) : (f[i] = Y(y), f[i].c(), f[i].m(z, null));
        }
        for (; i < f.length; i += 1)
          f[i].d(1);
        f.length = g.length;
      }
    },
    i: E,
    o: E,
    d(t) {
      t && O(e), G(o, t), G(f, t), J = !1, te(R);
    }
  };
}
function Z(n, e) {
  const l = [];
  if (e <= 0) return l;
  const c = 2, _ = Math.max(2, n - c), s = Math.min(e - 1, n + c);
  _ > 2 ? l.push(1, "...") : l.push(1);
  for (let r = _; r <= s; r++)
    l.includes(r) || l.push(r);
  return s < e - 1 ? l.push("...", e) : s === e - 1 && (l.includes(e) || l.push(e)), l;
}
function se(n, e, l) {
  var c = this && this.__awaiter || function(u, o, g, f) {
    function t(p) {
      return p instanceof g ? p : new g(function(i) {
        i(p);
      });
    }
    return new (g || (g = Promise))(function(p, i) {
      function y(N) {
        try {
          B(f.next(N));
        } catch (D) {
          i(D);
        }
      }
      function P(N) {
        try {
          B(f.throw(N));
        } catch (D) {
          i(D);
        }
      }
      function B(N) {
        N.done ? p(N.value) : t(N.value).then(y, P);
      }
      B((f = f.apply(u, o || [])).next());
    });
  };
  let { gradio: _ } = e, { value: s = "" } = e, r = 0, a = 1, d = 10, h = [];
  const C = (u) => {
    var o, g, f;
    try {
      const t = JSON.parse(u || "{}");
      return !((o = t == null ? void 0 : t.page_size_options) === null || o === void 0) && o.length && ((g = t == null ? void 0 : t.page_size_options) === null || g === void 0 || g.sort((p, i) => p - i)), t != null && t.page_size && !(t.page_size_options || h).includes(t == null ? void 0 : t.page_size) && (t.page_size = (f = t.page_size_options || h) === null || f === void 0 ? void 0 : f[0]), t;
    } catch (t) {
      return console.log(t), {
        total: 0,
        page: 1,
        page_size: (h == null ? void 0 : h[0]) || 10
      };
    }
  };
  let w;
  function b(u) {
    u !== a && (l(1, a = u), l(8, s = JSON.stringify({
      total: r,
      page: a,
      page_size: d,
      page_size_options: h
    })));
  }
  function q(u) {
    const o = a + u;
    o >= 1 && o <= w && (l(1, a = o), l(8, s = JSON.stringify({
      total: r,
      page: a,
      page_size: d,
      page_size_options: h
    })));
  }
  function S(u) {
    return c(this, void 0, void 0, function* () {
      const o = parseInt(u.target.value);
      o !== d && (l(2, d = o), l(1, a = 1), yield Q(), l(8, s = JSON.stringify({
        total: r,
        page: a,
        page_size: d,
        page_size_options: h
      })));
    });
  }
  function j() {
    return c(this, void 0, void 0, function* () {
      var u;
      const o = C(s);
      l(0, r = o.total), l(1, a = o.page), l(2, d = o.page_size), l(4, w = Math.ceil(r / d)), l(3, h = !((u = o.page_size_options) === null || u === void 0) && u.length ? o == null ? void 0 : o.page_size_options : h), yield Q(), _.dispatch("change");
    });
  }
  const z = () => q(-1), J = (u) => b(Number(u)), R = () => q(1);
  return n.$$set = (u) => {
    "gradio" in u && l(9, _ = u.gradio), "value" in u && l(8, s = u.value);
  }, n.$$.update = () => {
    n.$$.dirty & /*value*/
    256 && j();
  }, [
    r,
    a,
    d,
    h,
    w,
    b,
    q,
    S,
    s,
    _,
    z,
    J,
    R
  ];
}
class ae extends x {
  constructor(e) {
    super(), ee(this, e, se, oe, le, { gradio: 9, value: 8 });
  }
  get gradio() {
    return this.$$.ctx[9];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), H();
  }
  get value() {
    return this.$$.ctx[8];
  }
  set value(e) {
    this.$$set({ value: e }), H();
  }
}
export {
  ae as default
};
