import { g as le, w as L } from "./Index-BtO7Mt20.js";
const E = window.ms_globals.React, te = window.ms_globals.React.forwardRef, ne = window.ms_globals.React.useRef, re = window.ms_globals.React.useState, oe = window.ms_globals.React.useEffect, V = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, A = window.ms_globals.antd.Tree;
var J = {
  exports: {}
}, S = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var se = E, ce = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ae = Object.prototype.hasOwnProperty, ue = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, de = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Y(t, e, o) {
  var r, l = {}, n = null, s = null;
  o !== void 0 && (n = "" + o), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (r in e) ae.call(e, r) && !de.hasOwnProperty(r) && (l[r] = e[r]);
  if (t && t.defaultProps) for (r in e = t.defaultProps, e) l[r] === void 0 && (l[r] = e[r]);
  return {
    $$typeof: ce,
    type: t,
    key: n,
    ref: s,
    props: l,
    _owner: ue.current
  };
}
S.Fragment = ie;
S.jsx = Y;
S.jsxs = Y;
J.exports = S;
var w = J.exports;
const {
  SvelteComponent: fe,
  assign: W,
  binding_callbacks: M,
  check_outros: _e,
  children: K,
  claim_element: Q,
  claim_space: he,
  component_subscribe: U,
  compute_slots: me,
  create_slot: ge,
  detach: v,
  element: X,
  empty: z,
  exclude_internal_props: G,
  get_all_dirty_from_scope: pe,
  get_slot_changes: we,
  group_outros: be,
  init: ye,
  insert_hydration: k,
  safe_not_equal: Ee,
  set_custom_element_data: Z,
  space: ve,
  transition_in: j,
  transition_out: N,
  update_slot_base: Ie
} = window.__gradio__svelte__internal, {
  beforeUpdate: Re,
  getContext: Ce,
  onDestroy: xe,
  setContext: Oe
} = window.__gradio__svelte__internal;
function H(t) {
  let e, o;
  const r = (
    /*#slots*/
    t[7].default
  ), l = ge(
    r,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = X("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      e = Q(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = K(e);
      l && l.l(s), s.forEach(v), this.h();
    },
    h() {
      Z(e, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      k(n, e, s), l && l.m(e, null), t[9](e), o = !0;
    },
    p(n, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && Ie(
        l,
        r,
        n,
        /*$$scope*/
        n[6],
        o ? we(
          r,
          /*$$scope*/
          n[6],
          s,
          null
        ) : pe(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (j(l, n), o = !0);
    },
    o(n) {
      N(l, n), o = !1;
    },
    d(n) {
      n && v(e), l && l.d(n), t[9](null);
    }
  };
}
function Le(t) {
  let e, o, r, l, n = (
    /*$$slots*/
    t[4].default && H(t)
  );
  return {
    c() {
      e = X("react-portal-target"), o = ve(), n && n.c(), r = z(), this.h();
    },
    l(s) {
      e = Q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(e).forEach(v), o = he(s), n && n.l(s), r = z(), this.h();
    },
    h() {
      Z(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      k(s, e, c), t[8](e), k(s, o, c), n && n.m(s, c), k(s, r, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, c), c & /*$$slots*/
      16 && j(n, 1)) : (n = H(s), n.c(), j(n, 1), n.m(r.parentNode, r)) : n && (be(), N(n, 1, 1, () => {
        n = null;
      }), _e());
    },
    i(s) {
      l || (j(n), l = !0);
    },
    o(s) {
      N(n), l = !1;
    },
    d(s) {
      s && (v(e), v(o), v(r)), t[8](null), n && n.d(s);
    }
  };
}
function q(t) {
  const {
    svelteInit: e,
    ...o
  } = t;
  return o;
}
function ke(t, e, o) {
  let r, l, {
    $$slots: n = {},
    $$scope: s
  } = e;
  const c = me(n);
  let {
    svelteInit: i
  } = e;
  const m = L(q(e)), u = L();
  U(t, u, (d) => o(0, r = d));
  const f = L();
  U(t, f, (d) => o(1, l = d));
  const a = [], h = Ce("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: g,
    subSlotIndex: p
  } = le() || {}, y = i({
    parent: h,
    props: m,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: g,
    subSlotIndex: p,
    onDestroy(d) {
      a.push(d);
    }
  });
  Oe("$$ms-gr-react-wrapper", y), Re(() => {
    m.set(q(e));
  }), xe(() => {
    a.forEach((d) => d());
  });
  function b(d) {
    M[d ? "unshift" : "push"](() => {
      r = d, u.set(r);
    });
  }
  function T(d) {
    M[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  return t.$$set = (d) => {
    o(17, e = W(W({}, e), G(d))), "svelteInit" in d && o(5, i = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, e = G(e), [r, l, u, f, c, i, s, n, b, T];
}
class je extends fe {
  constructor(e) {
    super(), ye(this, e, ke, Le, Ee, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, P = window.ms_globals.tree;
function Se(t) {
  function e(o) {
    const r = L(), l = new je({
      ...o,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            slotKey: n.slotKey,
            nodes: []
          }, c = n.parent ?? P;
          return c.nodes = [...c.nodes, s], B({
            createPortal: F,
            node: P
          }), n.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== r), B({
              createPortal: F,
              node: P
            });
          }), s;
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
const Te = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(t) {
  return t ? Object.keys(t).reduce((e, o) => {
    const r = t[o];
    return typeof r == "number" && !Te.includes(o) ? e[o] = r + "px" : e[o] = r, e;
  }, {}) : {};
}
function D(t) {
  const e = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(F(E.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: E.Children.toArray(t._reactElement.props.children).map((l) => {
        if (E.isValidElement(l) && l.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = D(l.props.el);
          return E.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...E.Children.toArray(l.props.children), ...n]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: e
    };
  Object.keys(t.getEventListeners()).forEach((l) => {
    t.getEventListeners(l).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      o.addEventListener(c, s, i);
    });
  });
  const r = Array.from(t.childNodes);
  for (let l = 0; l < r.length; l++) {
    const n = r[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = D(n);
      e.push(...c), o.appendChild(s);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function Fe(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const x = te(({
  slot: t,
  clone: e,
  className: o,
  style: r
}, l) => {
  const n = ne(), [s, c] = re([]);
  return oe(() => {
    var f;
    if (!n.current || !t)
      return;
    let i = t;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Fe(l, a), o && a.classList.add(...o.split(" ")), r) {
        const h = Pe(r);
        Object.keys(h).forEach((_) => {
          a.style[_] = h[_];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var p, y, b;
        (p = n.current) != null && p.contains(i) && ((y = n.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: g
        } = D(t);
        return i = g, c(_), i.style.display = "contents", m(), (b = n.current) == null || b.appendChild(i), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", m(), (f = n.current) == null || f.appendChild(i);
    return () => {
      var a, h;
      i.style.display = "", (a = n.current) != null && a.contains(i) && ((h = n.current) == null || h.removeChild(i)), u == null || u.disconnect();
    };
  }, [t, e, o, r, l]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ne(t) {
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
function C(t) {
  return V(() => Ne(t), [t]);
}
function De(t) {
  return Object.keys(t).reduce((e, o) => (t[o] !== void 0 && (e[o] = t[o]), e), {});
}
function $(t, e, o) {
  return t.filter(Boolean).map((r, l) => {
    var i;
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const n = {
      ...r.props,
      key: ((i = r.props) == null ? void 0 : i.key) ?? (o ? `${o}-${l}` : `${l}`)
    };
    let s = n;
    Object.keys(r.slots).forEach((m) => {
      if (!r.slots[m] || !(r.slots[m] instanceof Element) && !r.slots[m].el)
        return;
      const u = m.split(".");
      u.forEach((g, p) => {
        s[g] || (s[g] = {}), p !== u.length - 1 && (s = n[g]);
      });
      const f = r.slots[m];
      let a, h, _ = (e == null ? void 0 : e.clone) ?? !1;
      f instanceof Element ? a = f : (a = f.el, h = f.callback, _ = f.clone ?? !1), s[u[u.length - 1]] = a ? h ? (...g) => (h(u[u.length - 1], g), /* @__PURE__ */ w.jsx(x, {
        slot: a,
        clone: _
      })) : /* @__PURE__ */ w.jsx(x, {
        slot: a,
        clone: _
      }) : s[u[u.length - 1]], s = n;
    });
    const c = (e == null ? void 0 : e.children) || "children";
    return r[c] && (n[c] = $(r[c], e, `${l}`)), n;
  });
}
function Ae(t, e) {
  return t ? /* @__PURE__ */ w.jsx(x, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function O({
  key: t,
  setSlotParams: e,
  slots: o
}, r) {
  return o[t] ? (...l) => (e(t, l), Ae(o[t], {
    clone: !0,
    ...r
  })) : void 0;
}
const Me = Se(({
  slots: t,
  filterTreeNode: e,
  treeData: o,
  draggable: r,
  allowDrop: l,
  onCheck: n,
  onSelect: s,
  onExpand: c,
  children: i,
  directory: m,
  slotItems: u,
  setSlotParams: f,
  onLoadData: a,
  titleRender: h,
  ..._
}) => {
  const g = C(e), p = C(r), y = C(h), b = C(typeof r == "object" ? r.nodeDraggable : void 0), T = C(l), d = m ? A.DirectoryTree : A, ee = V(() => ({
    ..._,
    treeData: o || $(u, {
      clone: !0
    }),
    showLine: t["showLine.showLeafIcon"] ? {
      showLeafIcon: O({
        slots: t,
        setSlotParams: f,
        key: "showLine.showLeafIcon"
      })
    } : _.showLine,
    icon: t.icon ? O({
      slots: t,
      setSlotParams: f,
      key: "icon"
    }) : _.icon,
    switcherLoadingIcon: t.switcherLoadingIcon ? /* @__PURE__ */ w.jsx(x, {
      slot: t.switcherLoadingIcon
    }) : _.switcherLoadingIcon,
    switcherIcon: t.switcherIcon ? O({
      slots: t,
      setSlotParams: f,
      key: "switcherIcon"
    }) : _.switcherIcon,
    titleRender: t.titleRender ? O({
      slots: t,
      setSlotParams: f,
      key: "titleRender"
    }) : y,
    draggable: t["draggable.icon"] || b ? {
      icon: t["draggable.icon"] ? /* @__PURE__ */ w.jsx(x, {
        slot: t["draggable.icon"]
      }) : typeof r == "object" ? r.icon : void 0,
      nodeDraggable: b
    } : p || r,
    loadData: a
  }), [_, o, u, t, f, b, r, y, p, a]);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: i
    }), /* @__PURE__ */ w.jsx(d, {
      ...De(ee),
      filterTreeNode: g,
      allowDrop: T,
      onSelect: (I, ...R) => {
        s == null || s(I, ...R);
      },
      onExpand: (I, ...R) => {
        c == null || c(I, ...R);
      },
      onCheck: (I, ...R) => {
        n == null || n(I, ...R);
      }
    })]
  });
});
export {
  Me as Tree,
  Me as default
};
