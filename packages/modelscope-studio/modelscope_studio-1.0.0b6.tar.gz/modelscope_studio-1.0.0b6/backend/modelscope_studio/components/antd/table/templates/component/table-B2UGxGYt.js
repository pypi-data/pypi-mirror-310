import { g as Oe, w as I } from "./Index-jigI5IvI.js";
const E = window.ms_globals.React, Ce = window.ms_globals.React.forwardRef, be = window.ms_globals.React.useRef, Ee = window.ms_globals.React.useState, ye = window.ms_globals.React.useEffect, L = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, k = window.ms_globals.antd.Table;
var Z = {
  exports: {}
}, M = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ve = E, Se = Symbol.for("react.element"), Re = Symbol.for("react.fragment"), ke = Object.prototype.hasOwnProperty, xe = ve.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $(n, e, o) {
  var r, l = {}, t = null, i = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (i = e.ref);
  for (r in e) ke.call(e, r) && !Ne.hasOwnProperty(r) && (l[r] = e[r]);
  if (n && n.defaultProps) for (r in e = n.defaultProps, e) l[r] === void 0 && (l[r] = e[r]);
  return {
    $$typeof: Se,
    type: n,
    key: t,
    ref: i,
    props: l,
    _owner: xe.current
  };
}
M.Fragment = Re;
M.jsx = $;
M.jsxs = $;
Z.exports = M;
var w = Z.exports;
const {
  SvelteComponent: Pe,
  assign: H,
  binding_callbacks: Q,
  check_outros: Te,
  children: ee,
  claim_element: te,
  claim_space: Le,
  component_subscribe: z,
  compute_slots: Ie,
  create_slot: je,
  detach: R,
  element: ne,
  empty: X,
  exclude_internal_props: q,
  get_all_dirty_from_scope: Fe,
  get_slot_changes: Ae,
  group_outros: Me,
  init: Ue,
  insert_hydration: j,
  safe_not_equal: De,
  set_custom_element_data: re,
  space: We,
  transition_in: F,
  transition_out: B,
  update_slot_base: Be
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ge,
  getContext: Je,
  onDestroy: He,
  setContext: Qe
} = window.__gradio__svelte__internal;
function V(n) {
  let e, o;
  const r = (
    /*#slots*/
    n[7].default
  ), l = je(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = ne("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = te(t, "SVELTE-SLOT", {
        class: !0
      });
      var i = ee(e);
      l && l.l(i), i.forEach(R), this.h();
    },
    h() {
      re(e, "class", "svelte-1rt0kpf");
    },
    m(t, i) {
      j(t, e, i), l && l.m(e, null), n[9](e), o = !0;
    },
    p(t, i) {
      l && l.p && (!o || i & /*$$scope*/
      64) && Be(
        l,
        r,
        t,
        /*$$scope*/
        t[6],
        o ? Ae(
          r,
          /*$$scope*/
          t[6],
          i,
          null
        ) : Fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (F(l, t), o = !0);
    },
    o(t) {
      B(l, t), o = !1;
    },
    d(t) {
      t && R(e), l && l.d(t), n[9](null);
    }
  };
}
function ze(n) {
  let e, o, r, l, t = (
    /*$$slots*/
    n[4].default && V(n)
  );
  return {
    c() {
      e = ne("react-portal-target"), o = We(), t && t.c(), r = X(), this.h();
    },
    l(i) {
      e = te(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), ee(e).forEach(R), o = Le(i), t && t.l(i), r = X(), this.h();
    },
    h() {
      re(e, "class", "svelte-1rt0kpf");
    },
    m(i, c) {
      j(i, e, c), n[8](e), j(i, o, c), t && t.m(i, c), j(i, r, c), l = !0;
    },
    p(i, [c]) {
      /*$$slots*/
      i[4].default ? t ? (t.p(i, c), c & /*$$slots*/
      16 && F(t, 1)) : (t = V(i), t.c(), F(t, 1), t.m(r.parentNode, r)) : t && (Me(), B(t, 1, 1, () => {
        t = null;
      }), Te());
    },
    i(i) {
      l || (F(t), l = !0);
    },
    o(i) {
      B(t), l = !1;
    },
    d(i) {
      i && (R(e), R(o), R(r)), n[8](null), t && t.d(i);
    }
  };
}
function K(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function Xe(n, e, o) {
  let r, l, {
    $$slots: t = {},
    $$scope: i
  } = e;
  const c = Ie(t);
  let {
    svelteInit: s
  } = e;
  const g = I(K(e)), u = I();
  z(n, u, (d) => o(0, r = d));
  const f = I();
  z(n, f, (d) => o(1, l = d));
  const a = [], _ = Je("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: h,
    subSlotIndex: C
  } = Oe() || {}, O = s({
    parent: _,
    props: g,
    target: u,
    slot: f,
    slotKey: p,
    slotIndex: h,
    subSlotIndex: C,
    onDestroy(d) {
      a.push(d);
    }
  });
  Qe("$$ms-gr-react-wrapper", O), Ge(() => {
    g.set(K(e));
  }), He(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    Q[d ? "unshift" : "push"](() => {
      r = d, u.set(r);
    });
  }
  function S(d) {
    Q[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  return n.$$set = (d) => {
    o(17, e = H(H({}, e), q(d))), "svelteInit" in d && o(5, s = d.svelteInit), "$$scope" in d && o(6, i = d.$$scope);
  }, e = q(e), [r, l, u, f, c, s, i, t, v, S];
}
class qe extends Pe {
  constructor(e) {
    super(), Ue(this, e, Xe, ze, De, {
      svelteInit: 5
    });
  }
}
const Y = window.ms_globals.rerender, D = window.ms_globals.tree;
function Ve(n) {
  function e(o) {
    const r = I(), l = new qe({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? D;
          return c.nodes = [...c.nodes, i], Y({
            createPortal: W,
            node: D
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((s) => s.svelteInstance !== r), Y({
              createPortal: W,
              node: D
            });
          }), i;
        },
        ...o.props
      }
    });
    return r.set(l), l;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(e);
    });
  });
}
const Ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ye(n) {
  return n ? Object.keys(n).reduce((e, o) => {
    const r = n[o];
    return typeof r == "number" && !Ke.includes(o) ? e[o] = r + "px" : e[o] = r, e;
  }, {}) : {};
}
function G(n) {
  const e = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(W(E.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: E.Children.toArray(n._reactElement.props.children).map((l) => {
        if (E.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: i
          } = G(l.props.el);
          return E.cloneElement(l, {
            ...l.props,
            el: i,
            children: [...E.Children.toArray(l.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: i,
      type: c,
      useCapture: s
    }) => {
      o.addEventListener(c, i, s);
    });
  });
  const r = Array.from(n.childNodes);
  for (let l = 0; l < r.length; l++) {
    const t = r[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: i,
        portals: c
      } = G(t);
      e.push(...c), o.appendChild(i);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function Ze(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const y = Ce(({
  slot: n,
  clone: e,
  className: o,
  style: r
}, l) => {
  const t = be(), [i, c] = Ee([]);
  return ye(() => {
    var f;
    if (!t.current || !n)
      return;
    let s = n;
    function g() {
      let a = s;
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (a = s.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Ze(l, a), o && a.classList.add(...o.split(" ")), r) {
        const _ = Ye(r);
        Object.keys(_).forEach((p) => {
          a.style[p] = _[p];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var C, O, v;
        (C = t.current) != null && C.contains(s) && ((O = t.current) == null || O.removeChild(s));
        const {
          portals: p,
          clonedElement: h
        } = G(n);
        return s = h, c(p), s.style.display = "contents", g(), (v = t.current) == null || v.appendChild(s), p.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      s.style.display = "contents", g(), (f = t.current) == null || f.appendChild(s);
    return () => {
      var a, _;
      s.style.display = "", (a = t.current) != null && a.contains(s) && ((_ = t.current) == null || _.removeChild(s)), u == null || u.disconnect();
    };
  }, [n, e, o, r, l]), E.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...i);
});
function $e(n) {
  try {
    if (typeof n == "string") {
      let e = n.trim();
      return e.startsWith(";") && (e = e.slice(1)), e.endsWith(";") && (e = e.slice(0, -1)), new Function(`return (...args) => (${e})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function m(n) {
  return L(() => $e(n), [n]);
}
function et(n) {
  return Object.keys(n).reduce((e, o) => (n[o] !== void 0 && (e[o] = n[o]), e), {});
}
function A(n, e, o) {
  return n.filter(Boolean).map((r, l) => {
    var s;
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const t = {
      ...r.props,
      key: ((s = r.props) == null ? void 0 : s.key) ?? (o ? `${o}-${l}` : `${l}`)
    };
    let i = t;
    Object.keys(r.slots).forEach((g) => {
      if (!r.slots[g] || !(r.slots[g] instanceof Element) && !r.slots[g].el)
        return;
      const u = g.split(".");
      u.forEach((h, C) => {
        i[h] || (i[h] = {}), C !== u.length - 1 && (i = t[h]);
      });
      const f = r.slots[g];
      let a, _, p = (e == null ? void 0 : e.clone) ?? !1;
      f instanceof Element ? a = f : (a = f.el, _ = f.callback, p = f.clone ?? !1), i[u[u.length - 1]] = a ? _ ? (...h) => (_(u[u.length - 1], h), /* @__PURE__ */ w.jsx(y, {
        slot: a,
        clone: p
      })) : /* @__PURE__ */ w.jsx(y, {
        slot: a,
        clone: p
      }) : i[u[u.length - 1]], i = t;
    });
    const c = (e == null ? void 0 : e.children) || "children";
    return r[c] && (t[c] = A(r[c], e, `${l}`)), t;
  });
}
function tt(n, e) {
  return n ? /* @__PURE__ */ w.jsx(y, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function P({
  key: n,
  setSlotParams: e,
  slots: o
}, r) {
  return o[n] ? (...l) => (e(n, l), tt(o[n], {
    clone: !0,
    ...r
  })) : void 0;
}
function T(n) {
  return typeof n == "object" && n !== null ? n : {};
}
const rt = Ve(({
  children: n,
  slots: e,
  columnItems: o,
  columns: r,
  getPopupContainer: l,
  pagination: t,
  loading: i,
  rowKey: c,
  rowClassName: s,
  summary: g,
  rowSelection: u,
  rowSelectionItems: f,
  expandableItems: a,
  expandable: _,
  sticky: p,
  footer: h,
  showSorterTooltip: C,
  onRow: O,
  onHeaderRow: v,
  setSlotParams: S,
  ...d
}) => {
  const oe = m(l), le = e["loading.tip"] || e["loading.indicator"], U = T(i), ie = e["pagination.showQuickJumper.goButton"] || e["pagination.itemRender"], x = T(t), se = m(x.showTotal), ce = m(s), ae = m(c), ue = e["showSorterTooltip.title"] || typeof C == "object", N = T(C), de = m(N.afterOpenChange), fe = m(N.getPopupContainer), pe = typeof p == "object", J = T(p), _e = m(J.getContainer), ge = m(O), he = m(v), me = m(g), we = m(h);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ w.jsx(k, {
      ...d,
      columns: L(() => (r == null ? void 0 : r.map((b) => b === "EXPAND_COLUMN" ? k.EXPAND_COLUMN : b === "SELECTION_COLUMN" ? k.SELECTION_COLUMN : b)) || A(o, {
        fallback: (b) => b === "EXPAND_COLUMN" ? k.EXPAND_COLUMN : b === "SELECTION_COLUMN" ? k.SELECTION_COLUMN : b
      }), [o, r]),
      onRow: ge,
      onHeaderRow: he,
      summary: e.summary ? P({
        slots: e,
        setSlotParams: S,
        key: "summary"
      }) : me,
      rowSelection: L(() => u || A(f)[0], [u, f]),
      expandable: L(() => _ || A(a)[0], [_, a]),
      rowClassName: ce,
      rowKey: ae || c,
      sticky: pe ? {
        ...J,
        getContainer: _e
      } : p,
      showSorterTooltip: ue ? {
        ...N,
        afterOpenChange: de,
        getPopupContainer: fe,
        title: e["showSorterTooltip.title"] ? /* @__PURE__ */ w.jsx(y, {
          slot: e["showSorterTooltip.title"]
        }) : N.title
      } : C,
      pagination: ie ? et({
        ...x,
        showTotal: se,
        showQuickJumper: e["pagination.showQuickJumper.goButton"] ? {
          goButton: /* @__PURE__ */ w.jsx(y, {
            slot: e["pagination.showQuickJumper.goButton"]
          })
        } : x.showQuickJumper,
        itemRender: e["pagination.itemRender"] ? P({
          slots: e,
          setSlotParams: S,
          key: "pagination.itemRender"
        }) : x.itemRender
      }) : t,
      getPopupContainer: oe,
      loading: le ? {
        ...U,
        tip: e["loading.tip"] ? /* @__PURE__ */ w.jsx(y, {
          slot: e["loading.tip"]
        }) : U.tip,
        indicator: e["loading.indicator"] ? /* @__PURE__ */ w.jsx(y, {
          slot: e["loading.indicator"]
        }) : U.indicator
      } : i,
      footer: e.footer ? P({
        slots: e,
        setSlotParams: S,
        key: "footer"
      }) : we,
      title: e.title ? P({
        slots: e,
        setSlotParams: S,
        key: "title"
      }) : d.title
    })]
  });
});
export {
  rt as Table,
  rt as default
};
