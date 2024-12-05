import { b as $, g as ee, w as v } from "./Index-D8q_icAb.js";
const g = window.ms_globals.React, X = window.ms_globals.React.forwardRef, P = window.ms_globals.React.useRef, z = window.ms_globals.React.useState, j = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.InputNumber;
function ne(e, n) {
  return $(e, n);
}
var G = {
  exports: {}
}, C = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var oe = g, re = Symbol.for("react.element"), se = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, ie = oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(e, n, r) {
  var s, o = {}, t = null, l = null;
  r !== void 0 && (t = "" + r), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (l = n.ref);
  for (s in n) le.call(n, s) && !ce.hasOwnProperty(s) && (o[s] = n[s]);
  if (e && e.defaultProps) for (s in n = e.defaultProps, n) o[s] === void 0 && (o[s] = n[s]);
  return {
    $$typeof: re,
    type: e,
    key: t,
    ref: l,
    props: o,
    _owner: ie.current
  };
}
C.Fragment = se;
C.jsx = U;
C.jsxs = U;
G.exports = C;
var f = G.exports;
const {
  SvelteComponent: ae,
  assign: N,
  binding_callbacks: T,
  check_outros: ue,
  children: H,
  claim_element: K,
  claim_space: de,
  component_subscribe: F,
  compute_slots: fe,
  create_slot: _e,
  detach: b,
  element: J,
  empty: V,
  exclude_internal_props: W,
  get_all_dirty_from_scope: pe,
  get_slot_changes: me,
  group_outros: he,
  init: ge,
  insert_hydration: I,
  safe_not_equal: we,
  set_custom_element_data: Y,
  space: be,
  transition_in: R,
  transition_out: A,
  update_slot_base: ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: xe,
  onDestroy: ve,
  setContext: Ie
} = window.__gradio__svelte__internal;
function D(e) {
  let n, r;
  const s = (
    /*#slots*/
    e[7].default
  ), o = _e(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = J("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      n = K(t, "SVELTE-SLOT", {
        class: !0
      });
      var l = H(n);
      o && o.l(l), l.forEach(b), this.h();
    },
    h() {
      Y(n, "class", "svelte-1rt0kpf");
    },
    m(t, l) {
      I(t, n, l), o && o.m(n, null), e[9](n), r = !0;
    },
    p(t, l) {
      o && o.p && (!r || l & /*$$scope*/
      64) && ye(
        o,
        s,
        t,
        /*$$scope*/
        t[6],
        r ? me(
          s,
          /*$$scope*/
          t[6],
          l,
          null
        ) : pe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (R(o, t), r = !0);
    },
    o(t) {
      A(o, t), r = !1;
    },
    d(t) {
      t && b(n), o && o.d(t), e[9](null);
    }
  };
}
function Re(e) {
  let n, r, s, o, t = (
    /*$$slots*/
    e[4].default && D(e)
  );
  return {
    c() {
      n = J("react-portal-target"), r = be(), t && t.c(), s = V(), this.h();
    },
    l(l) {
      n = K(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(n).forEach(b), r = de(l), t && t.l(l), s = V(), this.h();
    },
    h() {
      Y(n, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      I(l, n, i), e[8](n), I(l, r, i), t && t.m(l, i), I(l, s, i), o = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? t ? (t.p(l, i), i & /*$$slots*/
      16 && R(t, 1)) : (t = D(l), t.c(), R(t, 1), t.m(s.parentNode, s)) : t && (he(), A(t, 1, 1, () => {
        t = null;
      }), ue());
    },
    i(l) {
      o || (R(t), o = !0);
    },
    o(l) {
      A(t), o = !1;
    },
    d(l) {
      l && (b(n), b(r), b(s)), e[8](null), t && t.d(l);
    }
  };
}
function M(e) {
  const {
    svelteInit: n,
    ...r
  } = e;
  return r;
}
function Ce(e, n, r) {
  let s, o, {
    $$slots: t = {},
    $$scope: l
  } = n;
  const i = fe(t);
  let {
    svelteInit: c
  } = n;
  const h = v(M(n)), d = v();
  F(e, d, (u) => r(0, s = u));
  const _ = v();
  F(e, _, (u) => r(1, o = u));
  const a = [], p = xe("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: S,
    subSlotIndex: y
  } = ee() || {}, E = c({
    parent: p,
    props: h,
    target: d,
    slot: _,
    slotKey: m,
    slotIndex: S,
    subSlotIndex: y,
    onDestroy(u) {
      a.push(u);
    }
  });
  Ie("$$ms-gr-react-wrapper", E), Ee(() => {
    h.set(M(n));
  }), ve(() => {
    a.forEach((u) => u());
  });
  function x(u) {
    T[u ? "unshift" : "push"](() => {
      s = u, d.set(s);
    });
  }
  function Q(u) {
    T[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return e.$$set = (u) => {
    r(17, n = N(N({}, n), W(u))), "svelteInit" in u && r(5, c = u.svelteInit), "$$scope" in u && r(6, l = u.$$scope);
  }, n = W(n), [s, o, d, _, i, c, l, t, x, Q];
}
class Se extends ae {
  constructor(n) {
    super(), ge(this, n, Ce, Re, we, {
      svelteInit: 5
    });
  }
}
const B = window.ms_globals.rerender, O = window.ms_globals.tree;
function Oe(e) {
  function n(r) {
    const s = v(), o = new Se({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? O;
          return i.nodes = [...i.nodes, l], B({
            createPortal: k,
            node: O
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== s), B({
              createPortal: k,
              node: O
            });
          }), l;
        },
        ...r.props
      }
    });
    return s.set(o), o;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
const Pe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function je(e) {
  return e ? Object.keys(e).reduce((n, r) => {
    const s = e[r];
    return typeof s == "number" && !Pe.includes(r) ? n[r] = s + "px" : n[r] = s, n;
  }, {}) : {};
}
function L(e) {
  const n = [], r = e.cloneNode(!1);
  if (e._reactElement)
    return n.push(k(g.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: g.Children.toArray(e._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: l
          } = L(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...g.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), r)), {
      clonedElement: r,
      portals: n
    };
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      r.addEventListener(i, l, c);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const t = s[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = L(t);
      n.push(...i), r.appendChild(l);
    } else t.nodeType === 3 && r.appendChild(t.cloneNode());
  }
  return {
    clonedElement: r,
    portals: n
  };
}
function ke(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const w = X(({
  slot: e,
  clone: n,
  className: r,
  style: s
}, o) => {
  const t = P(), [l, i] = z([]);
  return j(() => {
    var _;
    if (!t.current || !e)
      return;
    let c = e;
    function h() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(o, a), r && a.classList.add(...r.split(" ")), s) {
        const p = je(s);
        Object.keys(p).forEach((m) => {
          a.style[m] = p[m];
        });
      }
    }
    let d = null;
    if (n && window.MutationObserver) {
      let a = function() {
        var y, E, x;
        (y = t.current) != null && y.contains(c) && ((E = t.current) == null || E.removeChild(c));
        const {
          portals: m,
          clonedElement: S
        } = L(e);
        return c = S, i(m), c.style.display = "contents", h(), (x = t.current) == null || x.appendChild(c), m.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", h(), (_ = t.current) == null || _.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = t.current) != null && a.contains(c) && ((p = t.current) == null || p.removeChild(c)), d == null || d.disconnect();
    };
  }, [e, n, r, s, o]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Ae(e) {
  try {
    if (typeof e == "string") {
      let n = e.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function q(e) {
  return Z(() => Ae(e), [e]);
}
function Le({
  value: e,
  onValueChange: n
}) {
  const [r, s] = z(e), o = P(n);
  o.current = n;
  const t = P(r);
  return t.current = r, j(() => {
    o.current(r);
  }, [r]), j(() => {
    ne(e, t.current) || s(e);
  }, [e]), [r, s];
}
const Te = Oe(({
  slots: e,
  children: n,
  onValueChange: r,
  onChange: s,
  formatter: o,
  parser: t,
  elRef: l,
  ...i
}) => {
  const c = q(o), h = q(t), [d, _] = Le({
    onValueChange: r,
    value: i.value
  });
  return /* @__PURE__ */ f.jsxs(f.Fragment, {
    children: [/* @__PURE__ */ f.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ f.jsx(te, {
      ...i,
      ref: l,
      value: d,
      onChange: (a) => {
        s == null || s(a), _(a);
      },
      parser: h,
      formatter: c,
      controls: e["controls.upIcon"] || e["controls.downIcon"] ? {
        upIcon: e["controls.upIcon"] ? /* @__PURE__ */ f.jsx(w, {
          slot: e["controls.upIcon"]
        }) : typeof i.controls == "object" ? i.controls.upIcon : void 0,
        downIcon: e["controls.downIcon"] ? /* @__PURE__ */ f.jsx(w, {
          slot: e["controls.downIcon"]
        }) : typeof i.controls == "object" ? i.controls.downIcon : void 0
      } : i.controls,
      addonAfter: e.addonAfter ? /* @__PURE__ */ f.jsx(w, {
        slot: e.addonAfter
      }) : i.addonAfter,
      addonBefore: e.addonBefore ? /* @__PURE__ */ f.jsx(w, {
        slot: e.addonBefore
      }) : i.addonBefore,
      prefix: e.prefix ? /* @__PURE__ */ f.jsx(w, {
        slot: e.prefix
      }) : i.prefix,
      suffix: e.suffix ? /* @__PURE__ */ f.jsx(w, {
        slot: e.suffix
      }) : i.suffix
    })]
  });
});
export {
  Te as InputNumber,
  Te as default
};
