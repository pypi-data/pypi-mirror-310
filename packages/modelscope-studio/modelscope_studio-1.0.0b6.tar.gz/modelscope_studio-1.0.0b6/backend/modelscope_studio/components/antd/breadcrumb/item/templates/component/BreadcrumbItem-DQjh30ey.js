import { g as Fe, b as Ne } from "./Index-BtAfKt7K.js";
const I = window.ms_globals.React, Ke = window.ms_globals.React.forwardRef, Le = window.ms_globals.React.useRef, Ae = window.ms_globals.React.useState, Me = window.ms_globals.React.useEffect, qe = window.ms_globals.ReactDOM.createPortal;
function Be(t) {
  return t === void 0;
}
function k() {
}
function Te(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function We(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return k;
  }
  const r = t.subscribe(...e);
  return r.unsubscribe ? () => r.unsubscribe() : r;
}
function x(t) {
  let e;
  return We(t, (r) => e = r)(), e;
}
const C = [];
function y(t, e = k) {
  let r;
  const n = /* @__PURE__ */ new Set();
  function o(l) {
    if (Te(t, l) && (t = l, r)) {
      const u = !C.length;
      for (const f of n)
        f[1](), C.push(f, t);
      if (u) {
        for (let f = 0; f < C.length; f += 2)
          C[f][0](C[f + 1]);
        C.length = 0;
      }
    }
  }
  function s(l) {
    o(l(t));
  }
  function i(l, u = k) {
    const f = [l, u];
    return n.add(f), n.size === 1 && (r = e(o, s) || k), l(t), () => {
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
  getContext: ze,
  setContext: Nt
} = window.__gradio__svelte__internal, De = "$$ms-gr-loading-status-key";
function Ue() {
  const t = window.ms_globals.loadingKey++, e = ze(De);
  return (r) => {
    if (!e || !r)
      return;
    const {
      loadingStatusMap: n,
      options: o
    } = e, {
      generating: s,
      error: i
    } = x(o);
    (r == null ? void 0 : r.status) === "pending" || i && (r == null ? void 0 : r.status) === "error" || (s && (r == null ? void 0 : r.status)) === "generating" ? n.update(({
      map: l
    }) => (l.set(t, r), {
      map: l
    })) : n.update(({
      map: l
    }) => (l.delete(t), {
      map: l
    }));
  };
}
const {
  getContext: D,
  setContext: R
} = window.__gradio__svelte__internal, Ge = "$$ms-gr-slots-key";
function He() {
  const t = y({});
  return R(Ge, t);
}
const Je = "$$ms-gr-render-slot-context-key";
function Ye() {
  const t = R(Je, y({}));
  return (e, r) => {
    t.update((n) => typeof r == "function" ? {
      ...n,
      [e]: r(n[e])
    } : {
      ...n,
      [e]: r
    });
  };
}
const Qe = "$$ms-gr-context-key";
function L(t) {
  return Be(t) ? {} : typeof t == "object" && !Array.isArray(t) ? t : {
    value: t
  };
}
const Ie = "$$ms-gr-sub-index-context-key";
function Xe() {
  return D(Ie) || null;
}
function he(t) {
  return R(Ie, t);
}
function Ze(t, e, r) {
  var m, _;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const n = Ee(), o = et({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  }), s = Xe();
  typeof s == "number" && he(void 0);
  const i = Ue();
  typeof t._internal.subIndex == "number" && he(t._internal.subIndex), n && n.subscribe((c) => {
    o.slotKey.set(c);
  }), Ve();
  const l = D(Qe), u = ((m = x(l)) == null ? void 0 : m.as_item) || t.as_item, f = L(l ? u ? ((_ = x(l)) == null ? void 0 : _[u]) || {} : x(l) || {} : {}), d = (c, p) => c ? Fe({
    ...c,
    ...p || {}
  }, e) : void 0, g = y({
    ...t,
    _internal: {
      ...t._internal,
      index: s ?? t._internal.index
    },
    ...f,
    restProps: d(t.restProps, f),
    originalRestProps: t.restProps
  });
  return l ? (l.subscribe((c) => {
    const {
      as_item: p
    } = x(g);
    p && (c = c == null ? void 0 : c[p]), c = L(c), g.update((b) => ({
      ...b,
      ...c || {},
      restProps: d(b.restProps, c)
    }));
  }), [g, (c) => {
    var b, h;
    const p = L(c.as_item ? ((b = x(l)) == null ? void 0 : b[c.as_item]) || {} : x(l) || {});
    return i((h = c.restProps) == null ? void 0 : h.loading_status), g.set({
      ...c,
      _internal: {
        ...c._internal,
        index: s ?? c._internal.index
      },
      ...p,
      restProps: d(c.restProps, p),
      originalRestProps: c.restProps
    });
  }]) : [g, (c) => {
    var p;
    i((p = c.restProps) == null ? void 0 : p.loading_status), g.set({
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
const Ce = "$$ms-gr-slot-key";
function Ve() {
  R(Ce, y(void 0));
}
function Ee() {
  return D(Ce);
}
const $e = "$$ms-gr-component-slot-context-key";
function et({
  slot: t,
  index: e,
  subIndex: r
}) {
  return R($e, {
    slotKey: y(t),
    slotIndex: y(e),
    subSlotIndex: y(r)
  });
}
function tt(t) {
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
function nt(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var Re = {
  exports: {}
}, N = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var rt = I, st = Symbol.for("react.element"), ot = Symbol.for("react.fragment"), it = Object.prototype.hasOwnProperty, lt = rt.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ct = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Se(t, e, r) {
  var n, o = {}, s = null, i = null;
  r !== void 0 && (s = "" + r), e.key !== void 0 && (s = "" + e.key), e.ref !== void 0 && (i = e.ref);
  for (n in e) it.call(e, n) && !ct.hasOwnProperty(n) && (o[n] = e[n]);
  if (t && t.defaultProps) for (n in e = t.defaultProps, e) o[n] === void 0 && (o[n] = e[n]);
  return {
    $$typeof: st,
    type: t,
    key: s,
    ref: i,
    props: o,
    _owner: lt.current
  };
}
N.Fragment = ot;
N.jsx = Se;
N.jsxs = Se;
Re.exports = N;
var M = Re.exports;
const ut = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function dt(t) {
  return t ? Object.keys(t).reduce((e, r) => {
    const n = t[r];
    return typeof n == "number" && !ut.includes(r) ? e[r] = n + "px" : e[r] = n, e;
  }, {}) : {};
}
function q(t) {
  const e = [], r = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(qe(I.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: I.Children.toArray(t._reactElement.props.children).map((o) => {
        if (I.isValidElement(o) && o.props.__slot__) {
          const {
            portals: s,
            clonedElement: i
          } = q(o.props.el);
          return I.cloneElement(o, {
            ...o.props,
            el: i,
            children: [...I.Children.toArray(o.props.children), ...s]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: e
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: i,
      type: l,
      useCapture: u
    }) => {
      r.addEventListener(l, i, u);
    });
  });
  const n = Array.from(t.childNodes);
  for (let o = 0; o < n.length; o++) {
    const s = n[o];
    if (s.nodeType === 1) {
      const {
        clonedElement: i,
        portals: l
      } = q(s);
      e.push(...l), r.appendChild(i);
    } else s.nodeType === 3 && r.appendChild(s.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function at(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const B = Ke(({
  slot: t,
  clone: e,
  className: r,
  style: n
}, o) => {
  const s = Le(), [i, l] = Ae([]);
  return Me(() => {
    var g;
    if (!s.current || !t)
      return;
    let u = t;
    function f() {
      let m = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (m = u.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), at(o, m), r && m.classList.add(...r.split(" ")), n) {
        const _ = dt(n);
        Object.keys(_).forEach((c) => {
          m.style[c] = _[c];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let m = function() {
        var b, h, w;
        (b = s.current) != null && b.contains(u) && ((h = s.current) == null || h.removeChild(u));
        const {
          portals: c,
          clonedElement: p
        } = q(t);
        return u = p, l(c), u.style.display = "contents", f(), (w = s.current) == null || w.appendChild(u), c.length > 0;
      };
      m() || (d = new window.MutationObserver(() => {
        m() && (d == null || d.disconnect());
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      u.style.display = "contents", f(), (g = s.current) == null || g.appendChild(u);
    return () => {
      var m, _;
      u.style.display = "", (m = s.current) != null && m.contains(u) && ((_ = s.current) == null || _.removeChild(u)), d == null || d.disconnect();
    };
  }, [t, e, r, n, o]), I.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...i);
});
function T(t, e, r) {
  return t.filter(Boolean).map((n, o) => {
    var u;
    if (typeof n != "object")
      return e != null && e.fallback ? e.fallback(n) : n;
    const s = {
      ...n.props,
      key: ((u = n.props) == null ? void 0 : u.key) ?? (r ? `${r}-${o}` : `${o}`)
    };
    let i = s;
    Object.keys(n.slots).forEach((f) => {
      if (!n.slots[f] || !(n.slots[f] instanceof Element) && !n.slots[f].el)
        return;
      const d = f.split(".");
      d.forEach((p, b) => {
        i[p] || (i[p] = {}), b !== d.length - 1 && (i = s[p]);
      });
      const g = n.slots[f];
      let m, _, c = (e == null ? void 0 : e.clone) ?? !1;
      g instanceof Element ? m = g : (m = g.el, _ = g.callback, c = g.clone ?? !1), i[d[d.length - 1]] = m ? _ ? (...p) => (_(d[d.length - 1], p), /* @__PURE__ */ M.jsx(B, {
        slot: m,
        clone: c
      })) : /* @__PURE__ */ M.jsx(B, {
        slot: m,
        clone: c
      }) : i[d[d.length - 1]], i = s;
    });
    const l = (e == null ? void 0 : e.children) || "children";
    return n[l] && (s[l] = T(n[l], e, `${o}`)), s;
  });
}
function W(t, e) {
  return t ? /* @__PURE__ */ M.jsx(B, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function A({
  key: t,
  setSlotParams: e,
  slots: r
}, n) {
  return r[t] ? (...o) => (e(t, o), W(r[t], {
    clone: !0,
    ...n
  })) : void 0;
}
var Oe = {
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
        e.call(s, l) && s[l] && (i = o(i, l));
      return i;
    }
    function o(s, i) {
      return i ? s ? s + " " + i : s + i : s;
    }
    t.exports ? (r.default = r, t.exports = r) : window.classNames = r;
  })();
})(Oe);
var ft = Oe.exports;
const mt = /* @__PURE__ */ nt(ft), {
  getContext: pt,
  setContext: _t
} = window.__gradio__svelte__internal;
function ve(t) {
  const e = `$$ms-gr-${t}-context-key`;
  function r(o = ["default"]) {
    const s = o.reduce((i, l) => (i[l] = y([]), i), {});
    return _t(e, {
      itemsMap: s,
      allowedSlots: o
    }), s;
  }
  function n() {
    const {
      itemsMap: o,
      allowedSlots: s
    } = pt(e);
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
  getItems: gt,
  getSetItemFn: Kt
} = ve("menu"), {
  getItems: Lt,
  getSetItemFn: bt
} = ve("breadcrumb"), {
  SvelteComponent: ht,
  assign: ye,
  check_outros: yt,
  component_subscribe: E,
  compute_rest_props: Pe,
  create_slot: Pt,
  detach: wt,
  empty: we,
  exclude_internal_props: xt,
  flush: P,
  get_all_dirty_from_scope: It,
  get_slot_changes: Ct,
  group_outros: Et,
  init: Rt,
  insert_hydration: St,
  safe_not_equal: Ot,
  transition_in: F,
  transition_out: z,
  update_slot_base: vt
} = window.__gradio__svelte__internal;
function xe(t) {
  let e;
  const r = (
    /*#slots*/
    t[21].default
  ), n = Pt(
    r,
    t,
    /*$$scope*/
    t[20],
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
      n && n.m(o, s), e = !0;
    },
    p(o, s) {
      n && n.p && (!e || s & /*$$scope*/
      1048576) && vt(
        n,
        r,
        o,
        /*$$scope*/
        o[20],
        e ? Ct(
          r,
          /*$$scope*/
          o[20],
          s,
          null
        ) : It(
          /*$$scope*/
          o[20]
        ),
        null
      );
    },
    i(o) {
      e || (F(n, o), e = !0);
    },
    o(o) {
      z(n, o), e = !1;
    },
    d(o) {
      n && n.d(o);
    }
  };
}
function jt(t) {
  let e, r, n = (
    /*$mergedProps*/
    t[0].visible && xe(t)
  );
  return {
    c() {
      n && n.c(), e = we();
    },
    l(o) {
      n && n.l(o), e = we();
    },
    m(o, s) {
      n && n.m(o, s), St(o, e, s), r = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[0].visible ? n ? (n.p(o, s), s & /*$mergedProps*/
      1 && F(n, 1)) : (n = xe(o), n.c(), F(n, 1), n.m(e.parentNode, e)) : n && (Et(), z(n, 1, 1, () => {
        n = null;
      }), yt());
    },
    i(o) {
      r || (F(n), r = !0);
    },
    o(o) {
      z(n), r = !1;
    },
    d(o) {
      o && wt(e), n && n.d(o);
    }
  };
}
function kt(t, e, r) {
  const n = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = Pe(e, n), s, i, l, u, f, d, {
    $$slots: g = {},
    $$scope: m
  } = e, {
    gradio: _
  } = e, {
    props: c = {}
  } = e;
  const p = y(c);
  E(t, p, (a) => r(19, d = a));
  let {
    _internal: b = {}
  } = e, {
    as_item: h
  } = e, {
    visible: w = !0
  } = e, {
    elem_id: S = ""
  } = e, {
    elem_classes: O = []
  } = e, {
    elem_style: v = {}
  } = e;
  const U = Ee();
  E(t, U, (a) => r(16, l = a));
  const [G, je] = Ze({
    gradio: _,
    props: d,
    _internal: b,
    visible: w,
    elem_id: S,
    elem_classes: O,
    elem_style: v,
    as_item: h,
    restProps: o
  });
  E(t, G, (a) => r(0, i = a));
  const H = He();
  E(t, H, (a) => r(15, s = a));
  const ke = bt(), K = Ye(), {
    "menu.items": J,
    "dropdownProps.menu.items": Y
  } = gt(["menu.items", "dropdownProps.menu.items"]);
  return E(t, J, (a) => r(18, f = a)), E(t, Y, (a) => r(17, u = a)), t.$$set = (a) => {
    e = ye(ye({}, e), xt(a)), r(25, o = Pe(e, n)), "gradio" in a && r(7, _ = a.gradio), "props" in a && r(8, c = a.props), "_internal" in a && r(9, b = a._internal), "as_item" in a && r(10, h = a.as_item), "visible" in a && r(11, w = a.visible), "elem_id" in a && r(12, S = a.elem_id), "elem_classes" in a && r(13, O = a.elem_classes), "elem_style" in a && r(14, v = a.elem_style), "$$scope" in a && r(20, m = a.$$scope);
  }, t.$$.update = () => {
    var a, Q, X, Z, V, $, ee, te, ne, re, se, oe, ie, le, ce, ue, de, ae, fe, me, pe, _e;
    if (t.$$.dirty & /*props*/
    256 && p.update((j) => ({
      ...j,
      ...c
    })), je({
      gradio: _,
      props: d,
      _internal: b,
      visible: w,
      elem_id: S,
      elem_classes: O,
      elem_style: v,
      as_item: h,
      restProps: o
    }), t.$$.dirty & /*$mergedProps, $menuItems, $slots, $dropdownMenuItems, $slotKey*/
    491521) {
      const j = {
        ...i.restProps.menu || {},
        ...i.props.menu || {},
        items: (a = i.props.menu) != null && a.items || (Q = i.restProps.menu) != null && Q.items || f.length > 0 ? T(f, {
          clone: !0
        }) : void 0,
        expandIcon: A({
          setSlotParams: K,
          slots: s,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) || ((X = i.props.menu) == null ? void 0 : X.expandIcon) || ((Z = i.restProps.menu) == null ? void 0 : Z.expandIcon),
        overflowedIndicator: W(s["menu.overflowedIndicator"]) || ((V = i.props.menu) == null ? void 0 : V.overflowedIndicator) || (($ = i.restProps.menu) == null ? void 0 : $.overflowedIndicator)
      }, ge = {
        ...((ee = i.restProps.dropdownProps) == null ? void 0 : ee.menu) || {},
        ...((te = i.props.dropdownProps) == null ? void 0 : te.menu) || {},
        items: (re = (ne = i.props.dropdownProps) == null ? void 0 : ne.menu) != null && re.items || (oe = (se = i.restProps.dropdownProps) == null ? void 0 : se.menu) != null && oe.items || u.length > 0 ? T(u, {
          clone: !0
        }) : void 0,
        expandIcon: A({
          setSlotParams: K,
          slots: s,
          key: "dropdownProps.menu.expandIcon"
        }, {
          clone: !0
        }) || ((le = (ie = i.props.dropdownProps) == null ? void 0 : ie.menu) == null ? void 0 : le.expandIcon) || ((ue = (ce = i.restProps.dropdownProps) == null ? void 0 : ce.menu) == null ? void 0 : ue.expandIcon),
        overflowedIndicator: W(s["dropdownProps.menu.overflowedIndicator"]) || ((ae = (de = i.props.dropdownProps) == null ? void 0 : de.menu) == null ? void 0 : ae.overflowedIndicator) || ((me = (fe = i.restProps.dropdownProps) == null ? void 0 : fe.menu) == null ? void 0 : me.overflowedIndicator)
      }, be = {
        ...i.restProps.dropdownProps || {},
        ...i.props.dropdownProps || {},
        dropdownRender: s["dropdownProps.dropdownRender"] ? A({
          setSlotParams: K,
          slots: s,
          key: "dropdownProps.dropdownRender"
        }, {
          clone: !0
        }) : tt(((pe = i.props.dropdownProps) == null ? void 0 : pe.dropdownRender) || ((_e = i.restProps.dropdownProps) == null ? void 0 : _e.dropdownRender)),
        menu: Object.values(ge).filter(Boolean).length > 0 ? ge : void 0
      };
      ke(l, i._internal.index || 0, {
        props: {
          style: i.elem_style,
          className: mt(i.elem_classes, "ms-gr-antd-breadcrumb-item"),
          id: i.elem_id,
          ...i.restProps,
          ...i.props,
          ...Ne(i),
          menu: Object.values(j).filter(Boolean).length > 0 ? j : void 0,
          dropdownProps: Object.values(be).filter(Boolean).length > 0 ? be : void 0
        },
        slots: {
          title: s.title
        }
      });
    }
  }, [i, p, U, G, H, J, Y, _, c, b, h, w, S, O, v, s, l, u, f, d, m, g];
}
class At extends ht {
  constructor(e) {
    super(), Rt(this, e, kt, jt, Ot, {
      gradio: 7,
      props: 8,
      _internal: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), P();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), P();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), P();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), P();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), P();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), P();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), P();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), P();
  }
}
export {
  At as default
};
