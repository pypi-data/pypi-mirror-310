import { g as oe, b as ie } from "./Index-zLSw6Mm5.js";
const E = window.ms_globals.React, le = window.ms_globals.React.forwardRef, ce = window.ms_globals.React.useRef, ue = window.ms_globals.React.useState, ae = window.ms_globals.React.useEffect, fe = window.ms_globals.ReactDOM.createPortal;
function de(e) {
  return e === void 0;
}
function k() {
}
function me(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function _e(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return k;
  }
  const r = e.subscribe(...t);
  return r.unsubscribe ? () => r.unsubscribe() : r;
}
function P(e) {
  let t;
  return _e(e, (r) => t = r)(), t;
}
const w = [];
function y(e, t = k) {
  let r;
  const n = /* @__PURE__ */ new Set();
  function o(l) {
    if (me(e, l) && (e = l, r)) {
      const u = !w.length;
      for (const f of n)
        f[1](), w.push(f, e);
      if (u) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function s(l) {
    o(l(e));
  }
  function i(l, u = k) {
    const f = [l, u];
    return n.add(f), n.size === 1 && (r = t(o, s) || k), l(e), () => {
      n.delete(f), n.size === 0 && r && (r(), r = null);
    };
  }
  return {
    set: o,
    update: s,
    subscribe: i
  };
}
const {
  getContext: pe,
  setContext: ot
} = window.__gradio__svelte__internal, ge = "$$ms-gr-loading-status-key";
function be() {
  const e = window.ms_globals.loadingKey++, t = pe(ge);
  return (r) => {
    if (!t || !r)
      return;
    const {
      loadingStatusMap: n,
      options: o
    } = t, {
      generating: s,
      error: i
    } = P(o);
    (r == null ? void 0 : r.status) === "pending" || i && (r == null ? void 0 : r.status) === "error" || (s && (r == null ? void 0 : r.status)) === "generating" ? n.update(({
      map: l
    }) => (l.set(e, r), {
      map: l
    })) : n.update(({
      map: l
    }) => (l.delete(e), {
      map: l
    }));
  };
}
const {
  getContext: T,
  setContext: I
} = window.__gradio__svelte__internal, he = "$$ms-gr-slots-key";
function ye() {
  const e = y({});
  return I(he, e);
}
const xe = "$$ms-gr-render-slot-context-key";
function Ce() {
  const e = I(xe, y({}));
  return (t, r) => {
    e.update((n) => typeof r == "function" ? {
      ...n,
      [t]: r(n[t])
    } : {
      ...n,
      [t]: r
    });
  };
}
const Pe = "$$ms-gr-context-key";
function F(e) {
  return de(e) ? {} : typeof e == "object" && !Array.isArray(e) ? e : {
    value: e
  };
}
const Q = "$$ms-gr-sub-index-context-key";
function Ee() {
  return T(Q) || null;
}
function D(e) {
  return I(Q, e);
}
function we(e, t, r) {
  var m, g;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const n = Z(), o = Re({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), s = Ee();
  typeof s == "number" && D(void 0);
  const i = be();
  typeof e._internal.subIndex == "number" && D(e._internal.subIndex), n && n.subscribe((c) => {
    o.slotKey.set(c);
  }), Se();
  const l = T(Pe), u = ((m = P(l)) == null ? void 0 : m.as_item) || e.as_item, f = F(l ? u ? ((g = P(l)) == null ? void 0 : g[u]) || {} : P(l) || {} : {}), d = (c, _) => c ? oe({
    ...c,
    ..._ || {}
  }, t) : void 0, p = y({
    ...e,
    _internal: {
      ...e._internal,
      index: s ?? e._internal.index
    },
    ...f,
    restProps: d(e.restProps, f),
    originalRestProps: e.restProps
  });
  return l ? (l.subscribe((c) => {
    const {
      as_item: _
    } = P(p);
    _ && (c = c == null ? void 0 : c[_]), c = F(c), p.update((b) => ({
      ...b,
      ...c || {},
      restProps: d(b.restProps, c)
    }));
  }), [p, (c) => {
    var b, h;
    const _ = F(c.as_item ? ((b = P(l)) == null ? void 0 : b[c.as_item]) || {} : P(l) || {});
    return i((h = c.restProps) == null ? void 0 : h.loading_status), p.set({
      ...c,
      _internal: {
        ...c._internal,
        index: s ?? c._internal.index
      },
      ..._,
      restProps: d(c.restProps, _),
      originalRestProps: c.restProps
    });
  }]) : [p, (c) => {
    var _;
    i((_ = c.restProps) == null ? void 0 : _.loading_status), p.set({
      ...c,
      _internal: {
        ...c._internal,
        index: s ?? c._internal.index
      },
      restProps: d(c.restProps),
      originalRestProps: c.restProps
    });
  }];
}
const X = "$$ms-gr-slot-key";
function Se() {
  I(X, y(void 0));
}
function Z() {
  return T(X);
}
const Ie = "$$ms-gr-component-slot-context-key";
function Re({
  slot: e,
  index: t,
  subIndex: r
}) {
  return I(Ie, {
    slotKey: y(e),
    slotIndex: y(t),
    subSlotIndex: y(r)
  });
}
function N(e) {
  try {
    if (typeof e == "string") {
      let t = e.trim();
      return t.startsWith(";") && (t = t.slice(1)), t.endsWith(";") && (t = t.slice(0, -1)), new Function(`return (...args) => (${t})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Oe(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var V = {
  exports: {}
}, v = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ke = E, je = Symbol.for("react.element"), ve = Symbol.for("react.fragment"), Fe = Object.prototype.hasOwnProperty, Ne = ke.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ke = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $(e, t, r) {
  var n, o = {}, s = null, i = null;
  r !== void 0 && (s = "" + r), t.key !== void 0 && (s = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (n in t) Fe.call(t, n) && !Ke.hasOwnProperty(n) && (o[n] = t[n]);
  if (e && e.defaultProps) for (n in t = e.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: je,
    type: e,
    key: s,
    ref: i,
    props: o,
    _owner: Ne.current
  };
}
v.Fragment = ve;
v.jsx = $;
v.jsxs = $;
V.exports = v;
var U = V.exports;
const Le = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Te(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const n = e[r];
    return typeof n == "number" && !Le.includes(r) ? t[r] = n + "px" : t[r] = n, t;
  }, {}) : {};
}
function K(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(fe(E.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: E.Children.toArray(e._reactElement.props.children).map((o) => {
        if (E.isValidElement(o) && o.props.__slot__) {
          const {
            portals: s,
            clonedElement: i
          } = K(o.props.el);
          return E.cloneElement(o, {
            ...o.props,
            el: i,
            children: [...E.Children.toArray(o.props.children), ...s]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: i,
      type: l,
      useCapture: u
    }) => {
      r.addEventListener(l, i, u);
    });
  });
  const n = Array.from(e.childNodes);
  for (let o = 0; o < n.length; o++) {
    const s = n[o];
    if (s.nodeType === 1) {
      const {
        clonedElement: i,
        portals: l
      } = K(s);
      t.push(...l), r.appendChild(i);
    } else s.nodeType === 3 && r.appendChild(s.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Ae(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const G = le(({
  slot: e,
  clone: t,
  className: r,
  style: n
}, o) => {
  const s = ce(), [i, l] = ue([]);
  return ae(() => {
    var p;
    if (!s.current || !e)
      return;
    let u = e;
    function f() {
      let m = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (m = u.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), Ae(o, m), r && m.classList.add(...r.split(" ")), n) {
        const g = Te(n);
        Object.keys(g).forEach((c) => {
          m.style[c] = g[c];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let m = function() {
        var b, h, C;
        (b = s.current) != null && b.contains(u) && ((h = s.current) == null || h.removeChild(u));
        const {
          portals: c,
          clonedElement: _
        } = K(e);
        return u = _, l(c), u.style.display = "contents", f(), (C = s.current) == null || C.appendChild(u), c.length > 0;
      };
      m() || (d = new window.MutationObserver(() => {
        m() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      u.style.display = "contents", f(), (p = s.current) == null || p.appendChild(u);
    return () => {
      var m, g;
      u.style.display = "", (m = s.current) != null && m.contains(u) && ((g = s.current) == null || g.removeChild(u)), d == null || d.disconnect();
    };
  }, [e, t, r, n, o]), E.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...i);
});
function ee(e, t, r) {
  return e.filter(Boolean).map((n, o) => {
    var u;
    if (typeof n != "object")
      return n;
    const s = {
      ...n.props,
      key: ((u = n.props) == null ? void 0 : u.key) ?? (r ? `${r}-${o}` : `${o}`)
    };
    let i = s;
    Object.keys(n.slots).forEach((f) => {
      if (!n.slots[f] || !(n.slots[f] instanceof Element) && !n.slots[f].el)
        return;
      const d = f.split(".");
      d.forEach((_, b) => {
        i[_] || (i[_] = {}), b !== d.length - 1 && (i = s[_]);
      });
      const p = n.slots[f];
      let m, g, c = !1;
      p instanceof Element ? m = p : (m = p.el, g = p.callback, c = p.clone ?? !1), i[d[d.length - 1]] = m ? g ? (..._) => (g(d[d.length - 1], _), /* @__PURE__ */ U.jsx(G, {
        slot: m,
        clone: c
      })) : /* @__PURE__ */ U.jsx(G, {
        slot: m,
        clone: c
      }) : i[d[d.length - 1]], i = s;
    });
    const l = "children";
    return n[l] && (s[l] = ee(n[l], t, `${o}`)), s;
  });
}
var te = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function r() {
      for (var s = "", i = 0; i < arguments.length; i++) {
        var l = arguments[i];
        l && (s = o(s, n(l)));
      }
      return s;
    }
    function n(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return r.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var i = "";
      for (var l in s)
        t.call(s, l) && s[l] && (i = o(i, l));
      return i;
    }
    function o(s, i) {
      return i ? s ? s + " " + i : s + i : s;
    }
    e.exports ? (r.default = r, e.exports = r) : window.classNames = r;
  })();
})(te);
var Me = te.exports;
const qe = /* @__PURE__ */ Oe(Me), {
  getContext: We,
  setContext: ze
} = window.__gradio__svelte__internal;
function ne(e) {
  const t = `$$ms-gr-${e}-context-key`;
  function r(o = ["default"]) {
    const s = o.reduce((i, l) => (i[l] = y([]), i), {});
    return ze(t, {
      itemsMap: s,
      allowedSlots: o
    }), s;
  }
  function n() {
    const {
      itemsMap: o,
      allowedSlots: s
    } = We(t);
    return function(i, l, u) {
      o && (i ? o[i].update((f) => {
        const d = [...f];
        return s.includes(i) ? d[l] = u : d[l] = void 0, d;
      }) : s.includes("default") && o.default.update((f) => {
        const d = [...f];
        return d[l] = u, d;
      }));
    };
  }
  return {
    getItems: r,
    getSetItemFn: n
  };
}
const {
  getItems: De,
  getSetItemFn: it
} = ne("table-row-selection-selection"), {
  getItems: lt,
  getSetItemFn: Ue
} = ne("table-row-selection"), {
  SvelteComponent: Ge,
  assign: H,
  check_outros: He,
  component_subscribe: S,
  compute_rest_props: B,
  create_slot: Be,
  detach: Je,
  empty: J,
  exclude_internal_props: Ye,
  flush: x,
  get_all_dirty_from_scope: Qe,
  get_slot_changes: Xe,
  group_outros: Ze,
  init: Ve,
  insert_hydration: $e,
  safe_not_equal: et,
  transition_in: j,
  transition_out: L,
  update_slot_base: tt
} = window.__gradio__svelte__internal;
function Y(e) {
  let t;
  const r = (
    /*#slots*/
    e[19].default
  ), n = Be(
    r,
    e,
    /*$$scope*/
    e[18],
    null
  );
  return {
    c() {
      n && n.c();
    },
    l(o) {
      n && n.l(o);
    },
    m(o, s) {
      n && n.m(o, s), t = !0;
    },
    p(o, s) {
      n && n.p && (!t || s & /*$$scope*/
      262144) && tt(
        n,
        r,
        o,
        /*$$scope*/
        o[18],
        t ? Xe(
          r,
          /*$$scope*/
          o[18],
          s,
          null
        ) : Qe(
          /*$$scope*/
          o[18]
        ),
        null
      );
    },
    i(o) {
      t || (j(n, o), t = !0);
    },
    o(o) {
      L(n, o), t = !1;
    },
    d(o) {
      n && n.d(o);
    }
  };
}
function nt(e) {
  let t, r, n = (
    /*$mergedProps*/
    e[0].visible && Y(e)
  );
  return {
    c() {
      n && n.c(), t = J();
    },
    l(o) {
      n && n.l(o), t = J();
    },
    m(o, s) {
      n && n.m(o, s), $e(o, t, s), r = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[0].visible ? n ? (n.p(o, s), s & /*$mergedProps*/
      1 && j(n, 1)) : (n = Y(o), n.c(), j(n, 1), n.m(t.parentNode, t)) : n && (Ze(), L(n, 1, 1, () => {
        n = null;
      }), He());
    },
    i(o) {
      r || (j(n), r = !0);
    },
    o(o) {
      L(n), r = !1;
    },
    d(o) {
      o && Je(t), n && n.d(o);
    }
  };
}
function rt(e, t, r) {
  const n = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = B(t, n), s, i, l, u, f, {
    $$slots: d = {},
    $$scope: p
  } = t, {
    gradio: m
  } = t, {
    props: g = {}
  } = t;
  const c = y(g);
  S(e, c, (a) => r(17, f = a));
  let {
    _internal: _ = {}
  } = t, {
    as_item: b
  } = t, {
    visible: h = !0
  } = t, {
    elem_id: C = ""
  } = t, {
    elem_classes: R = []
  } = t, {
    elem_style: O = {}
  } = t;
  const A = Z();
  S(e, A, (a) => r(16, u = a));
  const [M, re] = we({
    gradio: m,
    props: f,
    _internal: _,
    visible: h,
    elem_id: C,
    elem_classes: R,
    elem_style: O,
    as_item: b,
    restProps: o
  });
  S(e, M, (a) => r(0, i = a));
  const q = Ce(), W = ye();
  S(e, W, (a) => r(14, s = a));
  const {
    selections: z
  } = De(["selections"]);
  S(e, z, (a) => r(15, l = a));
  const se = Ue();
  return e.$$set = (a) => {
    t = H(H({}, t), Ye(a)), r(23, o = B(t, n)), "gradio" in a && r(6, m = a.gradio), "props" in a && r(7, g = a.props), "_internal" in a && r(8, _ = a._internal), "as_item" in a && r(9, b = a.as_item), "visible" in a && r(10, h = a.visible), "elem_id" in a && r(11, C = a.elem_id), "elem_classes" in a && r(12, R = a.elem_classes), "elem_style" in a && r(13, O = a.elem_style), "$$scope" in a && r(18, p = a.$$scope);
  }, e.$$.update = () => {
    if (e.$$.dirty & /*props*/
    128 && c.update((a) => ({
      ...a,
      ...g
    })), re({
      gradio: m,
      props: f,
      _internal: _,
      visible: h,
      elem_id: C,
      elem_classes: R,
      elem_style: O,
      as_item: b,
      restProps: o
    }), e.$$.dirty & /*$mergedProps, $slotKey, $selectionsItems, $slots*/
    114689) {
      const a = ie(i);
      se(u, i._internal.index || 0, {
        props: {
          style: i.elem_style,
          className: qe(i.elem_classes, "ms-gr-antd-table-row-selection"),
          id: i.elem_id,
          ...i.restProps,
          ...i.props,
          ...a,
          selections: i.props.selections || i.restProps.selections || ee(l),
          onCell: N(i.props.onCell || i.restProps.onCell),
          getCheckboxProps: N(i.props.getCheckboxProps || i.restProps.getCheckboxProps),
          renderCell: N(i.props.renderCell || i.restProps.renderCell),
          columnTitle: i.props.columnTitle || i.restProps.columnTitle
        },
        slots: {
          ...s,
          columnTitle: {
            el: s.columnTitle,
            callback: q,
            clone: !0
          },
          renderCell: {
            el: s.renderCell,
            callback: q,
            clone: !0
          }
        }
      });
    }
  }, [i, c, A, M, W, z, m, g, _, b, h, C, R, O, s, l, u, f, p, d];
}
class ct extends Ge {
  constructor(t) {
    super(), Ve(this, t, rt, nt, et, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      visible: 10,
      elem_id: 11,
      elem_classes: 12,
      elem_style: 13
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), x();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), x();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), x();
  }
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), x();
  }
  get visible() {
    return this.$$.ctx[10];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), x();
  }
  get elem_id() {
    return this.$$.ctx[11];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), x();
  }
  get elem_classes() {
    return this.$$.ctx[12];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), x();
  }
  get elem_style() {
    return this.$$.ctx[13];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), x();
  }
}
export {
  ct as default
};
