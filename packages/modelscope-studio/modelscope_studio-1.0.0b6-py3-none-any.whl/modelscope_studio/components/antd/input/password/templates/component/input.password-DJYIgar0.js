import { b as ee, g as te, w as C } from "./Index-BcUL9yWh.js";
const w = window.ms_globals.React, $ = window.ms_globals.React.forwardRef, j = window.ms_globals.React.useRef, z = window.ms_globals.React.useState, k = window.ms_globals.React.useEffect, G = window.ms_globals.React.useMemo, F = window.ms_globals.ReactDOM.createPortal, re = window.ms_globals.antd.Input;
function ne(e, t) {
  return ee(e, t);
}
var H = {
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
var oe = w, se = Symbol.for("react.element"), le = Symbol.for("react.fragment"), ie = Object.prototype.hasOwnProperty, ae = oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function K(e, t, n) {
  var s, o = {}, r = null, l = null;
  n !== void 0 && (r = "" + n), t.key !== void 0 && (r = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (s in t) ie.call(t, s) && !ce.hasOwnProperty(s) && (o[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: se,
    type: e,
    key: r,
    ref: l,
    props: o,
    _owner: ae.current
  };
}
P.Fragment = le;
P.jsx = K;
P.jsxs = K;
H.exports = P;
var h = H.exports;
const {
  SvelteComponent: de,
  assign: T,
  binding_callbacks: N,
  check_outros: ue,
  children: J,
  claim_element: Y,
  claim_space: fe,
  component_subscribe: V,
  compute_slots: _e,
  create_slot: me,
  detach: E,
  element: Q,
  empty: W,
  exclude_internal_props: D,
  get_all_dirty_from_scope: pe,
  get_slot_changes: he,
  group_outros: ge,
  init: we,
  insert_hydration: I,
  safe_not_equal: be,
  set_custom_element_data: X,
  space: ye,
  transition_in: S,
  transition_out: A,
  update_slot_base: Ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: xe,
  getContext: ve,
  onDestroy: Re,
  setContext: Ce
} = window.__gradio__svelte__internal;
function M(e) {
  let t, n;
  const s = (
    /*#slots*/
    e[7].default
  ), o = me(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Q("svelte-slot"), o && o.c(), this.h();
    },
    l(r) {
      t = Y(r, "SVELTE-SLOT", {
        class: !0
      });
      var l = J(t);
      o && o.l(l), l.forEach(E), this.h();
    },
    h() {
      X(t, "class", "svelte-1rt0kpf");
    },
    m(r, l) {
      I(r, t, l), o && o.m(t, null), e[9](t), n = !0;
    },
    p(r, l) {
      o && o.p && (!n || l & /*$$scope*/
      64) && Ee(
        o,
        s,
        r,
        /*$$scope*/
        r[6],
        n ? he(
          s,
          /*$$scope*/
          r[6],
          l,
          null
        ) : pe(
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
      A(o, r), n = !1;
    },
    d(r) {
      r && E(t), o && o.d(r), e[9](null);
    }
  };
}
function Ie(e) {
  let t, n, s, o, r = (
    /*$$slots*/
    e[4].default && M(e)
  );
  return {
    c() {
      t = Q("react-portal-target"), n = ye(), r && r.c(), s = W(), this.h();
    },
    l(l) {
      t = Y(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), J(t).forEach(E), n = fe(l), r && r.l(l), s = W(), this.h();
    },
    h() {
      X(t, "class", "svelte-1rt0kpf");
    },
    m(l, a) {
      I(l, t, a), e[8](t), I(l, n, a), r && r.m(l, a), I(l, s, a), o = !0;
    },
    p(l, [a]) {
      /*$$slots*/
      l[4].default ? r ? (r.p(l, a), a & /*$$slots*/
      16 && S(r, 1)) : (r = M(l), r.c(), S(r, 1), r.m(s.parentNode, s)) : r && (ge(), A(r, 1, 1, () => {
        r = null;
      }), ue());
    },
    i(l) {
      o || (S(r), o = !0);
    },
    o(l) {
      A(r), o = !1;
    },
    d(l) {
      l && (E(t), E(n), E(s)), e[8](null), r && r.d(l);
    }
  };
}
function B(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function Se(e, t, n) {
  let s, o, {
    $$slots: r = {},
    $$scope: l
  } = t;
  const a = _e(r);
  let {
    svelteInit: i
  } = t;
  const f = C(B(t)), u = C();
  V(e, u, (d) => n(0, s = d));
  const m = C();
  V(e, m, (d) => n(1, o = d));
  const c = [], _ = ve("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: x,
    subSlotIndex: b
  } = te() || {}, g = i({
    parent: _,
    props: f,
    target: u,
    slot: m,
    slotKey: p,
    slotIndex: x,
    subSlotIndex: b,
    onDestroy(d) {
      c.push(d);
    }
  });
  Ce("$$ms-gr-react-wrapper", g), xe(() => {
    f.set(B(t));
  }), Re(() => {
    c.forEach((d) => d());
  });
  function R(d) {
    N[d ? "unshift" : "push"](() => {
      s = d, u.set(s);
    });
  }
  function Z(d) {
    N[d ? "unshift" : "push"](() => {
      o = d, m.set(o);
    });
  }
  return e.$$set = (d) => {
    n(17, t = T(T({}, t), D(d))), "svelteInit" in d && n(5, i = d.svelteInit), "$$scope" in d && n(6, l = d.$$scope);
  }, t = D(t), [s, o, u, m, a, i, l, r, R, Z];
}
class Pe extends de {
  constructor(t) {
    super(), we(this, t, Se, Ie, be, {
      svelteInit: 5
    });
  }
}
const U = window.ms_globals.rerender, O = window.ms_globals.tree;
function Oe(e) {
  function t(n) {
    const s = C(), o = new Pe({
      ...n,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            slotKey: r.slotKey,
            nodes: []
          }, a = r.parent ?? O;
          return a.nodes = [...a.nodes, l], U({
            createPortal: F,
            node: O
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((i) => i.svelteInstance !== s), U({
              createPortal: F,
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
      n(t);
    });
  });
}
const je = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ke(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const s = e[n];
    return typeof s == "number" && !je.includes(n) ? t[n] = s + "px" : t[n] = s, t;
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
            clonedElement: l
          } = L(o.props.el);
          return w.cloneElement(o, {
            ...o.props,
            el: l,
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
      listener: l,
      type: a,
      useCapture: i
    }) => {
      n.addEventListener(a, l, i);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const r = s[o];
    if (r.nodeType === 1) {
      const {
        clonedElement: l,
        portals: a
      } = L(r);
      t.push(...a), n.appendChild(l);
    } else r.nodeType === 3 && n.appendChild(r.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Fe(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const y = $(({
  slot: e,
  clone: t,
  className: n,
  style: s
}, o) => {
  const r = j(), [l, a] = z([]);
  return k(() => {
    var m;
    if (!r.current || !e)
      return;
    let i = e;
    function f() {
      let c = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (c = i.children[0], c.tagName.toLowerCase() === "react-portal-target" && c.children[0] && (c = c.children[0])), Fe(o, c), n && c.classList.add(...n.split(" ")), s) {
        const _ = ke(s);
        Object.keys(_).forEach((p) => {
          c.style[p] = _[p];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let c = function() {
        var b, g, R;
        (b = r.current) != null && b.contains(i) && ((g = r.current) == null || g.removeChild(i));
        const {
          portals: p,
          clonedElement: x
        } = L(e);
        return i = x, a(p), i.style.display = "contents", f(), (R = r.current) == null || R.appendChild(i), p.length > 0;
      };
      c() || (u = new window.MutationObserver(() => {
        c() && (u == null || u.disconnect());
      }), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", f(), (m = r.current) == null || m.appendChild(i);
    return () => {
      var c, _;
      i.style.display = "", (c = r.current) != null && c.contains(i) && ((_ = r.current) == null || _.removeChild(i)), u == null || u.disconnect();
    };
  }, [e, t, n, s, o]), w.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ae(e) {
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
function v(e) {
  return G(() => Ae(e), [e]);
}
function Le({
  value: e,
  onValueChange: t
}) {
  const [n, s] = z(e), o = j(t);
  o.current = t;
  const r = j(n);
  return r.current = n, k(() => {
    o.current(n);
  }, [n]), k(() => {
    ne(e, r.current) || s(e);
  }, [e]), [n, s];
}
function Te(e) {
  return Object.keys(e).reduce((t, n) => (e[n] !== void 0 && (t[n] = e[n]), t), {});
}
function Ne(e, t) {
  return e ? /* @__PURE__ */ h.jsx(y, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function q({
  key: e,
  setSlotParams: t,
  slots: n
}, s) {
  return n[e] ? (...o) => (t(e, o), Ne(n[e], {
    clone: !0,
    ...s
  })) : void 0;
}
const We = Oe(({
  slots: e,
  children: t,
  count: n,
  showCount: s,
  onValueChange: o,
  onChange: r,
  iconRender: l,
  elRef: a,
  setSlotParams: i,
  ...f
}) => {
  const u = v(n == null ? void 0 : n.strategy), m = v(n == null ? void 0 : n.exceedFormatter), c = v(n == null ? void 0 : n.show), _ = v(typeof s == "object" ? s.formatter : void 0), p = v(l), [x, b] = Le({
    onValueChange: o,
    value: f.value
  });
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ h.jsx(re.Password, {
      ...f,
      value: x,
      ref: a,
      onChange: (g) => {
        r == null || r(g), b(g.target.value);
      },
      iconRender: e.iconRender ? q({
        slots: e,
        setSlotParams: i,
        key: "iconRender"
      }) : p,
      showCount: e["showCount.formatter"] ? {
        formatter: q({
          slots: e,
          setSlotParams: i,
          key: "showCount.formatter"
        })
      } : typeof s == "object" && _ ? {
        ...s,
        formatter: _
      } : s,
      count: G(() => Te({
        ...n,
        exceedFormatter: m,
        strategy: u,
        show: c || (n == null ? void 0 : n.show)
      }), [n, m, u, c]),
      addonAfter: e.addonAfter ? /* @__PURE__ */ h.jsx(y, {
        slot: e.addonAfter
      }) : f.addonAfter,
      addonBefore: e.addonBefore ? /* @__PURE__ */ h.jsx(y, {
        slot: e.addonBefore
      }) : f.addonBefore,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ h.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : f.allowClear,
      prefix: e.prefix ? /* @__PURE__ */ h.jsx(y, {
        slot: e.prefix
      }) : f.prefix,
      suffix: e.suffix ? /* @__PURE__ */ h.jsx(y, {
        slot: e.suffix
      }) : f.suffix
    })]
  });
});
export {
  We as InputPassword,
  We as default
};
