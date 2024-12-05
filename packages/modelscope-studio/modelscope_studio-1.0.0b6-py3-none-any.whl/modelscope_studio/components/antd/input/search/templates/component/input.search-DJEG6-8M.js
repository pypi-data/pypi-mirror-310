import { b as $, g as ee, w as S } from "./Index-DfqwsSWQ.js";
const w = window.ms_globals.React, Z = window.ms_globals.React.forwardRef, j = window.ms_globals.React.useRef, q = window.ms_globals.React.useState, k = window.ms_globals.React.useEffect, z = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Input;
function re(e, t) {
  return $(e, t);
}
var G = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ne = w, oe = Symbol.for("react.element"), le = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ie = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(e, t, n) {
  var l, o = {}, r = null, s = null;
  n !== void 0 && (r = "" + n), t.key !== void 0 && (r = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) se.call(t, l) && !ae.hasOwnProperty(l) && (o[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: oe,
    type: e,
    key: r,
    ref: s,
    props: o,
    _owner: ie.current
  };
}
O.Fragment = le;
O.jsx = H;
O.jsxs = H;
G.exports = O;
var f = G.exports;
const {
  SvelteComponent: ce,
  assign: T,
  binding_callbacks: N,
  check_outros: de,
  children: K,
  claim_element: J,
  claim_space: ue,
  component_subscribe: B,
  compute_slots: fe,
  create_slot: _e,
  detach: y,
  element: Y,
  empty: V,
  exclude_internal_props: W,
  get_all_dirty_from_scope: me,
  get_slot_changes: pe,
  group_outros: he,
  init: ge,
  insert_hydration: I,
  safe_not_equal: we,
  set_custom_element_data: Q,
  space: be,
  transition_in: R,
  transition_out: A,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: xe,
  onDestroy: ve,
  setContext: Ce
} = window.__gradio__svelte__internal;
function D(e) {
  let t, n;
  const l = (
    /*#slots*/
    e[7].default
  ), o = _e(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Y("svelte-slot"), o && o.c(), this.h();
    },
    l(r) {
      t = J(r, "SVELTE-SLOT", {
        class: !0
      });
      var s = K(t);
      o && o.l(s), s.forEach(y), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(r, s) {
      I(r, t, s), o && o.m(t, null), e[9](t), n = !0;
    },
    p(r, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && ye(
        o,
        l,
        r,
        /*$$scope*/
        r[6],
        n ? pe(
          l,
          /*$$scope*/
          r[6],
          s,
          null
        ) : me(
          /*$$scope*/
          r[6]
        ),
        null
      );
    },
    i(r) {
      n || (R(o, r), n = !0);
    },
    o(r) {
      A(o, r), n = !1;
    },
    d(r) {
      r && y(t), o && o.d(r), e[9](null);
    }
  };
}
function Se(e) {
  let t, n, l, o, r = (
    /*$$slots*/
    e[4].default && D(e)
  );
  return {
    c() {
      t = Y("react-portal-target"), n = be(), r && r.c(), l = V(), this.h();
    },
    l(s) {
      t = J(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(t).forEach(y), n = ue(s), r && r.l(s), l = V(), this.h();
    },
    h() {
      Q(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      I(s, t, a), e[8](t), I(s, n, a), r && r.m(s, a), I(s, l, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? r ? (r.p(s, a), a & /*$$slots*/
      16 && R(r, 1)) : (r = D(s), r.c(), R(r, 1), r.m(l.parentNode, l)) : r && (he(), A(r, 1, 1, () => {
        r = null;
      }), de());
    },
    i(s) {
      o || (R(r), o = !0);
    },
    o(s) {
      A(r), o = !1;
    },
    d(s) {
      s && (y(t), y(n), y(l)), e[8](null), r && r.d(s);
    }
  };
}
function M(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function Ie(e, t, n) {
  let l, o, {
    $$slots: r = {},
    $$scope: s
  } = t;
  const a = fe(r);
  let {
    svelteInit: i
  } = t;
  const h = S(M(t)), u = S();
  B(e, u, (d) => n(0, l = d));
  const _ = S();
  B(e, _, (d) => n(1, o = d));
  const c = [], m = xe("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: b,
    subSlotIndex: E
  } = ee() || {}, x = i({
    parent: m,
    props: h,
    target: u,
    slot: _,
    slotKey: p,
    slotIndex: b,
    subSlotIndex: E,
    onDestroy(d) {
      c.push(d);
    }
  });
  Ce("$$ms-gr-react-wrapper", x), Ee(() => {
    h.set(M(t));
  }), ve(() => {
    c.forEach((d) => d());
  });
  function v(d) {
    N[d ? "unshift" : "push"](() => {
      l = d, u.set(l);
    });
  }
  function X(d) {
    N[d ? "unshift" : "push"](() => {
      o = d, _.set(o);
    });
  }
  return e.$$set = (d) => {
    n(17, t = T(T({}, t), W(d))), "svelteInit" in d && n(5, i = d.svelteInit), "$$scope" in d && n(6, s = d.$$scope);
  }, t = W(t), [l, o, u, _, a, i, s, r, v, X];
}
class Re extends ce {
  constructor(t) {
    super(), ge(this, t, Ie, Se, we, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, P = window.ms_globals.tree;
function Oe(e) {
  function t(n) {
    const l = S(), o = new Re({
      ...n,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            slotKey: r.slotKey,
            nodes: []
          }, a = r.parent ?? P;
          return a.nodes = [...a.nodes, s], U({
            createPortal: F,
            node: P
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== l), U({
              createPortal: F,
              node: P
            });
          }), s;
        },
        ...n.props
      }
    });
    return l.set(o), o;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const l = e[n];
    return typeof l == "number" && !Pe.includes(n) ? t[n] = l + "px" : t[n] = l, t;
  }, {}) : {};
}
function L(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement)
    return t.push(F(w.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: w.Children.toArray(e._reactElement.props.children).map((o) => {
        if (w.isValidElement(o) && o.props.__slot__) {
          const {
            portals: r,
            clonedElement: s
          } = L(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...w.Children.toArray(o.props.children), ...r]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: t
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: i
    }) => {
      n.addEventListener(a, s, i);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const r = l[o];
    if (r.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = L(r);
      t.push(...a), n.appendChild(s);
    } else r.nodeType === 3 && n.appendChild(r.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function ke(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const g = Z(({
  slot: e,
  clone: t,
  className: n,
  style: l
}, o) => {
  const r = j(), [s, a] = q([]);
  return k(() => {
    var _;
    if (!r.current || !e)
      return;
    let i = e;
    function h() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), ke(o, c), n && c.classList.add(...n.split(" ")), l) {
        const m = je(l);
        Object.keys(m).forEach((p) => {
          c.style[p] = m[p];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var E, x, v;
        (E = r.current) != null && E.contains(i) && ((x = r.current) == null || x.removeChild(i));
        const {
          portals: p,
          clonedElement: b
        } = L(e);
        return i = b, a(p), i.style.display = "contents", h(), (v = r.current) == null || v.appendChild(i), p.length > 0;
      };
      c() || (u = new window.MutationObserver(() => {
        c() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", h(), (_ = r.current) == null || _.appendChild(i);
    return () => {
      var c, m;
      i.style.display = "", (c = r.current) != null && c.contains(i) && ((m = r.current) == null || m.removeChild(i)), u == null || u.disconnect();
    };
  }, [e, t, n, l, o]), w.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...s);
});
function Fe(e) {
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
function C(e) {
  return z(() => Fe(e), [e]);
}
function Ae({
  value: e,
  onValueChange: t
}) {
  const [n, l] = q(e), o = j(t);
  o.current = t;
  const r = j(n);
  return r.current = n, k(() => {
    o.current(n);
  }, [n]), k(() => {
    re(e, r.current) || l(e);
  }, [e]), [n, l];
}
function Le(e) {
  return Object.keys(e).reduce((t, n) => (e[n] !== void 0 && (t[n] = e[n]), t), {});
}
function Te(e, t) {
  return e ? /* @__PURE__ */ f.jsx(g, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Ne({
  key: e,
  setSlotParams: t,
  slots: n
}, l) {
  return n[e] ? (...o) => (t(e, o), Te(n[e], {
    clone: !0,
    ...l
  })) : void 0;
}
const Ve = Oe(({
  slots: e,
  children: t,
  count: n,
  showCount: l,
  onValueChange: o,
  onChange: r,
  elRef: s,
  setSlotParams: a,
  ...i
}) => {
  const h = C(n == null ? void 0 : n.strategy), u = C(n == null ? void 0 : n.exceedFormatter), _ = C(n == null ? void 0 : n.show), c = C(typeof l == "object" ? l.formatter : void 0), [m, p] = Ae({
    onValueChange: o,
    value: i.value
  });
  return /* @__PURE__ */ f.jsxs(f.Fragment, {
    children: [/* @__PURE__ */ f.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ f.jsx(te.Search, {
      ...i,
      value: m,
      ref: s,
      onChange: (b) => {
        r == null || r(b), p(b.target.value);
      },
      showCount: e["showCount.formatter"] ? {
        formatter: Ne({
          slots: e,
          setSlotParams: a,
          key: "showCount.formatter"
        })
      } : typeof l == "object" && c ? {
        ...l,
        formatter: c
      } : l,
      count: z(() => Le({
        ...n,
        exceedFormatter: u,
        strategy: h,
        show: _ || (n == null ? void 0 : n.show)
      }), [n, u, h, _]),
      enterButton: e.enterButton ? /* @__PURE__ */ f.jsx(g, {
        slot: e.enterButton
      }) : i.enterButton,
      addonAfter: e.addonAfter ? /* @__PURE__ */ f.jsx(g, {
        slot: e.addonAfter
      }) : i.addonAfter,
      addonBefore: e.addonBefore ? /* @__PURE__ */ f.jsx(g, {
        slot: e.addonBefore
      }) : i.addonBefore,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ f.jsx(g, {
          slot: e["allowClear.clearIcon"]
        })
      } : i.allowClear,
      prefix: e.prefix ? /* @__PURE__ */ f.jsx(g, {
        slot: e.prefix
      }) : i.prefix,
      suffix: e.suffix ? /* @__PURE__ */ f.jsx(g, {
        slot: e.suffix
      }) : i.suffix
    })]
  });
});
export {
  Ve as InputSearch,
  Ve as default
};
