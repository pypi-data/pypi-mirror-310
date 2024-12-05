import { g as $, w as S } from "./Index-BLMwwNWV.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, z = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Slider;
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
var te = h, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(r, e, n) {
  var l, o = {}, t = null, s = null;
  n !== void 0 && (t = "" + n), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (l in e) oe.call(e, l) && !le.hasOwnProperty(l) && (o[l] = e[l]);
  if (r && r.defaultProps) for (l in e = r.defaultProps, e) o[l] === void 0 && (o[l] = e[l]);
  return {
    $$typeof: ne,
    type: r,
    key: t,
    ref: s,
    props: o,
    _owner: se.current
  };
}
R.Fragment = re;
R.jsx = H;
R.jsxs = H;
U.exports = R;
var g = U.exports;
const {
  SvelteComponent: ie,
  assign: T,
  binding_callbacks: F,
  check_outros: ce,
  children: K,
  claim_element: q,
  claim_space: ae,
  component_subscribe: N,
  compute_slots: ue,
  create_slot: de,
  detach: w,
  element: V,
  empty: A,
  exclude_internal_props: v,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: me,
  insert_hydration: C,
  safe_not_equal: he,
  set_custom_element_data: B,
  space: ge,
  transition_in: x,
  transition_out: k,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: ye,
  onDestroy: Ee,
  setContext: Se
} = window.__gradio__svelte__internal;
function W(r) {
  let e, n;
  const l = (
    /*#slots*/
    r[7].default
  ), o = de(
    l,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      e = V("svelte-slot"), o && o.c(), this.h();
    },
    l(t) {
      e = q(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = K(e);
      o && o.l(s), s.forEach(w), this.h();
    },
    h() {
      B(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      C(t, e, s), o && o.m(e, null), r[9](e), n = !0;
    },
    p(t, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && we(
        o,
        l,
        t,
        /*$$scope*/
        t[6],
        n ? pe(
          l,
          /*$$scope*/
          t[6],
          s,
          null
        ) : fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      n || (x(o, t), n = !0);
    },
    o(t) {
      k(o, t), n = !1;
    },
    d(t) {
      t && w(e), o && o.d(t), r[9](null);
    }
  };
}
function Ce(r) {
  let e, n, l, o, t = (
    /*$$slots*/
    r[4].default && W(r)
  );
  return {
    c() {
      e = V("react-portal-target"), n = ge(), t && t.c(), l = A(), this.h();
    },
    l(s) {
      e = q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), K(e).forEach(w), n = ae(s), t && t.l(s), l = A(), this.h();
    },
    h() {
      B(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      C(s, e, c), r[8](e), C(s, n, c), t && t.m(s, c), C(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && x(t, 1)) : (t = W(s), t.c(), x(t, 1), t.m(l.parentNode, l)) : t && (_e(), k(t, 1, 1, () => {
        t = null;
      }), ce());
    },
    i(s) {
      o || (x(t), o = !0);
    },
    o(s) {
      k(t), o = !1;
    },
    d(s) {
      s && (w(e), w(n), w(l)), r[8](null), t && t.d(s);
    }
  };
}
function D(r) {
  const {
    svelteInit: e,
    ...n
  } = r;
  return n;
}
function xe(r, e, n) {
  let l, o, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = ue(t);
  let {
    svelteInit: i
  } = e;
  const m = S(D(e)), d = S();
  N(r, d, (u) => n(0, l = u));
  const _ = S();
  N(r, _, (u) => n(1, o = u));
  const a = [], p = ye("$$ms-gr-react-wrapper"), {
    slotKey: f,
    slotIndex: P,
    subSlotIndex: b
  } = $() || {}, y = i({
    parent: p,
    props: m,
    target: d,
    slot: _,
    slotKey: f,
    slotIndex: P,
    subSlotIndex: b,
    onDestroy(u) {
      a.push(u);
    }
  });
  Se("$$ms-gr-react-wrapper", y), be(() => {
    m.set(D(e));
  }), Ee(() => {
    a.forEach((u) => u());
  });
  function E(u) {
    F[u ? "unshift" : "push"](() => {
      l = u, d.set(l);
    });
  }
  function J(u) {
    F[u ? "unshift" : "push"](() => {
      o = u, _.set(o);
    });
  }
  return r.$$set = (u) => {
    n(17, e = T(T({}, e), v(u))), "svelteInit" in u && n(5, i = u.svelteInit), "$$scope" in u && n(6, s = u.$$scope);
  }, e = v(e), [l, o, d, _, c, i, s, t, E, J];
}
class Re extends ie {
  constructor(e) {
    super(), me(this, e, xe, Ce, he, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, I = window.ms_globals.tree;
function Pe(r) {
  function e(n) {
    const l = S(), o = new Re({
      ...n,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: r,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? I;
          return c.nodes = [...c.nodes, s], M({
            createPortal: O,
            node: I
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), M({
              createPortal: O,
              node: I
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
      n(e);
    });
  });
}
const Ie = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Oe(r) {
  return r ? Object.keys(r).reduce((e, n) => {
    const l = r[n];
    return typeof l == "number" && !Ie.includes(n) ? e[n] = l + "px" : e[n] = l, e;
  }, {}) : {};
}
function j(r) {
  const e = [], n = r.cloneNode(!1);
  if (r._reactElement)
    return e.push(O(h.cloneElement(r._reactElement, {
      ...r._reactElement.props,
      children: h.Children.toArray(r._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = j(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...h.Children.toArray(o.props.children), ...t]
          });
        }
        return null;
      })
    }), n)), {
      clonedElement: n,
      portals: e
    };
  Object.keys(r.getEventListeners()).forEach((o) => {
    r.getEventListeners(o).forEach(({
      listener: s,
      type: c,
      useCapture: i
    }) => {
      n.addEventListener(c, s, i);
    });
  });
  const l = Array.from(r.childNodes);
  for (let o = 0; o < l.length; o++) {
    const t = l[o];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: c
      } = j(t);
      e.push(...c), n.appendChild(s);
    } else t.nodeType === 3 && n.appendChild(t.cloneNode());
  }
  return {
    clonedElement: n,
    portals: e
  };
}
function ke(r, e) {
  r && (typeof r == "function" ? r(e) : r.current = e);
}
const L = Y(({
  slot: r,
  clone: e,
  className: n,
  style: l
}, o) => {
  const t = Q(), [s, c] = X([]);
  return Z(() => {
    var _;
    if (!t.current || !r)
      return;
    let i = r;
    function m() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), ke(o, a), n && a.classList.add(...n.split(" ")), l) {
        const p = Oe(l);
        Object.keys(p).forEach((f) => {
          a.style[f] = p[f];
        });
      }
    }
    let d = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var b, y, E;
        (b = t.current) != null && b.contains(i) && ((y = t.current) == null || y.removeChild(i));
        const {
          portals: f,
          clonedElement: P
        } = j(r);
        return i = P, c(f), i.style.display = "contents", m(), (E = t.current) == null || E.appendChild(i), f.length > 0;
      };
      a() || (d = new window.MutationObserver(() => {
        a() && (d == null || d.disconnect());
      }), d.observe(r, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", m(), (_ = t.current) == null || _.appendChild(i);
    return () => {
      var a, p;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((p = t.current) == null || p.removeChild(i)), d == null || d.disconnect();
    };
  }, [r, e, n, l, o]), h.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function je(r) {
  try {
    if (typeof r == "string") {
      let e = r.trim();
      return e.startsWith(";") && (e = e.slice(1)), e.endsWith(";") && (e = e.slice(0, -1)), new Function(`return (...args) => (${e})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function G(r) {
  return z(() => je(r), [r]);
}
function Le(r, e) {
  return r ? /* @__PURE__ */ g.jsx(L, {
    slot: r,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Te({
  key: r,
  setSlotParams: e,
  slots: n
}, l) {
  return n[r] ? (...o) => (e(r, o), Le(n[r], {
    clone: !0,
    ...l
  })) : void 0;
}
const Fe = (r) => r.reduce((e, n) => {
  const l = n == null ? void 0 : n.props.number;
  return l !== void 0 && (e[l] = (n == null ? void 0 : n.slots.label) instanceof Element ? {
    ...n.props,
    label: /* @__PURE__ */ g.jsx(L, {
      slot: n == null ? void 0 : n.slots.label
    })
  } : (n == null ? void 0 : n.slots.children) instanceof Element ? /* @__PURE__ */ g.jsx(L, {
    slot: n == null ? void 0 : n.slots.children
  }) : {
    ...n == null ? void 0 : n.props
  }), e;
}, {}), Ae = Pe(({
  marks: r,
  markItems: e,
  children: n,
  onValueChange: l,
  onChange: o,
  elRef: t,
  tooltip: s,
  step: c,
  slots: i,
  setSlotParams: m,
  ...d
}) => {
  const _ = (f) => {
    o == null || o(f), l(f);
  }, a = G(s == null ? void 0 : s.getPopupContainer), p = G(s == null ? void 0 : s.formatter);
  return /* @__PURE__ */ g.jsxs(g.Fragment, {
    children: [/* @__PURE__ */ g.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ g.jsx(ee, {
      ...d,
      tooltip: {
        ...s,
        getPopupContainer: a,
        formatter: i["tooltip.formatter"] ? Te({
          key: "tooltip.formatter",
          setSlotParams: m,
          slots: i
        }) : p
      },
      marks: z(() => r || Fe(e), [e, r]),
      step: c === void 0 ? null : c,
      ref: t,
      onChange: _
    })]
  });
});
export {
  Ae as Slider,
  Ae as default
};
