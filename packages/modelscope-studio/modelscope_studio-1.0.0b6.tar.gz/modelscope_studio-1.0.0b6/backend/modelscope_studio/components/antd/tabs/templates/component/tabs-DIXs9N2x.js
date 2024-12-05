import { g as ee, w as C } from "./Index-Chv9_G1E.js";
const E = window.ms_globals.React, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, M = window.ms_globals.React.useMemo, j = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Tabs;
var U = {
  exports: {}
}, R = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = E, re = Symbol.for("react.element"), oe = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(t, n, o) {
  var r, l = {}, e = null, s = null;
  o !== void 0 && (e = "" + o), n.key !== void 0 && (e = "" + n.key), n.ref !== void 0 && (s = n.ref);
  for (r in n) le.call(n, r) && !ae.hasOwnProperty(r) && (l[r] = n[r]);
  if (t && t.defaultProps) for (r in n = t.defaultProps, n) l[r] === void 0 && (l[r] = n[r]);
  return {
    $$typeof: re,
    type: t,
    key: e,
    ref: s,
    props: l,
    _owner: se.current
  };
}
R.Fragment = oe;
R.jsx = G;
R.jsxs = G;
U.exports = R;
var h = U.exports;
const {
  SvelteComponent: ie,
  assign: B,
  binding_callbacks: L,
  check_outros: ce,
  children: H,
  claim_element: q,
  claim_space: ue,
  component_subscribe: F,
  compute_slots: de,
  create_slot: fe,
  detach: v,
  element: V,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: _e,
  get_slot_changes: pe,
  group_outros: he,
  init: me,
  insert_hydration: I,
  safe_not_equal: be,
  set_custom_element_data: J,
  space: ge,
  transition_in: S,
  transition_out: k,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: ve,
  onDestroy: xe,
  setContext: ye
} = window.__gradio__svelte__internal;
function z(t) {
  let n, o;
  const r = (
    /*#slots*/
    t[7].default
  ), l = fe(
    r,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      n = V("svelte-slot"), l && l.c(), this.h();
    },
    l(e) {
      n = q(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(n);
      l && l.l(s), s.forEach(v), this.h();
    },
    h() {
      J(n, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      I(e, n, s), l && l.m(n, null), t[9](n), o = !0;
    },
    p(e, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && Ee(
        l,
        r,
        e,
        /*$$scope*/
        e[6],
        o ? pe(
          r,
          /*$$scope*/
          e[6],
          s,
          null
        ) : _e(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      o || (S(l, e), o = !0);
    },
    o(e) {
      k(l, e), o = !1;
    },
    d(e) {
      e && v(n), l && l.d(e), t[9](null);
    }
  };
}
function Ce(t) {
  let n, o, r, l, e = (
    /*$$slots*/
    t[4].default && z(t)
  );
  return {
    c() {
      n = V("react-portal-target"), o = ge(), e && e.c(), r = N(), this.h();
    },
    l(s) {
      n = q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(n).forEach(v), o = ue(s), e && e.l(s), r = N(), this.h();
    },
    h() {
      J(n, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      I(s, n, i), t[8](n), I(s, o, i), e && e.m(s, i), I(s, r, i), l = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && S(e, 1)) : (e = z(s), e.c(), S(e, 1), e.m(r.parentNode, r)) : e && (he(), k(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(s) {
      l || (S(e), l = !0);
    },
    o(s) {
      k(e), l = !1;
    },
    d(s) {
      s && (v(n), v(o), v(r)), t[8](null), e && e.d(s);
    }
  };
}
function W(t) {
  const {
    svelteInit: n,
    ...o
  } = t;
  return o;
}
function Ie(t, n, o) {
  let r, l, {
    $$slots: e = {},
    $$scope: s
  } = n;
  const i = de(e);
  let {
    svelteInit: a
  } = n;
  const f = C(W(n)), c = C();
  F(t, c, (d) => o(0, r = d));
  const _ = C();
  F(t, _, (d) => o(1, l = d));
  const u = [], p = ve("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: b,
    subSlotIndex: w
  } = ee() || {}, x = a({
    parent: p,
    props: f,
    target: c,
    slot: _,
    slotKey: m,
    slotIndex: b,
    subSlotIndex: w,
    onDestroy(d) {
      u.push(d);
    }
  });
  ye("$$ms-gr-react-wrapper", x), we(() => {
    f.set(W(n));
  }), xe(() => {
    u.forEach((d) => d());
  });
  function y(d) {
    L[d ? "unshift" : "push"](() => {
      r = d, c.set(r);
    });
  }
  function K(d) {
    L[d ? "unshift" : "push"](() => {
      l = d, _.set(l);
    });
  }
  return t.$$set = (d) => {
    o(17, n = B(B({}, n), A(d))), "svelteInit" in d && o(5, a = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, n = A(n), [r, l, c, _, i, a, s, e, y, K];
}
class Se extends ie {
  constructor(n) {
    super(), me(this, n, Ie, Ce, be, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, P = window.ms_globals.tree;
function Re(t) {
  function n(o) {
    const r = C(), l = new Se({
      ...o,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? P;
          return i.nodes = [...i.nodes, s], D({
            createPortal: j,
            node: P
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((a) => a.svelteInstance !== r), D({
              createPortal: j,
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
      o(n);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(t) {
  return t ? Object.keys(t).reduce((n, o) => {
    const r = t[o];
    return typeof r == "number" && !Pe.includes(o) ? n[o] = r + "px" : n[o] = r, n;
  }, {}) : {};
}
function T(t) {
  const n = [], o = t.cloneNode(!1);
  if (t._reactElement)
    return n.push(j(E.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: E.Children.toArray(t._reactElement.props.children).map((l) => {
        if (E.isValidElement(l) && l.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = T(l.props.el);
          return E.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...E.Children.toArray(l.props.children), ...e]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: n
    };
  Object.keys(t.getEventListeners()).forEach((l) => {
    t.getEventListeners(l).forEach(({
      listener: s,
      type: i,
      useCapture: a
    }) => {
      o.addEventListener(i, s, a);
    });
  });
  const r = Array.from(t.childNodes);
  for (let l = 0; l < r.length; l++) {
    const e = r[l];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = T(e);
      n.push(...i), o.appendChild(s);
    } else e.nodeType === 3 && o.appendChild(e.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function je(t, n) {
  t && (typeof t == "function" ? t(n) : t.current = n);
}
const g = Q(({
  slot: t,
  clone: n,
  className: o,
  style: r
}, l) => {
  const e = X(), [s, i] = Z([]);
  return $(() => {
    var _;
    if (!e.current || !t)
      return;
    let a = t;
    function f() {
      let u = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (u = a.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), je(l, u), o && u.classList.add(...o.split(" ")), r) {
        const p = Oe(r);
        Object.keys(p).forEach((m) => {
          u.style[m] = p[m];
        });
      }
    }
    let c = null;
    if (n && window.MutationObserver) {
      let u = function() {
        var w, x, y;
        (w = e.current) != null && w.contains(a) && ((x = e.current) == null || x.removeChild(a));
        const {
          portals: m,
          clonedElement: b
        } = T(t);
        return a = b, i(m), a.style.display = "contents", f(), (y = e.current) == null || y.appendChild(a), m.length > 0;
      };
      u() || (c = new window.MutationObserver(() => {
        u() && (c == null || c.disconnect());
      }), c.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      a.style.display = "contents", f(), (_ = e.current) == null || _.appendChild(a);
    return () => {
      var u, p;
      a.style.display = "", (u = e.current) != null && u.contains(a) && ((p = e.current) == null || p.removeChild(a)), c == null || c.disconnect();
    };
  }, [t, n, o, r, l]), E.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function ke(t) {
  try {
    if (typeof t == "string") {
      let n = t.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function O(t) {
  return M(() => ke(t), [t]);
}
function Te(t) {
  return Object.keys(t).reduce((n, o) => (t[o] !== void 0 && (n[o] = t[o]), n), {});
}
function Y(t, n, o) {
  return t.filter(Boolean).map((r, l) => {
    var a;
    if (typeof r != "object")
      return r;
    const e = {
      ...r.props,
      key: ((a = r.props) == null ? void 0 : a.key) ?? (o ? `${o}-${l}` : `${l}`)
    };
    let s = e;
    Object.keys(r.slots).forEach((f) => {
      if (!r.slots[f] || !(r.slots[f] instanceof Element) && !r.slots[f].el)
        return;
      const c = f.split(".");
      c.forEach((b, w) => {
        s[b] || (s[b] = {}), w !== c.length - 1 && (s = e[b]);
      });
      const _ = r.slots[f];
      let u, p, m = !1;
      _ instanceof Element ? u = _ : (u = _.el, p = _.callback, m = _.clone ?? !1), s[c[c.length - 1]] = u ? p ? (...b) => (p(c[c.length - 1], b), /* @__PURE__ */ h.jsx(g, {
        slot: u,
        clone: m
      })) : /* @__PURE__ */ h.jsx(g, {
        slot: u,
        clone: m
      }) : s[c[c.length - 1]], s = e;
    });
    const i = "children";
    return r[i] && (e[i] = Y(r[i], n, `${l}`)), e;
  });
}
function Be(t, n) {
  return t ? /* @__PURE__ */ h.jsx(g, {
    slot: t,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function Le({
  key: t,
  setSlotParams: n,
  slots: o
}, r) {
  return o[t] ? (...l) => (n(t, l), Be(o[t], {
    clone: !0,
    ...r
  })) : void 0;
}
const Ne = Re(({
  slots: t,
  indicator: n,
  items: o,
  onChange: r,
  slotItems: l,
  more: e,
  children: s,
  renderTabBar: i,
  setSlotParams: a,
  ...f
}) => {
  const c = O(n == null ? void 0 : n.size), _ = O(e == null ? void 0 : e.getPopupContainer), u = O(i);
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: s
    }), /* @__PURE__ */ h.jsx(te, {
      ...f,
      indicator: c ? {
        ...n,
        size: c
      } : n,
      renderTabBar: t.renderTabBar ? Le({
        slots: t,
        setSlotParams: a,
        key: "renderTabBar"
      }) : u,
      items: M(() => o || Y(l), [o, l]),
      more: Te({
        ...e || {},
        getPopupContainer: _ || (e == null ? void 0 : e.getPopupContainer),
        icon: t["more.icon"] ? /* @__PURE__ */ h.jsx(g, {
          slot: t["more.icon"]
        }) : e == null ? void 0 : e.icon
      }),
      tabBarExtraContent: t.tabBarExtraContent ? /* @__PURE__ */ h.jsx(g, {
        slot: t.tabBarExtraContent
      }) : t["tabBarExtraContent.left"] || t["tabBarExtraContent.right"] ? {
        left: t["tabBarExtraContent.left"] ? /* @__PURE__ */ h.jsx(g, {
          slot: t["tabBarExtraContent.left"]
        }) : void 0,
        right: t["tabBarExtraContent.right"] ? /* @__PURE__ */ h.jsx(g, {
          slot: t["tabBarExtraContent.right"]
        }) : void 0
      } : f.tabBarExtraContent,
      addIcon: t.addIcon ? /* @__PURE__ */ h.jsx(g, {
        slot: t.addIcon
      }) : f.addIcon,
      removeIcon: t.removeIcon ? /* @__PURE__ */ h.jsx(g, {
        slot: t.removeIcon
      }) : f.removeIcon,
      onChange: (p) => {
        r == null || r(p);
      }
    })]
  });
});
export {
  Ne as Tabs,
  Ne as default
};
