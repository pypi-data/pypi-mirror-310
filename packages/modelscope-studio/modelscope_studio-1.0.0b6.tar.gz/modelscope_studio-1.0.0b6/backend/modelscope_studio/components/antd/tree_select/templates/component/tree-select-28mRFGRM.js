import { g as le, w as k } from "./Index-Dyr5l-DB.js";
const E = window.ms_globals.React, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, ne = window.ms_globals.React.useState, re = window.ms_globals.React.useEffect, q = window.ms_globals.React.useMemo, j = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.TreeSelect;
var B = {
  exports: {}
}, P = {};
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
function V(t, e, l) {
  var r, o = {}, n = null, s = null;
  l !== void 0 && (n = "" + l), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (r in e) ae.call(e, r) && !de.hasOwnProperty(r) && (o[r] = e[r]);
  if (t && t.defaultProps) for (r in e = t.defaultProps, e) o[r] === void 0 && (o[r] = e[r]);
  return {
    $$typeof: ce,
    type: t,
    key: n,
    ref: s,
    props: o,
    _owner: ue.current
  };
}
P.Fragment = ie;
P.jsx = V;
P.jsxs = V;
B.exports = P;
var g = B.exports;
const {
  SvelteComponent: fe,
  assign: A,
  binding_callbacks: W,
  check_outros: _e,
  children: J,
  claim_element: Y,
  claim_space: he,
  component_subscribe: D,
  compute_slots: pe,
  create_slot: me,
  detach: R,
  element: K,
  empty: M,
  exclude_internal_props: U,
  get_all_dirty_from_scope: ge,
  get_slot_changes: we,
  group_outros: be,
  init: ye,
  insert_hydration: S,
  safe_not_equal: Ee,
  set_custom_element_data: Q,
  space: Re,
  transition_in: O,
  transition_out: F,
  update_slot_base: ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: Ce,
  onDestroy: Ie,
  setContext: ke
} = window.__gradio__svelte__internal;
function z(t) {
  let e, l;
  const r = (
    /*#slots*/
    t[7].default
  ), o = me(
    r,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = K("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      e = Y(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = J(e);
      o && o.l(s), s.forEach(R), this.h();
    },
    h() {
      Q(e, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      S(n, e, s), o && o.m(e, null), t[9](e), l = !0;
    },
    p(n, s) {
      o && o.p && (!l || s & /*$$scope*/
      64) && ve(
        o,
        r,
        n,
        /*$$scope*/
        n[6],
        l ? we(
          r,
          /*$$scope*/
          n[6],
          s,
          null
        ) : ge(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      l || (O(o, n), l = !0);
    },
    o(n) {
      F(o, n), l = !1;
    },
    d(n) {
      n && R(e), o && o.d(n), t[9](null);
    }
  };
}
function Se(t) {
  let e, l, r, o, n = (
    /*$$slots*/
    t[4].default && z(t)
  );
  return {
    c() {
      e = K("react-portal-target"), l = Re(), n && n.c(), r = M(), this.h();
    },
    l(s) {
      e = Y(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(e).forEach(R), l = he(s), n && n.l(s), r = M(), this.h();
    },
    h() {
      Q(e, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      S(s, e, i), t[8](e), S(s, l, i), n && n.m(s, i), S(s, r, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, i), i & /*$$slots*/
      16 && O(n, 1)) : (n = z(s), n.c(), O(n, 1), n.m(r.parentNode, r)) : n && (be(), F(n, 1, 1, () => {
        n = null;
      }), _e());
    },
    i(s) {
      o || (O(n), o = !0);
    },
    o(s) {
      F(n), o = !1;
    },
    d(s) {
      s && (R(e), R(l), R(r)), t[8](null), n && n.d(s);
    }
  };
}
function G(t) {
  const {
    svelteInit: e,
    ...l
  } = t;
  return l;
}
function Oe(t, e, l) {
  let r, o, {
    $$slots: n = {},
    $$scope: s
  } = e;
  const i = pe(n);
  let {
    svelteInit: c
  } = e;
  const m = k(G(e)), a = k();
  D(t, a, (d) => l(0, r = d));
  const _ = k();
  D(t, _, (d) => l(1, o = d));
  const u = [], f = Ce("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: h,
    subSlotIndex: w
  } = le() || {}, b = c({
    parent: f,
    props: m,
    target: a,
    slot: _,
    slotKey: p,
    slotIndex: h,
    subSlotIndex: w,
    onDestroy(d) {
      u.push(d);
    }
  });
  ke("$$ms-gr-react-wrapper", b), xe(() => {
    m.set(G(e));
  }), Ie(() => {
    u.forEach((d) => d());
  });
  function y(d) {
    W[d ? "unshift" : "push"](() => {
      r = d, a.set(r);
    });
  }
  function I(d) {
    W[d ? "unshift" : "push"](() => {
      o = d, _.set(o);
    });
  }
  return t.$$set = (d) => {
    l(17, e = A(A({}, e), U(d))), "svelteInit" in d && l(5, c = d.svelteInit), "$$scope" in d && l(6, s = d.$$scope);
  }, e = U(e), [r, o, a, _, i, c, s, n, y, I];
}
class Pe extends fe {
  constructor(e) {
    super(), ye(this, e, Oe, Se, Ee, {
      svelteInit: 5
    });
  }
}
const H = window.ms_globals.rerender, T = window.ms_globals.tree;
function Te(t) {
  function e(l) {
    const r = k(), o = new Pe({
      ...l,
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
          }, i = n.parent ?? T;
          return i.nodes = [...i.nodes, s], H({
            createPortal: j,
            node: T
          }), n.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== r), H({
              createPortal: j,
              node: T
            });
          }), s;
        },
        ...l.props
      }
    });
    return r.set(o), o;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(e);
    });
  });
}
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Fe(t) {
  return t ? Object.keys(t).reduce((e, l) => {
    const r = t[l];
    return typeof r == "number" && !je.includes(l) ? e[l] = r + "px" : e[l] = r, e;
  }, {}) : {};
}
function L(t) {
  const e = [], l = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(j(E.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: E.Children.toArray(t._reactElement.props.children).map((o) => {
        if (E.isValidElement(o) && o.props.__slot__) {
          const {
            portals: n,
            clonedElement: s
          } = L(o.props.el);
          return E.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...E.Children.toArray(o.props.children), ...n]
          });
        }
        return null;
      })
    }), l)), {
      clonedElement: l,
      portals: e
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: s,
      type: i,
      useCapture: c
    }) => {
      l.addEventListener(i, s, c);
    });
  });
  const r = Array.from(t.childNodes);
  for (let o = 0; o < r.length; o++) {
    const n = r[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = L(n);
      e.push(...i), l.appendChild(s);
    } else n.nodeType === 3 && l.appendChild(n.cloneNode());
  }
  return {
    clonedElement: l,
    portals: e
  };
}
function Le(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const v = ee(({
  slot: t,
  clone: e,
  className: l,
  style: r
}, o) => {
  const n = te(), [s, i] = ne([]);
  return re(() => {
    var _;
    if (!n.current || !t)
      return;
    let c = t;
    function m() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Le(o, u), l && u.classList.add(...l.split(" ")), r) {
        const f = Fe(r);
        Object.keys(f).forEach((p) => {
          u.style[p] = f[p];
        });
      }
    }
    let a = null;
    if (e && window.MutationObserver) {
      let u = function() {
        var w, b, y;
        (w = n.current) != null && w.contains(c) && ((b = n.current) == null || b.removeChild(c));
        const {
          portals: p,
          clonedElement: h
        } = L(t);
        return c = h, i(p), c.style.display = "contents", m(), (y = n.current) == null || y.appendChild(c), p.length > 0;
      };
      u() || (a = new window.MutationObserver(() => {
        u() && (a == null || a.disconnect());
      }), a.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", m(), (_ = n.current) == null || _.appendChild(c);
    return () => {
      var u, f;
      c.style.display = "", (u = n.current) != null && u.contains(c) && ((f = n.current) == null || f.removeChild(c)), a == null || a.disconnect();
    };
  }, [t, e, l, r, o]), E.createElement("react-child", {
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
function x(t) {
  return q(() => Ne(t), [t]);
}
function Ae(t) {
  return Object.keys(t).reduce((e, l) => (t[l] !== void 0 && (e[l] = t[l]), e), {});
}
function X(t, e, l) {
  return t.filter(Boolean).map((r, o) => {
    var c;
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const n = {
      ...r.props,
      key: ((c = r.props) == null ? void 0 : c.key) ?? (l ? `${l}-${o}` : `${o}`)
    };
    let s = n;
    Object.keys(r.slots).forEach((m) => {
      if (!r.slots[m] || !(r.slots[m] instanceof Element) && !r.slots[m].el)
        return;
      const a = m.split(".");
      a.forEach((h, w) => {
        s[h] || (s[h] = {}), w !== a.length - 1 && (s = n[h]);
      });
      const _ = r.slots[m];
      let u, f, p = (e == null ? void 0 : e.clone) ?? !1;
      _ instanceof Element ? u = _ : (u = _.el, f = _.callback, p = _.clone ?? !1), s[a[a.length - 1]] = u ? f ? (...h) => (f(a[a.length - 1], h), /* @__PURE__ */ g.jsx(v, {
        slot: u,
        clone: p
      })) : /* @__PURE__ */ g.jsx(v, {
        slot: u,
        clone: p
      }) : s[a[a.length - 1]], s = n;
    });
    const i = (e == null ? void 0 : e.children) || "children";
    return r[i] && (n[i] = X(r[i], e, `${o}`)), n;
  });
}
function We(t, e) {
  return t ? /* @__PURE__ */ g.jsx(v, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function C({
  key: t,
  setSlotParams: e,
  slots: l
}, r) {
  return l[t] ? (...o) => (e(t, o), We(l[t], {
    clone: !0,
    ...r
  })) : void 0;
}
const Me = Te(({
  slots: t,
  filterTreeNode: e,
  getPopupContainer: l,
  dropdownRender: r,
  tagRender: o,
  treeTitleRender: n,
  treeData: s,
  onValueChange: i,
  onChange: c,
  children: m,
  slotItems: a,
  maxTagPlaceholder: _,
  elRef: u,
  setSlotParams: f,
  onLoadData: p,
  ...h
}) => {
  const w = x(e), b = x(l), y = x(o), I = x(r), d = x(n), Z = q(() => ({
    ...h,
    loadData: p,
    treeData: s || X(a, {
      clone: !0
    }),
    dropdownRender: t.dropdownRender ? C({
      slots: t,
      setSlotParams: f,
      key: "dropdownRender"
    }) : I,
    allowClear: t["allowClear.clearIcon"] ? {
      clearIcon: /* @__PURE__ */ g.jsx(v, {
        slot: t["allowClear.clearIcon"]
      })
    } : h.allowClear,
    suffixIcon: t.suffixIcon ? /* @__PURE__ */ g.jsx(v, {
      slot: t.suffixIcon
    }) : h.suffixIcon,
    switcherIcon: t.switcherIcon ? C({
      slots: t,
      setSlotParams: f,
      key: "switcherIcon"
    }) : h.switcherIcon,
    getPopupContainer: b,
    tagRender: t.tagRender ? C({
      slots: t,
      setSlotParams: f,
      key: "tagRender"
    }) : y,
    treeTitleRender: t.treeTitleRender ? C({
      slots: t,
      setSlotParams: f,
      key: "treeTitleRender"
    }) : d,
    filterTreeNode: w || e,
    maxTagPlaceholder: t.maxTagPlaceholder ? C({
      slots: t,
      setSlotParams: f,
      key: "maxTagPlaceholder"
    }) : _,
    notFoundContent: t.notFoundContent ? /* @__PURE__ */ g.jsx(v, {
      slot: t.notFoundContent
    }) : h.notFoundContent
  }), [I, e, w, b, _, p, h, f, a, t, y, s, d]);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: m
    }), /* @__PURE__ */ g.jsx(oe, {
      ...Ae(Z),
      ref: u,
      onChange: (N, ...$) => {
        c == null || c(N, ...$), i(N);
      }
    })]
  });
});
export {
  Me as TreeSelect,
  Me as default
};
