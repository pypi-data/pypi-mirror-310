import { g as ne, w as C, d as re, a as x } from "./Index-BLgnBo93.js";
const w = window.ms_globals.React, A = window.ms_globals.React.useMemo, q = window.ms_globals.React.useState, B = window.ms_globals.React.useEffect, ee = window.ms_globals.React.forwardRef, te = window.ms_globals.React.useRef, L = window.ms_globals.ReactDOM.createPortal, oe = window.ms_globals.antd.Transfer;
var J = {
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
var se = w, le = Symbol.for("react.element"), ie = Symbol.for("react.fragment"), ce = Object.prototype.hasOwnProperty, ae = se.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ue = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function K(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) ce.call(t, l) && !ue.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: le,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: ae.current
  };
}
P.Fragment = ie;
P.jsx = K;
P.jsxs = K;
J.exports = P;
var g = J.exports;
const {
  SvelteComponent: de,
  assign: F,
  binding_callbacks: N,
  check_outros: fe,
  children: Y,
  claim_element: Q,
  claim_space: pe,
  component_subscribe: W,
  compute_slots: _e,
  create_slot: me,
  detach: v,
  element: X,
  empty: D,
  exclude_internal_props: M,
  get_all_dirty_from_scope: he,
  get_slot_changes: ge,
  group_outros: be,
  init: we,
  insert_hydration: R,
  safe_not_equal: ye,
  set_custom_element_data: Z,
  space: ve,
  transition_in: O,
  transition_out: T,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: Ie,
  onDestroy: Se,
  setContext: Ce
} = window.__gradio__svelte__internal;
function z(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = me(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = X("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = Q(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = Y(t);
      o && o.l(s), s.forEach(v), this.h();
    },
    h() {
      Z(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      R(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && Ee(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? ge(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : he(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (O(o, e), r = !0);
    },
    o(e) {
      T(o, e), r = !1;
    },
    d(e) {
      e && v(t), o && o.d(e), n[9](null);
    }
  };
}
function Re(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && z(n)
  );
  return {
    c() {
      t = X("react-portal-target"), r = ve(), e && e.c(), l = D(), this.h();
    },
    l(s) {
      t = Q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Y(t).forEach(v), r = pe(s), e && e.l(s), l = D(), this.h();
    },
    h() {
      Z(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      R(s, t, c), n[8](t), R(s, r, c), e && e.m(s, c), R(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && O(e, 1)) : (e = z(s), e.c(), O(e, 1), e.m(l.parentNode, l)) : e && (be(), T(e, 1, 1, () => {
        e = null;
      }), fe());
    },
    i(s) {
      o || (O(e), o = !0);
    },
    o(s) {
      T(e), o = !1;
    },
    d(s) {
      s && (v(t), v(r), v(l)), n[8](null), e && e.d(s);
    }
  };
}
function G(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Oe(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = _e(e);
  let {
    svelteInit: i
  } = t;
  const b = C(G(t)), d = C();
  W(n, d, (u) => r(0, l = u));
  const p = C();
  W(n, p, (u) => r(1, o = u));
  const a = [], _ = Ie("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: E,
    subSlotIndex: y
  } = ne() || {}, f = i({
    parent: _,
    props: b,
    target: d,
    slot: p,
    slotKey: m,
    slotIndex: E,
    subSlotIndex: y,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ce("$$ms-gr-react-wrapper", f), xe(() => {
    b.set(G(t));
  }), Se(() => {
    a.forEach((u) => u());
  });
  function h(u) {
    N[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function $(u) {
    N[u ? "unshift" : "push"](() => {
      o = u, p.set(o);
    });
  }
  return n.$$set = (u) => {
    r(17, t = F(F({}, t), M(u))), "svelteInit" in u && r(5, i = u.svelteInit), "$$scope" in u && r(6, s = u.$$scope);
  }, t = M(t), [l, o, d, p, c, i, s, e, h, $];
}
class Pe extends de {
  constructor(t) {
    super(), we(this, t, Oe, Re, ye, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, k = window.ms_globals.tree;
function ke(n) {
  function t(r) {
    const l = C(), o = new Pe({
      ...r,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? k;
          return c.nodes = [...c.nodes, s], U({
            createPortal: L,
            node: k
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), U({
              createPortal: L,
              node: k
            });
          }), s;
        },
        ...r.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(t);
    });
  });
}
function Le(n) {
  const [t, r] = q(() => x(n));
  return B(() => {
    let l = !0;
    return n.subscribe((e) => {
      l && (l = !1, e === t) || r(e);
    });
  }, [n]), t;
}
function Te(n) {
  const t = A(() => re(n, (r) => r), [n]);
  return Le(t);
}
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ae(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !je.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function j(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(L(w.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: w.Children.toArray(n._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = j(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...w.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      r.addEventListener(c, s, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let o = 0; o < l.length; o++) {
    const e = l[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(e);
      t.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Fe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const I = ee(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = te(), [s, c] = q([]);
  return B(() => {
    var p;
    if (!e.current || !n)
      return;
    let i = n;
    function b() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), Fe(o, a), r && a.classList.add(...r.split(" ")), l) {
        const _ = Ae(l);
        Object.keys(_).forEach((m) => {
          a.style[m] = _[m];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var y, f, h;
        (y = e.current) != null && y.contains(i) && ((f = e.current) == null || f.removeChild(i));
        const {
          portals: m,
          clonedElement: E
        } = j(n);
        return i = E, c(m), i.style.display = "contents", b(), (h = e.current) == null || h.appendChild(i), m.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", b(), (p = e.current) == null || p.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = e.current) != null && a.contains(i) && ((_ = e.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, r, l, o]), w.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Ne(n) {
  try {
    if (typeof n == "string") {
      let t = n.trim();
      return t.startsWith(";") && (t = t.slice(1)), t.endsWith(";") && (t = t.slice(0, -1)), new Function(`return (...args) => (${t})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function S(n) {
  return A(() => Ne(n), [n]);
}
function H(n, t) {
  const r = A(() => w.Children.toArray(n).filter((e) => e.props.node && (!t && !e.props.nodeSlotKey || t && t === e.props.nodeSlotKey)).sort((e, s) => {
    if (e.props.node.slotIndex && s.props.node.slotIndex) {
      const c = x(e.props.node.slotIndex) || 0, i = x(s.props.node.slotIndex) || 0;
      return c - i === 0 && e.props.node.subSlotIndex && s.props.node.subSlotIndex ? (x(e.props.node.subSlotIndex) || 0) - (x(s.props.node.subSlotIndex) || 0) : c - i;
    }
    return 0;
  }).map((e) => e.props.node.target), [n, t]);
  return Te(r);
}
function We(n, t) {
  return n ? /* @__PURE__ */ g.jsx(I, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function V({
  key: n,
  setSlotParams: t,
  slots: r
}, l) {
  return r[n] ? (...o) => (t(n, o), We(r[n], {
    clone: !0,
    ...l
  })) : void 0;
}
const Me = ke(({
  slots: n,
  children: t,
  render: r,
  filterOption: l,
  footer: o,
  listStyle: e,
  locale: s,
  onChange: c,
  onValueChange: i,
  setSlotParams: b,
  ...d
}) => {
  const p = H(t, "titles"), a = H(t, "selectAllLabels"), _ = S(r), m = S(e), E = S(o), y = S(l);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ g.jsx(oe, {
      ...d,
      onChange: (f, ...h) => {
        c == null || c(f, ...h), i(f);
      },
      selectionsIcon: n.selectionsIcon ? /* @__PURE__ */ g.jsx(I, {
        slot: n.selectionsIcon
      }) : d.selectionsIcon,
      locale: n["locale.notFoundContent"] ? {
        ...s,
        notFoundContent: /* @__PURE__ */ g.jsx(I, {
          slot: n["locale.notFoundContent"]
        })
      } : s,
      render: n.render ? V({
        slots: n,
        setSlotParams: b,
        key: "render"
      }) : _ || ((f) => ({
        label: f.title || f.label,
        value: f.value || f.title || f.label
      })),
      filterOption: y,
      footer: n.footer ? V({
        slots: n,
        setSlotParams: b,
        key: "footer"
      }) : E || o,
      titles: p.length > 0 ? p.map((f, h) => /* @__PURE__ */ g.jsx(I, {
        slot: f
      }, h)) : d.titles,
      listStyle: m || e,
      selectAllLabels: a.length > 0 ? a.map((f, h) => /* @__PURE__ */ g.jsx(I, {
        slot: f
      }, h)) : d.selectAllLabels
    })]
  });
});
export {
  Me as Transfer,
  Me as default
};
