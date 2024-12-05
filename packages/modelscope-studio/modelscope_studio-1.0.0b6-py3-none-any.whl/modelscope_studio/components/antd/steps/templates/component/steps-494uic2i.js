import { g as $, w as S } from "./Index-BkXWCeS9.js";
const g = window.ms_globals.React, z = window.ms_globals.React.useMemo, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, O = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Steps;
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
var te = g, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, t, s) {
  var r, o = {}, e = null, l = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t) oe.call(t, r) && !le.hasOwnProperty(r) && (o[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: ne,
    type: n,
    key: e,
    ref: l,
    props: o,
    _owner: se.current
  };
}
R.Fragment = re;
R.jsx = U;
R.jsxs = U;
G.exports = R;
var w = G.exports;
const {
  SvelteComponent: ie,
  assign: L,
  binding_callbacks: T,
  check_outros: ce,
  children: H,
  claim_element: q,
  claim_space: ae,
  component_subscribe: N,
  compute_slots: ue,
  create_slot: de,
  detach: E,
  element: B,
  empty: A,
  exclude_internal_props: D,
  get_all_dirty_from_scope: fe,
  get_slot_changes: pe,
  group_outros: _e,
  init: he,
  insert_hydration: C,
  safe_not_equal: me,
  set_custom_element_data: V,
  space: ge,
  transition_in: x,
  transition_out: k,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function F(n) {
  let t, s;
  const r = (
    /*#slots*/
    n[7].default
  ), o = de(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = B("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = q(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = H(t);
      o && o.l(l), l.forEach(E), this.h();
    },
    h() {
      V(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      C(e, t, l), o && o.m(t, null), n[9](t), s = !0;
    },
    p(e, l) {
      o && o.p && (!s || l & /*$$scope*/
      64) && we(
        o,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? pe(
          r,
          /*$$scope*/
          e[6],
          l,
          null
        ) : fe(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (x(o, e), s = !0);
    },
    o(e) {
      k(o, e), s = !1;
    },
    d(e) {
      e && E(t), o && o.d(e), n[9](null);
    }
  };
}
function Se(n) {
  let t, s, r, o, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = B("react-portal-target"), s = ge(), e && e.c(), r = A(), this.h();
    },
    l(l) {
      t = q(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(t).forEach(E), s = ae(l), e && e.l(l), r = A(), this.h();
    },
    h() {
      V(t, "class", "svelte-1rt0kpf");
    },
    m(l, i) {
      C(l, t, i), n[8](t), C(l, s, i), e && e.m(l, i), C(l, r, i), o = !0;
    },
    p(l, [i]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, i), i & /*$$slots*/
      16 && x(e, 1)) : (e = F(l), e.c(), x(e, 1), e.m(r.parentNode, r)) : e && (_e(), k(e, 1, 1, () => {
        e = null;
      }), ce());
    },
    i(l) {
      o || (x(e), o = !0);
    },
    o(l) {
      k(e), o = !1;
    },
    d(l) {
      l && (E(t), E(s), E(r)), n[8](null), e && e.d(l);
    }
  };
}
function W(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function Ce(n, t, s) {
  let r, o, {
    $$slots: e = {},
    $$scope: l
  } = t;
  const i = ue(e);
  let {
    svelteInit: c
  } = t;
  const h = S(W(t)), u = S();
  N(n, u, (d) => s(0, r = d));
  const f = S();
  N(n, f, (d) => s(1, o = d));
  const a = [], p = Ee("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: m,
    subSlotIndex: b
  } = $() || {}, y = c({
    parent: p,
    props: h,
    target: u,
    slot: f,
    slotKey: _,
    slotIndex: m,
    subSlotIndex: b,
    onDestroy(d) {
      a.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", y), be(() => {
    h.set(W(t));
  }), ye(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    T[d ? "unshift" : "push"](() => {
      r = d, u.set(r);
    });
  }
  function Y(d) {
    T[d ? "unshift" : "push"](() => {
      o = d, f.set(o);
    });
  }
  return n.$$set = (d) => {
    s(17, t = L(L({}, t), D(d))), "svelteInit" in d && s(5, c = d.svelteInit), "$$scope" in d && s(6, l = d.$$scope);
  }, t = D(t), [r, o, u, f, i, c, l, e, v, Y];
}
class xe extends ie {
  constructor(t) {
    super(), he(this, t, Ce, Se, me, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, I = window.ms_globals.tree;
function Re(n) {
  function t(s) {
    const r = S(), o = new xe({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: n,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, i = e.parent ?? I;
          return i.nodes = [...i.nodes, l], M({
            createPortal: O,
            node: I
          }), e.onDestroy(() => {
            i.nodes = i.nodes.filter((c) => c.svelteInstance !== r), M({
              createPortal: O,
              node: I
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
      s(t);
    });
  });
}
function Ie(n) {
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
function Oe(n) {
  return z(() => Ie(n), [n]);
}
const ke = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const r = n[s];
    return typeof r == "number" && !ke.includes(s) ? t[s] = r + "px" : t[s] = r, t;
  }, {}) : {};
}
function P(n) {
  const t = [], s = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(O(g.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: g.Children.toArray(n._reactElement.props.children).map((o) => {
        if (g.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = P(o.props.el);
          return g.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...g.Children.toArray(o.props.children), ...e]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((o) => {
    n.getEventListeners(o).forEach(({
      listener: l,
      type: i,
      useCapture: c
    }) => {
      s.addEventListener(i, l, c);
    });
  });
  const r = Array.from(n.childNodes);
  for (let o = 0; o < r.length; o++) {
    const e = r[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: i
      } = P(e);
      t.push(...i), s.appendChild(l);
    } else e.nodeType === 3 && s.appendChild(e.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function je(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const j = K(({
  slot: n,
  clone: t,
  className: s,
  style: r
}, o) => {
  const e = Q(), [l, i] = X([]);
  return Z(() => {
    var f;
    if (!e.current || !n)
      return;
    let c = n;
    function h() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), je(o, a), s && a.classList.add(...s.split(" ")), r) {
        const p = Pe(r);
        Object.keys(p).forEach((_) => {
          a.style[_] = p[_];
        });
      }
    }
    let u = null;
    if (t && window.MutationObserver) {
      let a = function() {
        var b, y, v;
        (b = e.current) != null && b.contains(c) && ((y = e.current) == null || y.removeChild(c));
        const {
          portals: _,
          clonedElement: m
        } = P(n);
        return c = m, i(_), c.style.display = "contents", h(), (v = e.current) == null || v.appendChild(c), _.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", h(), (f = e.current) == null || f.appendChild(c);
    return () => {
      var a, p;
      c.style.display = "", (a = e.current) != null && a.contains(c) && ((p = e.current) == null || p.removeChild(c)), u == null || u.disconnect();
    };
  }, [n, t, s, r, o]), g.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function J(n, t, s) {
  return n.filter(Boolean).map((r, o) => {
    var c;
    if (typeof r != "object")
      return r;
    const e = {
      ...r.props,
      key: ((c = r.props) == null ? void 0 : c.key) ?? (s ? `${s}-${o}` : `${o}`)
    };
    let l = e;
    Object.keys(r.slots).forEach((h) => {
      if (!r.slots[h] || !(r.slots[h] instanceof Element) && !r.slots[h].el)
        return;
      const u = h.split(".");
      u.forEach((m, b) => {
        l[m] || (l[m] = {}), b !== u.length - 1 && (l = e[m]);
      });
      const f = r.slots[h];
      let a, p, _ = !1;
      f instanceof Element ? a = f : (a = f.el, p = f.callback, _ = f.clone ?? !1), l[u[u.length - 1]] = a ? p ? (...m) => (p(u[u.length - 1], m), /* @__PURE__ */ w.jsx(j, {
        slot: a,
        clone: _
      })) : /* @__PURE__ */ w.jsx(j, {
        slot: a,
        clone: _
      }) : l[u[u.length - 1]], l = e;
    });
    const i = "children";
    return r[i] && (e[i] = J(r[i], t, `${o}`)), e;
  });
}
function Le(n, t) {
  return n ? /* @__PURE__ */ w.jsx(j, {
    slot: n,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function Te({
  key: n,
  setSlotParams: t,
  slots: s
}, r) {
  return s[n] ? (...o) => (t(n, o), Le(s[n], {
    clone: !0,
    ...r
  })) : void 0;
}
const Ae = Re(({
  slots: n,
  items: t,
  slotItems: s,
  setSlotParams: r,
  children: o,
  progressDot: e,
  ...l
}) => {
  const i = Oe(e);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: o
    }), /* @__PURE__ */ w.jsx(ee, {
      ...l,
      items: z(() => t || J(s), [t, s]),
      progressDot: n.progressDot ? Te({
        slots: n,
        setSlotParams: r,
        key: "progressDot"
      }, {
        clone: !0
      }) : i || e
    })]
  });
});
export {
  Ae as Steps,
  Ae as default
};
