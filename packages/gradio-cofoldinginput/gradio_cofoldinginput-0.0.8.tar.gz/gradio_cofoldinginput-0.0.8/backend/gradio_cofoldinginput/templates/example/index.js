const {
  SvelteComponent: j,
  add_iframe_resize_listener: P,
  add_render_callback: W,
  append_hydration: d,
  attr: A,
  binding_callbacks: F,
  children: E,
  claim_element: k,
  claim_space: D,
  claim_text: b,
  destroy_each: G,
  detach: u,
  element: g,
  empty: z,
  ensure_array_like: V,
  get_svelte_dataset: J,
  init: K,
  insert_hydration: m,
  noop: R,
  safe_not_equal: O,
  set_data: w,
  space: S,
  text: p,
  toggle_class: M
} = window.__gradio__svelte__internal, { onMount: Q } = window.__gradio__svelte__internal;
function q(a, e, n) {
  const i = a.slice();
  return i[8] = e[n], i;
}
function C(a) {
  let e, n, i, l, t, s = (
    /*value*/
    a[0].covMods.length + ""
  ), f, c;
  function o(_, y) {
    return (
      /*value*/
      _[0].chains.length > 1 ? Y : X
    );
  }
  let L = o(a), r = L(a), I = V(
    /*value*/
    a[0].chains
  ), v = [];
  for (let _ = 0; _ < I.length; _ += 1)
    v[_] = U(q(a, I, _));
  return {
    c() {
      r.c(), e = S(), n = g("ul");
      for (let _ = 0; _ < v.length; _ += 1)
        v[_].c();
      i = S(), l = g("ul"), t = g("li"), f = p(s), c = p(" covalent modifications");
    },
    l(_) {
      r.l(_), e = D(_), n = k(_, "UL", {});
      var y = E(n);
      for (let B = 0; B < v.length; B += 1)
        v[B].l(y);
      y.forEach(u), i = D(_), l = k(_, "UL", {});
      var h = E(l);
      t = k(h, "LI", {});
      var N = E(t);
      f = b(N, s), c = b(N, " covalent modifications"), N.forEach(u), h.forEach(u);
    },
    m(_, y) {
      r.m(_, y), m(_, e, y), m(_, n, y);
      for (let h = 0; h < v.length; h += 1)
        v[h] && v[h].m(n, null);
      m(_, i, y), m(_, l, y), d(l, t), d(t, f), d(t, c);
    },
    p(_, y) {
      if (L === (L = o(_)) && r ? r.p(_, y) : (r.d(1), r = L(_), r && (r.c(), r.m(e.parentNode, e))), y & /*value, undefined*/
      1) {
        I = V(
          /*value*/
          _[0].chains
        );
        let h;
        for (h = 0; h < I.length; h += 1) {
          const N = q(_, I, h);
          v[h] ? v[h].p(N, y) : (v[h] = U(N), v[h].c(), v[h].m(n, null));
        }
        for (; h < v.length; h += 1)
          v[h].d(1);
        v.length = I.length;
      }
      y & /*value*/
      1 && s !== (s = /*value*/
      _[0].covMods.length + "") && w(f, s);
    },
    d(_) {
      _ && (u(e), u(n), u(i), u(l)), r.d(_), G(v, _);
    }
  };
}
function X(a) {
  let e, n, i = (
    /*value*/
    a[0].chains.length + ""
  ), l, t, s;
  return {
    c() {
      e = g("b"), n = p("Input composed of "), l = p(i), t = p(" chain "), s = g("br");
    },
    l(f) {
      e = k(f, "B", {});
      var c = E(e);
      n = b(c, "Input composed of "), l = b(c, i), t = b(c, " chain "), c.forEach(u), s = k(f, "BR", {});
    },
    m(f, c) {
      m(f, e, c), d(e, n), d(e, l), d(e, t), m(f, s, c);
    },
    p(f, c) {
      c & /*value*/
      1 && i !== (i = /*value*/
      f[0].chains.length + "") && w(l, i);
    },
    d(f) {
      f && (u(e), u(s));
    }
  };
}
function Y(a) {
  let e, n, i = (
    /*value*/
    a[0].chains.length + ""
  ), l, t, s, f;
  return {
    c() {
      e = g("b"), n = p("Input composed of "), l = p(i), t = p(" chains"), s = S(), f = g("br");
    },
    l(c) {
      e = k(c, "B", {});
      var o = E(e);
      n = b(o, "Input composed of "), l = b(o, i), t = b(o, " chains"), o.forEach(u), s = D(c), f = k(c, "BR", {});
    },
    m(c, o) {
      m(c, e, o), d(e, n), d(e, l), d(e, t), m(c, s, o), m(c, f, o);
    },
    p(c, o) {
      o & /*value*/
      1 && i !== (i = /*value*/
      c[0].chains.length + "") && w(l, i);
    },
    d(c) {
      c && (u(e), u(s), u(f));
    }
  };
}
function H(a) {
  let e, n, i = (
    /*val*/
    a[8].class + ""
  ), l, t, s = (
    /*val*/
    a[8].sequence.length + ""
  ), f, c;
  return {
    c() {
      e = g("li"), n = g("div"), l = p(i), t = S(), f = p(s), c = p(" residues"), this.h();
    },
    l(o) {
      e = k(o, "LI", {});
      var L = E(e);
      n = k(L, "DIV", { class: !0 });
      var r = E(n);
      l = b(r, i), t = D(r), f = b(r, s), c = b(r, " residues"), r.forEach(u), L.forEach(u), this.h();
    },
    h() {
      A(n, "class", "svelte-166104d");
    },
    m(o, L) {
      m(o, e, L), d(e, n), d(n, l), d(n, t), d(n, f), d(n, c);
    },
    p(o, L) {
      L & /*value*/
      1 && i !== (i = /*val*/
      o[8].class + "") && w(l, i), L & /*value*/
      1 && s !== (s = /*val*/
      o[8].sequence.length + "") && w(f, s);
    },
    d(o) {
      o && u(e);
    }
  };
}
function T(a) {
  let e;
  function n(t, s) {
    return (
      /*val*/
      t[8].name != null ? $ : (
        /*val*/
        t[8].smiles != null ? x : Z
      )
    );
  }
  let i = n(a), l = i(a);
  return {
    c() {
      l.c(), e = z();
    },
    l(t) {
      l.l(t), e = z();
    },
    m(t, s) {
      l.m(t, s), m(t, e, s);
    },
    p(t, s) {
      i === (i = n(t)) && l ? l.p(t, s) : (l.d(1), l = i(t), l && (l.c(), l.m(e.parentNode, e)));
    },
    d(t) {
      t && u(e), l.d(t);
    }
  };
}
function Z(a) {
  let e, n = '<div class="svelte-166104d">Ligand</div>';
  return {
    c() {
      e = g("li"), e.innerHTML = n;
    },
    l(i) {
      e = k(i, "LI", { "data-svelte-h": !0 }), J(e) !== "svelte-z73xb2" && (e.innerHTML = n);
    },
    m(i, l) {
      m(i, e, l);
    },
    p: R,
    d(i) {
      i && u(e);
    }
  };
}
function x(a) {
  let e, n, i, l = (
    /*val*/
    a[8].smiles.length + ""
  ), t, s;
  return {
    c() {
      e = g("li"), n = g("div"), i = p("Ligand SMILES with "), t = p(l), s = p(" atoms"), this.h();
    },
    l(f) {
      e = k(f, "LI", {});
      var c = E(e);
      n = k(c, "DIV", { class: !0 });
      var o = E(n);
      i = b(o, "Ligand SMILES with "), t = b(o, l), s = b(o, " atoms"), o.forEach(u), c.forEach(u), this.h();
    },
    h() {
      A(n, "class", "svelte-166104d");
    },
    m(f, c) {
      m(f, e, c), d(e, n), d(n, i), d(n, t), d(n, s);
    },
    p(f, c) {
      c & /*value*/
      1 && l !== (l = /*val*/
      f[8].smiles.length + "") && w(t, l);
    },
    d(f) {
      f && u(e);
    }
  };
}
function $(a) {
  let e, n, i, l = (
    /*val*/
    a[8].name + ""
  ), t;
  return {
    c() {
      e = g("li"), n = g("div"), i = p("Ligand "), t = p(l), this.h();
    },
    l(s) {
      e = k(s, "LI", {});
      var f = E(e);
      n = k(f, "DIV", { class: !0 });
      var c = E(n);
      i = b(c, "Ligand "), t = b(c, l), c.forEach(u), f.forEach(u), this.h();
    },
    h() {
      A(n, "class", "svelte-166104d");
    },
    m(s, f) {
      m(s, e, f), d(e, n), d(n, i), d(n, t);
    },
    p(s, f) {
      f & /*value*/
      1 && l !== (l = /*val*/
      s[8].name + "") && w(t, l);
    },
    d(s) {
      s && u(e);
    }
  };
}
function U(a) {
  let e = ["protein", "DNA", "RNA"].includes(
    /*val*/
    a[8].class
  ), n, i, l = e && H(a), t = (
    /*val*/
    a[8].class == "ligand" && T(a)
  );
  return {
    c() {
      l && l.c(), n = S(), t && t.c(), i = z();
    },
    l(s) {
      l && l.l(s), n = D(s), t && t.l(s), i = z();
    },
    m(s, f) {
      l && l.m(s, f), m(s, n, f), t && t.m(s, f), m(s, i, f);
    },
    p(s, f) {
      f & /*value*/
      1 && (e = ["protein", "DNA", "RNA"].includes(
        /*val*/
        s[8].class
      )), e ? l ? l.p(s, f) : (l = H(s), l.c(), l.m(n.parentNode, n)) : l && (l.d(1), l = null), /*val*/
      s[8].class == "ligand" ? t ? t.p(s, f) : (t = T(s), t.c(), t.m(i.parentNode, i)) : t && (t.d(1), t = null);
    },
    d(s) {
      s && (u(n), u(i)), l && l.d(s), t && t.d(s);
    }
  };
}
function ee(a) {
  let e, n, i = (
    /*value*/
    a[0] && C(a)
  );
  return {
    c() {
      e = g("div"), i && i.c(), this.h();
    },
    l(l) {
      e = k(l, "DIV", { class: !0 });
      var t = E(e);
      i && i.l(t), t.forEach(u), this.h();
    },
    h() {
      A(e, "class", "flex items-center justify-center w-full svelte-166104d"), W(() => (
        /*div_elementresize_handler*/
        a[5].call(e)
      )), M(
        e,
        "table",
        /*type*/
        a[1] === "table"
      ), M(
        e,
        "gallery",
        /*type*/
        a[1] === "gallery"
      ), M(
        e,
        "selected",
        /*selected*/
        a[2]
      );
    },
    m(l, t) {
      m(l, e, t), i && i.m(e, null), n = P(
        e,
        /*div_elementresize_handler*/
        a[5].bind(e)
      ), a[6](e);
    },
    p(l, [t]) {
      /*value*/
      l[0] ? i ? i.p(l, t) : (i = C(l), i.c(), i.m(e, null)) : i && (i.d(1), i = null), t & /*type*/
      2 && M(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), t & /*type*/
      2 && M(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), t & /*selected*/
      4 && M(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    i: R,
    o: R,
    d(l) {
      l && u(e), i && i.d(), n(), a[6](null);
    }
  };
}
function le(a, e, n) {
  let { value: i } = e, { type: l } = e, { selected: t = !1 } = e, s, f;
  function c(r, I) {
    !r || !I || (f.style.setProperty("--local-text-width", `${I < 150 ? I : 200}px`), n(4, f.style.whiteSpace = "unset", f));
  }
  Q(() => {
    c(f, s);
  });
  function o() {
    s = this.clientWidth, n(3, s);
  }
  function L(r) {
    F[r ? "unshift" : "push"](() => {
      f = r, n(4, f);
    });
  }
  return a.$$set = (r) => {
    "value" in r && n(0, i = r.value), "type" in r && n(1, l = r.type), "selected" in r && n(2, t = r.selected);
  }, [i, l, t, s, f, o, L];
}
class te extends j {
  constructor(e) {
    super(), K(this, e, le, ee, O, { value: 0, type: 1, selected: 2 });
  }
}
export {
  te as default
};
