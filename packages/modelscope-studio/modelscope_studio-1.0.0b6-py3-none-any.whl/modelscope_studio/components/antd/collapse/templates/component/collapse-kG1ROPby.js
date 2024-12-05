import { g as $, w as x } from "./Index-DUKgOyNn.js";
const g = window.ms_globals.React, z = window.ms_globals.React.useMemo, K = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, Z = window.ms_globals.React.useEffect, k = window.ms_globals.ReactDOM.createPortal, ee = window.ms_globals.antd.Collapse;
var G = {
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
var te = g, ne = Symbol.for("react.element"), re = Symbol.for("react.fragment"), le = Object.prototype.hasOwnProperty, oe = te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function U(n, e, o) {
  var r, l = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (r in e) le.call(e, r) && !se.hasOwnProperty(r) && (l[r] = e[r]);
  if (n && n.defaultProps) for (r in e = n.defaultProps, e) l[r] === void 0 && (l[r] = e[r]);
  return {
    $$typeof: ne,
    type: n,
    key: t,
    ref: s,
    props: l,
    _owner: oe.current
  };
}
S.Fragment = re;
S.jsx = U;
S.jsxs = U;
G.exports = S;
var E = G.exports;
const {
  SvelteComponent: ce,
  assign: L,
  binding_callbacks: T,
  check_outros: ae,
  children: H,
  claim_element: q,
  claim_space: ie,
  component_subscribe: N,
  compute_slots: ue,
  create_slot: de,
  detach: b,
  element: B,
  empty: A,
  exclude_internal_props: F,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: pe,
  init: he,
  insert_hydration: C,
  safe_not_equal: me,
  set_custom_element_data: V,
  space: ge,
  transition_in: I,
  transition_out: O,
  update_slot_base: we
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: Ee,
  onDestroy: ye,
  setContext: ve
} = window.__gradio__svelte__internal;
function W(n) {
  let e, o;
  const r = (
    /*#slots*/
    n[7].default
  ), l = de(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = B("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = q(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = H(e);
      l && l.l(s), s.forEach(b), this.h();
    },
    h() {
      V(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      C(t, e, s), l && l.m(e, null), n[9](e), o = !0;
    },
    p(t, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && we(
        l,
        r,
        t,
        /*$$scope*/
        t[6],
        o ? _e(
          r,
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
      o || (I(l, t), o = !0);
    },
    o(t) {
      O(l, t), o = !1;
    },
    d(t) {
      t && b(e), l && l.d(t), n[9](null);
    }
  };
}
function xe(n) {
  let e, o, r, l, t = (
    /*$$slots*/
    n[4].default && W(n)
  );
  return {
    c() {
      e = B("react-portal-target"), o = ge(), t && t.c(), r = A(), this.h();
    },
    l(s) {
      e = q(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), H(e).forEach(b), o = ie(s), t && t.l(s), r = A(), this.h();
    },
    h() {
      V(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      C(s, e, a), n[8](e), C(s, o, a), t && t.m(s, a), C(s, r, a), l = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, a), a & /*$$slots*/
      16 && I(t, 1)) : (t = W(s), t.c(), I(t, 1), t.m(r.parentNode, r)) : t && (pe(), O(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(s) {
      l || (I(t), l = !0);
    },
    o(s) {
      O(t), l = !1;
    },
    d(s) {
      s && (b(e), b(o), b(r)), n[8](null), t && t.d(s);
    }
  };
}
function D(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function Ce(n, e, o) {
  let r, l, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const a = ue(t);
  let {
    svelteInit: c
  } = e;
  const f = x(D(e)), u = x();
  N(n, u, (d) => o(0, r = d));
  const _ = x();
  N(n, _, (d) => o(1, l = d));
  const i = [], p = Ee("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: m,
    subSlotIndex: w
  } = $() || {}, y = c({
    parent: p,
    props: f,
    target: u,
    slot: _,
    slotKey: h,
    slotIndex: m,
    subSlotIndex: w,
    onDestroy(d) {
      i.push(d);
    }
  });
  ve("$$ms-gr-react-wrapper", y), be(() => {
    f.set(D(e));
  }), ye(() => {
    i.forEach((d) => d());
  });
  function v(d) {
    T[d ? "unshift" : "push"](() => {
      r = d, u.set(r);
    });
  }
  function Y(d) {
    T[d ? "unshift" : "push"](() => {
      l = d, _.set(l);
    });
  }
  return n.$$set = (d) => {
    o(17, e = L(L({}, e), F(d))), "svelteInit" in d && o(5, c = d.svelteInit), "$$scope" in d && o(6, s = d.$$scope);
  }, e = F(e), [r, l, u, _, a, c, s, t, v, Y];
}
class Ie extends ce {
  constructor(e) {
    super(), he(this, e, Ce, xe, me, {
      svelteInit: 5
    });
  }
}
const M = window.ms_globals.rerender, R = window.ms_globals.tree;
function Se(n) {
  function e(o) {
    const r = x(), l = new Ie({
      ...o,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const s = {
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
          }, a = t.parent ?? R;
          return a.nodes = [...a.nodes, s], M({
            createPortal: k,
            node: R
          }), t.onDestroy(() => {
            a.nodes = a.nodes.filter((c) => c.svelteInstance !== r), M({
              createPortal: k,
              node: R
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
      o(e);
    });
  });
}
function Re(n) {
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
function ke(n) {
  return z(() => Re(n), [n]);
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((e, o) => {
    const r = n[o];
    return typeof r == "number" && !Oe.includes(o) ? e[o] = r + "px" : e[o] = r, e;
  }, {}) : {};
}
function P(n) {
  const e = [], o = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(k(g.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: g.Children.toArray(n._reactElement.props.children).map((l) => {
        if (g.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: s
          } = P(l.props.el);
          return g.cloneElement(l, {
            ...l.props,
            el: s,
            children: [...g.Children.toArray(l.props.children), ...t]
          });
        }
        return null;
      })
    }), o)), {
      clonedElement: o,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      o.addEventListener(a, s, c);
    });
  });
  const r = Array.from(n.childNodes);
  for (let l = 0; l < r.length; l++) {
    const t = r[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = P(t);
      e.push(...a), o.appendChild(s);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function je(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const j = K(({
  slot: n,
  clone: e,
  className: o,
  style: r
}, l) => {
  const t = Q(), [s, a] = X([]);
  return Z(() => {
    var _;
    if (!t.current || !n)
      return;
    let c = n;
    function f() {
      let i = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (i = c.children[0], i.tagName.toLowerCase() === "react-portal-target" && i.children[0] && (i = i.children[0])), je(l, i), o && i.classList.add(...o.split(" ")), r) {
        const p = Pe(r);
        Object.keys(p).forEach((h) => {
          i.style[h] = p[h];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let i = function() {
        var w, y, v;
        (w = t.current) != null && w.contains(c) && ((y = t.current) == null || y.removeChild(c));
        const {
          portals: h,
          clonedElement: m
        } = P(n);
        return c = m, a(h), c.style.display = "contents", f(), (v = t.current) == null || v.appendChild(c), h.length > 0;
      };
      i() || (u = new window.MutationObserver(() => {
        i() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      c.style.display = "contents", f(), (_ = t.current) == null || _.appendChild(c);
    return () => {
      var i, p;
      c.style.display = "", (i = t.current) != null && i.contains(c) && ((p = t.current) == null || p.removeChild(c)), u == null || u.disconnect();
    };
  }, [n, e, o, r, l]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...s);
});
function J(n, e, o) {
  return n.filter(Boolean).map((r, l) => {
    var c;
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const t = {
      ...r.props,
      key: ((c = r.props) == null ? void 0 : c.key) ?? (o ? `${o}-${l}` : `${l}`)
    };
    let s = t;
    Object.keys(r.slots).forEach((f) => {
      if (!r.slots[f] || !(r.slots[f] instanceof Element) && !r.slots[f].el)
        return;
      const u = f.split(".");
      u.forEach((m, w) => {
        s[m] || (s[m] = {}), w !== u.length - 1 && (s = t[m]);
      });
      const _ = r.slots[f];
      let i, p, h = (e == null ? void 0 : e.clone) ?? !1;
      _ instanceof Element ? i = _ : (i = _.el, p = _.callback, h = _.clone ?? !1), s[u[u.length - 1]] = i ? p ? (...m) => (p(u[u.length - 1], m), /* @__PURE__ */ E.jsx(j, {
        slot: i,
        clone: h
      })) : /* @__PURE__ */ E.jsx(j, {
        slot: i,
        clone: h
      }) : s[u[u.length - 1]], s = t;
    });
    const a = (e == null ? void 0 : e.children) || "children";
    return r[a] && (t[a] = J(r[a], e, `${l}`)), t;
  });
}
function Le(n, e) {
  return n ? /* @__PURE__ */ E.jsx(j, {
    slot: n,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function Te({
  key: n,
  setSlotParams: e,
  slots: o
}, r) {
  return o[n] ? (...l) => (e(n, l), Le(o[n], {
    clone: !0,
    ...r
  })) : void 0;
}
const Ae = Se(({
  slots: n,
  items: e,
  slotItems: o,
  children: r,
  onChange: l,
  setSlotParams: t,
  expandIcon: s,
  ...a
}) => {
  const c = ke(s);
  return /* @__PURE__ */ E.jsxs(E.Fragment, {
    children: [r, /* @__PURE__ */ E.jsx(ee, {
      ...a,
      onChange: (f) => {
        l == null || l(f);
      },
      expandIcon: n.expandIcon ? Te({
        slots: n,
        setSlotParams: t,
        key: "expandIcon"
      }) : c,
      items: z(() => e || J(o, {
        clone: !0
      }), [e, o])
    })]
  });
});
export {
  Ae as Collapse,
  Ae as default
};
