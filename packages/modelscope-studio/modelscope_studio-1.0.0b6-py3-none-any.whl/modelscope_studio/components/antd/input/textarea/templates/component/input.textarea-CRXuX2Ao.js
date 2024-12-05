import { b as $, g as ee, w as C } from "./Index-nZhstO7z.js";
const h = window.ms_globals.React, Z = window.ms_globals.React.forwardRef, P = window.ms_globals.React.useRef, q = window.ms_globals.React.useState, k = window.ms_globals.React.useEffect, z = window.ms_globals.React.useMemo, j = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Input;
function re(t, e) {
  return $(t, e);
}
var G = {
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
var ne = h, oe = Symbol.for("react.element"), se = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, ie = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(t, e, n) {
  var s, o = {}, r = null, l = null;
  n !== void 0 && (r = "" + n), e.key !== void 0 && (r = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) le.call(e, s) && !ae.hasOwnProperty(s) && (o[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) o[s] === void 0 && (o[s] = e[s]);
  return {
    $$typeof: oe,
    type: t,
    key: r,
    ref: l,
    props: o,
    _owner: ie.current
  };
}
R.Fragment = se;
R.jsx = H;
R.jsxs = H;
G.exports = R;
var w = G.exports;
const {
  SvelteComponent: ce,
  assign: L,
  binding_callbacks: A,
  check_outros: ue,
  children: K,
  claim_element: B,
  claim_space: de,
  component_subscribe: N,
  compute_slots: fe,
  create_slot: _e,
  detach: b,
  element: J,
  empty: V,
  exclude_internal_props: W,
  get_all_dirty_from_scope: me,
  get_slot_changes: pe,
  group_outros: he,
  init: ge,
  insert_hydration: I,
  safe_not_equal: we,
  set_custom_element_data: Y,
  space: be,
  transition_in: S,
  transition_out: F,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ve,
  onDestroy: xe,
  setContext: Ce
} = window.__gradio__svelte__internal;
function D(t) {
  let e, n;
  const s = (
    /*#slots*/
    t[7].default
  ), o = _e(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = J("svelte-slot"), o && o.c(), this.h();
    },
    l(r) {
      e = B(r, "SVELTE-SLOT", {
        class: !0
      });
      var l = K(e);
      o && o.l(l), l.forEach(b), this.h();
    },
    h() {
      Y(e, "class", "svelte-1rt0kpf");
    },
    m(r, l) {
      I(r, e, l), o && o.m(e, null), t[9](e), n = !0;
    },
    p(r, l) {
      o && o.p && (!n || l & /*$$scope*/
      64) && ye(
        o,
        s,
        r,
        /*$$scope*/
        r[6],
        n ? pe(
          s,
          /*$$scope*/
          r[6],
          l,
          null
        ) : me(
          /*$$scope*/
          r[6]
        ),
        null
      );
    },
    i(r) {
      n || (S(o, r), n = !0);
    },
    o(r) {
      F(o, r), n = !1;
    },
    d(r) {
      r && b(e), o && o.d(r), t[9](null);
    }
  };
}
function Ie(t) {
  let e, n, s, o, r = (
    /*$$slots*/
    t[4].default && D(t)
  );
  return {
    c() {
      e = J("react-portal-target"), n = be(), r && r.c(), s = V(), this.h();
    },
    l(l) {
      e = B(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(e).forEach(b), n = de(l), r && r.l(l), s = V(), this.h();
    },
    h() {
      Y(e, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      I(l, e, a), t[8](e), I(l, n, a), r && r.m(l, a), I(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? r ? (r.p(l, a), a & /*$$slots*/
      16 && S(r, 1)) : (r = D(l), r.c(), S(r, 1), r.m(s.parentNode, s)) : r && (he(), F(r, 1, 1, () => {
        r = null;
      }), ue());
    },
    i(l) {
      o || (S(r), o = !0);
    },
    o(l) {
      F(r), o = !1;
    },
    d(l) {
      l && (b(e), b(n), b(s)), t[8](null), r && r.d(l);
    }
  };
}
function M(t) {
  const {
    svelteInit: e,
    ...n
  } = t;
  return n;
}
function Se(t, e, n) {
  let s, o, {
    $$slots: r = {},
    $$scope: l
  } = e;
  const a = fe(r);
  let {
    svelteInit: i
  } = e;
  const p = C(M(e)), d = C();
  N(t, d, (u) => n(0, s = u));
  const f = C();
  N(t, f, (u) => n(1, o = u));
  const c = [], _ = ve("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: g,
    subSlotIndex: y
  } = ee() || {}, E = i({
    parent: _,
    props: p,
    target: d,
    slot: f,
    slotKey: m,
    slotIndex: g,
    subSlotIndex: y,
    onDestroy(u) {
      c.push(u);
    }
  });
  Ce("$$ms-gr-react-wrapper", E), Ee(() => {
    p.set(M(e));
  }), xe(() => {
    c.forEach((u) => u());
  });
  function v(u) {
    A[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function X(u) {
    A[u ? "unshift" : "push"](() => {
      o = u, f.set(o);
    });
  }
  return t.$$set = (u) => {
    n(17, e = L(L({}, e), W(u))), "svelteInit" in u && n(5, i = u.svelteInit), "$$scope" in u && n(6, l = u.$$scope);
  }, e = W(e), [s, o, d, f, a, i, l, r, v, X];
}
class Re extends ce {
  constructor(e) {
    super(), ge(this, e, Se, Ie, we, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, O = window.ms_globals.tree;
function Oe(t) {
  function e(n) {
    const s = C(), o = new Re({
      ...n,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: t,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            slotKey: r.slotKey,
            nodes: []
          }, a = r.parent ?? O;
          return a.nodes = [...a.nodes, l], U({
            createPortal: j,
            node: O
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), U({
              createPortal: j,
              node: O
            });
          }), l;
        },
        ...n.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(e);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(t) {
  return t ? Object.keys(t).reduce((e, n) => {
    const s = t[n];
    return typeof s == "number" && !Pe.includes(n) ? e[n] = s + "px" : e[n] = s, e;
  }, {}) : {};
}
function T(t) {
  const e = [], n = t.cloneNode(!1);
  if (t._reactElement)
    return e.push(j(h.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: h.Children.toArray(t._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: r,
            clonedElement: l
          } = T(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...h.Children.toArray(o.props.children), ...r]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: e
    };
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: l,
      type: a,
      useCapture: i
    }) => {
      n.addEventListener(a, l, i);
    });
  });
  const s = Array.from(t.childNodes);
  for (let o = 0; o < s.length; o++) {
    const r = s[o];
    if (r.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = T(r);
      e.push(...a), n.appendChild(l);
    } else r.nodeType === 3 && n.appendChild(r.cloneNode());
  }
  return {
    clonedElement: n,
    portals: e
  };
}
function je(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const Q = Z(({
  slot: t,
  clone: e,
  className: n,
  style: s
}, o) => {
  const r = P(), [l, a] = q([]);
  return k(() => {
    var f;
    if (!r.current || !t)
      return;
    let i = t;
    function p() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), je(o, c), n && c.classList.add(...n.split(" ")), s) {
        const _ = ke(s);
        Object.keys(_).forEach((m) => {
          c.style[m] = _[m];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let c = function() {
        var y, E, v;
        (y = r.current) != null && y.contains(i) && ((E = r.current) == null || E.removeChild(i));
        const {
          portals: m,
          clonedElement: g
        } = T(t);
        return i = g, a(m), i.style.display = "contents", p(), (v = r.current) == null || v.appendChild(i), m.length > 0;
      };
      c() || (d = new window.MutationObserver(() => {
        c() && (d == null || d.disconnect());
      }), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", p(), (f = r.current) == null || f.appendChild(i);
    return () => {
      var c, _;
      i.style.display = "", (c = r.current) != null && c.contains(i) && ((_ = r.current) == null || _.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, e, n, s, o]), h.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Fe(t) {
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
  return z(() => Fe(t), [t]);
}
function Te({
  value: t,
  onValueChange: e
}) {
  const [n, s] = q(t), o = P(e);
  o.current = e;
  const r = P(n);
  return r.current = n, k(() => {
    o.current(n);
  }, [n]), k(() => {
    re(t, r.current) || s(t);
  }, [t]), [n, s];
}
function Le(t) {
  return Object.keys(t).reduce((e, n) => (t[n] !== void 0 && (e[n] = t[n]), e), {});
}
function Ae(t, e) {
  return t ? /* @__PURE__ */ w.jsx(Q, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Ne({
  key: t,
  setSlotParams: e,
  slots: n
}, s) {
  return n[t] ? (...o) => (e(t, o), Ae(n[t], {
    clone: !0,
    ...s
  })) : void 0;
}
const We = Oe(({
  slots: t,
  children: e,
  count: n,
  showCount: s,
  onValueChange: o,
  onChange: r,
  elRef: l,
  setSlotParams: a,
  ...i
}) => {
  const p = x(n == null ? void 0 : n.strategy), d = x(n == null ? void 0 : n.exceedFormatter), f = x(n == null ? void 0 : n.show), c = x(typeof s == "object" ? s.formatter : void 0), [_, m] = Te({
    onValueChange: o,
    value: i.value
  });
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ w.jsx(te.TextArea, {
      ...i,
      ref: l,
      value: _,
      onChange: (g) => {
        r == null || r(g), m(g.target.value);
      },
      showCount: t["showCount.formatter"] ? {
        formatter: Ne({
          slots: t,
          setSlotParams: a,
          key: "showCount.formatter"
        })
      } : typeof s == "object" && c ? {
        ...s,
        formatter: c
      } : s,
      count: z(() => Le({
        ...n,
        exceedFormatter: d,
        strategy: p,
        show: f || (n == null ? void 0 : n.show)
      }), [n, d, p, f]),
      allowClear: t["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ w.jsx(Q, {
          slot: t["allowClear.clearIcon"]
        })
      } : i.allowClear
    })]
  });
});
export {
  We as InputTextarea,
  We as default
};
