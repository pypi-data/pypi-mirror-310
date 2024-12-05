import { g as X, b as Y } from "./Index-zdRnnhyX.js";
function Z(t) {
  return t === void 0;
}
function E() {
}
function v(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function V(t, ...e) {
  if (t == null) {
    for (const s of e)
      s(void 0);
    return E;
  }
  const n = t.subscribe(...e);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function P(t) {
  let e;
  return V(t, (n) => e = n)(), e;
}
const C = [];
function b(t, e = E) {
  let n;
  const s = /* @__PURE__ */ new Set();
  function o(l) {
    if (v(t, l) && (t = l, n)) {
      const d = !C.length;
      for (const a of s)
        a[1](), C.push(a, t);
      if (d) {
        for (let a = 0; a < C.length; a += 2)
          C[a][0](C[a + 1]);
        C.length = 0;
      }
    }
  }
  function r(l) {
    o(l(t));
  }
  function i(l, d = E) {
    const a = [l, d];
    return s.add(a), s.size === 1 && (n = e(o, r) || E), l(t), () => {
      s.delete(a), s.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: o,
    update: r,
    subscribe: i
  };
}
const {
  getContext: $,
  setContext: qe
} = window.__gradio__svelte__internal, ee = "$$ms-gr-loading-status-key";
function te() {
  const t = window.ms_globals.loadingKey++, e = $(ee);
  return (n) => {
    if (!e || !n)
      return;
    const {
      loadingStatusMap: s,
      options: o
    } = e, {
      generating: r,
      error: i
    } = P(o);
    (n == null ? void 0 : n.status) === "pending" || i && (n == null ? void 0 : n.status) === "error" || (r && (n == null ? void 0 : n.status)) === "generating" ? s.update(({
      map: l
    }) => (l.set(t, n), {
      map: l
    })) : s.update(({
      map: l
    }) => (l.delete(t), {
      map: l
    }));
  };
}
const {
  getContext: N,
  setContext: I
} = window.__gradio__svelte__internal, ne = "$$ms-gr-slots-key";
function se() {
  const t = b({});
  return I(ne, t);
}
const re = "$$ms-gr-render-slot-context-key";
function oe() {
  const t = I(re, b({}));
  return (e, n) => {
    t.update((s) => typeof n == "function" ? {
      ...s,
      [e]: n(s[e])
    } : {
      ...s,
      [e]: n
    });
  };
}
const ie = "$$ms-gr-context-key";
function F(t) {
  return Z(t) ? {} : typeof t == "object" && !Array.isArray(t) ? t : {
    value: t
  };
}
const U = "$$ms-gr-sub-index-context-key";
function le() {
  return N(U) || null;
}
function T(t) {
  return I(U, t);
}
function ce(t, e, n) {
  var x, h;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const s = G(), o = fe({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  }), r = le();
  typeof r == "number" && T(void 0);
  const i = te();
  typeof t._internal.subIndex == "number" && T(t._internal.subIndex), s && s.subscribe((c) => {
    o.slotKey.set(c);
  }), ue();
  const l = N(ie), d = ((x = P(l)) == null ? void 0 : x.as_item) || t.as_item, a = F(l ? d ? ((h = P(l)) == null ? void 0 : h[d]) || {} : P(l) || {} : {}), _ = (c, f) => c ? X({
    ...c,
    ...f || {}
  }, e) : void 0, m = b({
    ...t,
    _internal: {
      ...t._internal,
      index: r ?? t._internal.index
    },
    ...a,
    restProps: _(t.restProps, a),
    originalRestProps: t.restProps
  });
  return l ? (l.subscribe((c) => {
    const {
      as_item: f
    } = P(m);
    f && (c = c == null ? void 0 : c[f]), c = F(c), m.update((p) => ({
      ...p,
      ...c || {},
      restProps: _(p.restProps, c)
    }));
  }), [m, (c) => {
    var p, y;
    const f = F(c.as_item ? ((p = P(l)) == null ? void 0 : p[c.as_item]) || {} : P(l) || {});
    return i((y = c.restProps) == null ? void 0 : y.loading_status), m.set({
      ...c,
      _internal: {
        ...c._internal,
        index: r ?? c._internal.index
      },
      ...f,
      restProps: _(c.restProps, f),
      originalRestProps: c.restProps
    });
  }]) : [m, (c) => {
    var f;
    i((f = c.restProps) == null ? void 0 : f.loading_status), m.set({
      ...c,
      _internal: {
        ...c._internal,
        index: r ?? c._internal.index
      },
      restProps: _(c.restProps),
      originalRestProps: c.restProps
    });
  }];
}
const B = "$$ms-gr-slot-key";
function ue() {
  I(B, b(void 0));
}
function G() {
  return N(B);
}
const ae = "$$ms-gr-component-slot-context-key";
function fe({
  slot: t,
  index: e,
  subIndex: n
}) {
  return I(ae, {
    slotKey: b(t),
    slotIndex: b(e),
    subSlotIndex: b(n)
  });
}
function S(t) {
  try {
    if (typeof t == "string") {
      let e = t.trim();
      return e.startsWith(";") && (e = e.slice(1)), e.endsWith(";") && (e = e.slice(0, -1)), new Function(`return (...args) => (${e})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function de(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var H = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(t) {
  (function() {
    var e = {}.hasOwnProperty;
    function n() {
      for (var r = "", i = 0; i < arguments.length; i++) {
        var l = arguments[i];
        l && (r = o(r, s(l)));
      }
      return r;
    }
    function s(r) {
      if (typeof r == "string" || typeof r == "number")
        return r;
      if (typeof r != "object")
        return "";
      if (Array.isArray(r))
        return n.apply(null, r);
      if (r.toString !== Object.prototype.toString && !r.toString.toString().includes("[native code]"))
        return r.toString();
      var i = "";
      for (var l in r)
        e.call(r, l) && r[l] && (i = o(i, l));
      return i;
    }
    function o(r, i) {
      return i ? r ? r + " " + i : r + i : r;
    }
    t.exports ? (n.default = n, t.exports = n) : window.classNames = n;
  })();
})(H);
var _e = H.exports;
const me = /* @__PURE__ */ de(_e), {
  getContext: pe,
  setContext: be
} = window.__gradio__svelte__internal;
function ge(t) {
  const e = `$$ms-gr-${t}-context-key`;
  function n(o = ["default"]) {
    const r = o.reduce((i, l) => (i[l] = b([]), i), {});
    return be(e, {
      itemsMap: r,
      allowedSlots: o
    }), r;
  }
  function s() {
    const {
      itemsMap: o,
      allowedSlots: r
    } = pe(e);
    return function(i, l, d) {
      o && (i ? o[i].update((a) => {
        const _ = [...a];
        return r.includes(i) ? _[l] = d : _[l] = void 0, _;
      }) : r.includes("default") && o.default.update((a) => {
        const _ = [...a];
        return _[l] = d, _;
      }));
    };
  }
  return {
    getItems: n,
    getSetItemFn: s
  };
}
const {
  getItems: Ae,
  getSetItemFn: xe
} = ge("table-expandable"), {
  SvelteComponent: ye,
  assign: z,
  check_outros: Pe,
  component_subscribe: w,
  compute_rest_props: L,
  create_slot: he,
  detach: Ce,
  empty: W,
  exclude_internal_props: Ie,
  flush: g,
  get_all_dirty_from_scope: Re,
  get_slot_changes: Ke,
  group_outros: Se,
  init: we,
  insert_hydration: Ee,
  safe_not_equal: ke,
  transition_in: k,
  transition_out: j,
  update_slot_base: Fe
} = window.__gradio__svelte__internal;
function D(t) {
  let e;
  const n = (
    /*#slots*/
    t[17].default
  ), s = he(
    n,
    t,
    /*$$scope*/
    t[16],
    null
  );
  return {
    c() {
      s && s.c();
    },
    l(o) {
      s && s.l(o);
    },
    m(o, r) {
      s && s.m(o, r), e = !0;
    },
    p(o, r) {
      s && s.p && (!e || r & /*$$scope*/
      65536) && Fe(
        s,
        n,
        o,
        /*$$scope*/
        o[16],
        e ? Ke(
          n,
          /*$$scope*/
          o[16],
          r,
          null
        ) : Re(
          /*$$scope*/
          o[16]
        ),
        null
      );
    },
    i(o) {
      e || (k(s, o), e = !0);
    },
    o(o) {
      j(s, o), e = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function je(t) {
  let e, n, s = (
    /*$mergedProps*/
    t[0].visible && D(t)
  );
  return {
    c() {
      s && s.c(), e = W();
    },
    l(o) {
      s && s.l(o), e = W();
    },
    m(o, r) {
      s && s.m(o, r), Ee(o, e, r), n = !0;
    },
    p(o, [r]) {
      /*$mergedProps*/
      o[0].visible ? s ? (s.p(o, r), r & /*$mergedProps*/
      1 && k(s, 1)) : (s = D(o), s.c(), k(s, 1), s.m(e.parentNode, e)) : s && (Se(), j(s, 1, 1, () => {
        s = null;
      }), Pe());
    },
    i(o) {
      n || (k(s), n = !0);
    },
    o(o) {
      j(s), n = !1;
    },
    d(o) {
      o && Ce(e), s && s.d(o);
    }
  };
}
function Ne(t, e, n) {
  const s = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = L(e, s), r, i, l, d, {
    $$slots: a = {},
    $$scope: _
  } = e, {
    gradio: m
  } = e, {
    props: x = {}
  } = e;
  const h = b(x);
  w(t, h, (u) => n(15, d = u));
  let {
    _internal: c = {}
  } = e, {
    as_item: f
  } = e, {
    visible: p = !0
  } = e, {
    elem_id: y = ""
  } = e, {
    elem_classes: R = []
  } = e, {
    elem_style: K = {}
  } = e;
  const O = G();
  w(t, O, (u) => n(14, l = u));
  const [q, J] = ce({
    gradio: m,
    props: d,
    _internal: c,
    visible: p,
    elem_id: y,
    elem_classes: R,
    elem_style: K,
    as_item: f,
    restProps: o
  });
  w(t, q, (u) => n(0, i = u));
  const A = se();
  w(t, A, (u) => n(13, r = u));
  const M = oe(), Q = xe();
  return t.$$set = (u) => {
    e = z(z({}, e), Ie(u)), n(21, o = L(e, s)), "gradio" in u && n(5, m = u.gradio), "props" in u && n(6, x = u.props), "_internal" in u && n(7, c = u._internal), "as_item" in u && n(8, f = u.as_item), "visible" in u && n(9, p = u.visible), "elem_id" in u && n(10, y = u.elem_id), "elem_classes" in u && n(11, R = u.elem_classes), "elem_style" in u && n(12, K = u.elem_style), "$$scope" in u && n(16, _ = u.$$scope);
  }, t.$$.update = () => {
    if (t.$$.dirty & /*props*/
    64 && h.update((u) => ({
      ...u,
      ...x
    })), J({
      gradio: m,
      props: d,
      _internal: c,
      visible: p,
      elem_id: y,
      elem_classes: R,
      elem_style: K,
      as_item: f,
      restProps: o
    }), t.$$.dirty & /*$mergedProps, $slotKey, $slots*/
    24577) {
      const u = Y(i);
      Q(l, i._internal.index || 0, {
        props: {
          style: i.elem_style,
          className: me(i.elem_classes, "ms-gr-antd-table-expandable"),
          id: i.elem_id,
          ...i.restProps,
          ...i.props,
          ...u,
          expandedRowClassName: S(i.props.expandedRowClassName || i.restProps.expandedRowClassName),
          expandedRowRender: S(i.props.expandedRowRender || i.restProps.expandedRowRender),
          rowExpandable: S(i.props.rowExpandable || i.restProps.rowExpandable),
          expandIcon: S(i.props.expandIcon || i.restProps.expandIcon),
          columnTitle: i.props.columnTitle || i.restProps.columnTitle
        },
        slots: {
          ...r,
          expandIcon: {
            el: r.expandIcon,
            callback: M,
            clone: !0
          },
          expandedRowRender: {
            el: r.expandedRowRender,
            callback: M,
            clone: !0
          }
        }
      });
    }
  }, [i, h, O, q, A, m, x, c, f, p, y, R, K, r, l, d, _, a];
}
class Me extends ye {
  constructor(e) {
    super(), we(this, e, Ne, je, ke, {
      gradio: 5,
      props: 6,
      _internal: 7,
      as_item: 8,
      visible: 9,
      elem_id: 10,
      elem_classes: 11,
      elem_style: 12
    });
  }
  get gradio() {
    return this.$$.ctx[5];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), g();
  }
  get props() {
    return this.$$.ctx[6];
  }
  set props(e) {
    this.$$set({
      props: e
    }), g();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), g();
  }
  get as_item() {
    return this.$$.ctx[8];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), g();
  }
  get visible() {
    return this.$$.ctx[9];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), g();
  }
  get elem_id() {
    return this.$$.ctx[10];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), g();
  }
  get elem_classes() {
    return this.$$.ctx[11];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), g();
  }
  get elem_style() {
    return this.$$.ctx[12];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), g();
  }
}
export {
  Me as default
};
