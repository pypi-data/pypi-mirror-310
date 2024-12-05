import { g as te, w as x } from "./Index-D4t9z3b2.js";
const w = window.ms_globals.React, X = window.ms_globals.React.forwardRef, Z = window.ms_globals.React.useRef, $ = window.ms_globals.React.useState, ee = window.ms_globals.React.useEffect, U = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, ne = window.ms_globals.antd.Dropdown;
var H = {
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
var re = w, oe = Symbol.for("react.element"), le = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ce = re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ie = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function q(n, e, s) {
  var r, o = {}, t = null, l = null;
  s !== void 0 && (t = "" + s), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (r in e) se.call(e, r) && !ie.hasOwnProperty(r) && (o[r] = e[r]);
  if (n && n.defaultProps) for (r in e = n.defaultProps, e) o[r] === void 0 && (o[r] = e[r]);
  return {
    $$typeof: oe,
    type: n,
    key: t,
    ref: l,
    props: o,
    _owner: ce.current
  };
}
S.Fragment = le;
S.jsx = q;
S.jsxs = q;
H.exports = S;
var g = H.exports;
const {
  SvelteComponent: ae,
  assign: L,
  binding_callbacks: T,
  check_outros: de,
  children: B,
  claim_element: V,
  claim_space: ue,
  component_subscribe: N,
  compute_slots: fe,
  create_slot: _e,
  detach: y,
  element: J,
  empty: F,
  exclude_internal_props: A,
  get_all_dirty_from_scope: me,
  get_slot_changes: pe,
  group_outros: he,
  init: ge,
  insert_hydration: C,
  safe_not_equal: we,
  set_custom_element_data: Y,
  space: be,
  transition_in: I,
  transition_out: P,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ve,
  onDestroy: xe,
  setContext: Ce
} = window.__gradio__svelte__internal;
function D(n) {
  let e, s;
  const r = (
    /*#slots*/
    n[7].default
  ), o = _e(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = J("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = V(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = B(e);
      o && o.l(l), l.forEach(y), this.h();
    },
    h() {
      Y(e, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      C(t, e, l), o && o.m(e, null), n[9](e), s = !0;
    },
    p(t, l) {
      o && o.p && (!s || l & /*$$scope*/
      64) && ye(
        o,
        r,
        t,
        /*$$scope*/
        t[6],
        s ? pe(
          r,
          /*$$scope*/
          t[6],
          l,
          null
        ) : me(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      s || (I(o, t), s = !0);
    },
    o(t) {
      P(o, t), s = !1;
    },
    d(t) {
      t && y(e), o && o.d(t), n[9](null);
    }
  };
}
function Ie(n) {
  let e, s, r, o, t = (
    /*$$slots*/
    n[4].default && D(n)
  );
  return {
    c() {
      e = J("react-portal-target"), s = be(), t && t.c(), r = F(), this.h();
    },
    l(l) {
      e = V(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), B(e).forEach(y), s = ue(l), t && t.l(l), r = F(), this.h();
    },
    h() {
      Y(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      C(l, e, c), n[8](e), C(l, s, c), t && t.m(l, c), C(l, r, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, c), c & /*$$slots*/
      16 && I(t, 1)) : (t = D(l), t.c(), I(t, 1), t.m(r.parentNode, r)) : t && (he(), P(t, 1, 1, () => {
        t = null;
      }), de());
    },
    i(l) {
      o || (I(t), o = !0);
    },
    o(l) {
      P(t), o = !1;
    },
    d(l) {
      l && (y(e), y(s), y(r)), n[8](null), t && t.d(l);
    }
  };
}
function W(n) {
  const {
    svelteInit: e,
    ...s
  } = n;
  return s;
}
function Re(n, e, s) {
  let r, o, {
    $$slots: t = {},
    $$scope: l
  } = e;
  const c = fe(t);
  let {
    svelteInit: i
  } = e;
  const m = x(W(e)), d = x();
  N(n, d, (u) => s(0, r = u));
  const f = x();
  N(n, f, (u) => s(1, o = u));
  const a = [], _ = ve("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: h,
    subSlotIndex: b
  } = te() || {}, E = i({
    parent: _,
    props: m,
    target: d,
    slot: f,
    slotKey: p,
    slotIndex: h,
    subSlotIndex: b,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ce("$$ms-gr-react-wrapper", E), Ee(() => {
    m.set(W(e));
  }), xe(() => {
    a.forEach((u) => u());
  });
  function v(u) {
    T[u ? "unshift" : "push"](() => {
      r = u, d.set(r);
    });
  }
  function Q(u) {
    T[u ? "unshift" : "push"](() => {
      o = u, f.set(o);
    });
  }
  return n.$$set = (u) => {
    s(17, e = L(L({}, e), A(u))), "svelteInit" in u && s(5, i = u.svelteInit), "$$scope" in u && s(6, l = u.$$scope);
  }, e = A(e), [r, o, d, f, c, i, l, t, v, Q];
}
class Se extends ae {
  constructor(e) {
    super(), ge(this, e, Re, Ie, we, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, k = window.ms_globals.tree;
function ke(n) {
  function e(s) {
    const r = x(), o = new Se({
      ...s,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
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
          }, c = t.parent ?? k;
          return c.nodes = [...c.nodes, l], M({
            createPortal: O,
            node: k
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== r), M({
              createPortal: O,
              node: k
            });
          }), l;
        },
        ...s.props
      }
    });
    return r.set(o), o;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(e);
    });
  });
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((e, s) => {
    const r = n[s];
    return typeof r == "number" && !Oe.includes(s) ? e[s] = r + "px" : e[s] = r, e;
  }, {}) : {};
}
function j(n) {
  const e = [], s = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(O(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = j(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...w.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: l,
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, l, i);
    });
  });
  const r = Array.from(n.childNodes);
  for (let o = 0; o < r.length; o++) {
    const t = r[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = j(t);
      e.push(...c), s.appendChild(l);
    } else t.nodeType === 3 && s.appendChild(t.cloneNode());
  }
  return {
    clonedElement: s,
    portals: e
  };
}
function je(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const R = X(({
  slot: n,
  clone: e,
  className: s,
  style: r
}, o) => {
  const t = Z(), [l, c] = $([]);
  return ee(() => {
    var f;
    if (!t.current || !n)
      return;
    let i = n;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), je(o, a), s && a.classList.add(...s.split(" ")), r) {
        const _ = Pe(r);
        Object.keys(_).forEach((p) => {
          a.style[p] = _[p];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var b, E, v;
        (b = t.current) != null && b.contains(i) && ((E = t.current) == null || E.removeChild(i));
        const {
          portals: p,
          clonedElement: h
        } = j(n);
        return i = h, c(p), i.style.display = "contents", m(), (v = t.current) == null || v.appendChild(i), p.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", m(), (f = t.current) == null || f.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((_ = t.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, e, s, r, o]), w.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Le(n) {
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
function z(n) {
  return U(() => Le(n), [n]);
}
function K(n, e, s) {
  return n.filter(Boolean).map((r, o) => {
    var i;
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const t = {
      ...r.props,
      key: ((i = r.props) == null ? void 0 : i.key) ?? (s ? `${s}-${o}` : `${o}`)
    };
    let l = t;
    Object.keys(r.slots).forEach((m) => {
      if (!r.slots[m] || !(r.slots[m] instanceof Element) && !r.slots[m].el)
        return;
      const d = m.split(".");
      d.forEach((h, b) => {
        l[h] || (l[h] = {}), b !== d.length - 1 && (l = t[h]);
      });
      const f = r.slots[m];
      let a, _, p = (e == null ? void 0 : e.clone) ?? !1;
      f instanceof Element ? a = f : (a = f.el, _ = f.callback, p = f.clone ?? !1), l[d[d.length - 1]] = a ? _ ? (...h) => (_(d[d.length - 1], h), /* @__PURE__ */ g.jsx(R, {
        slot: a,
        clone: p
      })) : /* @__PURE__ */ g.jsx(R, {
        slot: a,
        clone: p
      }) : l[d[d.length - 1]], l = t;
    });
    const c = (e == null ? void 0 : e.children) || "children";
    return r[c] && (t[c] = K(r[c], e, `${o}`)), t;
  });
}
function Te(n, e) {
  return n ? /* @__PURE__ */ g.jsx(R, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function G({
  key: n,
  setSlotParams: e,
  slots: s
}, r) {
  return s[n] ? (...o) => (e(n, o), Te(s[n], {
    clone: !0,
    ...r
  })) : void 0;
}
const Fe = ke(({
  getPopupContainer: n,
  innerStyle: e,
  children: s,
  slots: r,
  menuItems: o,
  dropdownRender: t,
  setSlotParams: l,
  ...c
}) => {
  var d, f, a;
  const i = z(n), m = z(t);
  return /* @__PURE__ */ g.jsx(g.Fragment, {
    children: /* @__PURE__ */ g.jsx(ne, {
      ...c,
      menu: {
        ...c.menu,
        items: U(() => {
          var _;
          return ((_ = c.menu) == null ? void 0 : _.items) || K(o, {
            clone: !0
          });
        }, [o, (d = c.menu) == null ? void 0 : d.items]),
        expandIcon: r["menu.expandIcon"] ? G({
          slots: r,
          setSlotParams: l,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) : (f = c.menu) == null ? void 0 : f.expandIcon,
        overflowedIndicator: r["menu.overflowedIndicator"] ? /* @__PURE__ */ g.jsx(R, {
          slot: r["menu.overflowedIndicator"]
        }) : (a = c.menu) == null ? void 0 : a.overflowedIndicator
      },
      getPopupContainer: i,
      dropdownRender: r.dropdownRender ? G({
        slots: r,
        setSlotParams: l,
        key: "dropdownRender"
      }, {
        clone: !0
      }) : m,
      children: /* @__PURE__ */ g.jsx("div", {
        className: "ms-gr-antd-dropdown-content",
        style: {
          display: "inline-block",
          ...e
        },
        children: s
      })
    })
  });
});
export {
  Fe as Dropdown,
  Fe as default
};
