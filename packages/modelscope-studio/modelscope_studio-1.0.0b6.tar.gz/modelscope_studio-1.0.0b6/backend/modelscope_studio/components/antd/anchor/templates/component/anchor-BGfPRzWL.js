import { g as ee, w as C } from "./Index-CoZNOFpe.js";
const g = window.ms_globals.React, G = window.ms_globals.React.useMemo, Q = window.ms_globals.React.forwardRef, X = window.ms_globals.React.useRef, Z = window.ms_globals.React.useState, $ = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, te = window.ms_globals.antd.Anchor;
var U = {
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
var ne = g, re = Symbol.for("react.element"), le = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, se = ne.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, ce = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(n, e, s) {
  var r, l = {}, t = null, o = null;
  s !== void 0 && (t = "" + s), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (o = e.ref);
  for (r in e) oe.call(e, r) && !ce.hasOwnProperty(r) && (l[r] = e[r]);
  if (n && n.defaultProps) for (r in e = n.defaultProps, e) l[r] === void 0 && (l[r] = e[r]);
  return {
    $$typeof: re,
    type: n,
    key: t,
    ref: o,
    props: l,
    _owner: se.current
  };
}
S.Fragment = le;
S.jsx = H;
S.jsxs = H;
U.exports = S;
var E = U.exports;
const {
  SvelteComponent: ie,
  assign: j,
  binding_callbacks: A,
  check_outros: ae,
  children: q,
  claim_element: B,
  claim_space: ue,
  component_subscribe: L,
  compute_slots: de,
  create_slot: fe,
  detach: b,
  element: V,
  empty: T,
  exclude_internal_props: F,
  get_all_dirty_from_scope: _e,
  get_slot_changes: he,
  group_outros: pe,
  init: me,
  insert_hydration: R,
  safe_not_equal: ge,
  set_custom_element_data: J,
  space: we,
  transition_in: x,
  transition_out: O,
  update_slot_base: be
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ee,
  getContext: ye,
  onDestroy: ve,
  setContext: Ce
} = window.__gradio__svelte__internal;
function N(n) {
  let e, s;
  const r = (
    /*#slots*/
    n[7].default
  ), l = fe(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = V("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = B(t, "SVELTE-SLOT", {
        class: !0
      });
      var o = q(e);
      l && l.l(o), o.forEach(b), this.h();
    },
    h() {
      J(e, "class", "svelte-1rt0kpf");
    },
    m(t, o) {
      R(t, e, o), l && l.m(e, null), n[9](e), s = !0;
    },
    p(t, o) {
      l && l.p && (!s || o & /*$$scope*/
      64) && be(
        l,
        r,
        t,
        /*$$scope*/
        t[6],
        s ? he(
          r,
          /*$$scope*/
          t[6],
          o,
          null
        ) : _e(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      s || (x(l, t), s = !0);
    },
    o(t) {
      O(l, t), s = !1;
    },
    d(t) {
      t && b(e), l && l.d(t), n[9](null);
    }
  };
}
function Re(n) {
  let e, s, r, l, t = (
    /*$$slots*/
    n[4].default && N(n)
  );
  return {
    c() {
      e = V("react-portal-target"), s = we(), t && t.c(), r = T(), this.h();
    },
    l(o) {
      e = B(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), q(e).forEach(b), s = ue(o), t && t.l(o), r = T(), this.h();
    },
    h() {
      J(e, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      R(o, e, c), n[8](e), R(o, s, c), t && t.m(o, c), R(o, r, c), l = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? t ? (t.p(o, c), c & /*$$slots*/
      16 && x(t, 1)) : (t = N(o), t.c(), x(t, 1), t.m(r.parentNode, r)) : t && (pe(), O(t, 1, 1, () => {
        t = null;
      }), ae());
    },
    i(o) {
      l || (x(t), l = !0);
    },
    o(o) {
      O(t), l = !1;
    },
    d(o) {
      o && (b(e), b(s), b(r)), n[8](null), t && t.d(o);
    }
  };
}
function W(n) {
  const {
    svelteInit: e,
    ...s
  } = n;
  return s;
}
function xe(n, e, s) {
  let r, l, {
    $$slots: t = {},
    $$scope: o
  } = e;
  const c = de(t);
  let {
    svelteInit: i
  } = e;
  const p = C(W(e)), u = C();
  L(n, u, (d) => s(0, r = d));
  const f = C();
  L(n, f, (d) => s(1, l = d));
  const a = [], _ = ye("$$ms-gr-react-wrapper"), {
    slotKey: h,
    slotIndex: m,
    subSlotIndex: w
  } = ee() || {}, y = i({
    parent: _,
    props: p,
    target: u,
    slot: f,
    slotKey: h,
    slotIndex: m,
    subSlotIndex: w,
    onDestroy(d) {
      a.push(d);
    }
  });
  Ce("$$ms-gr-react-wrapper", y), Ee(() => {
    p.set(W(e));
  }), ve(() => {
    a.forEach((d) => d());
  });
  function v(d) {
    A[d ? "unshift" : "push"](() => {
      r = d, u.set(r);
    });
  }
  function K(d) {
    A[d ? "unshift" : "push"](() => {
      l = d, f.set(l);
    });
  }
  return n.$$set = (d) => {
    s(17, e = j(j({}, e), F(d))), "svelteInit" in d && s(5, i = d.svelteInit), "$$scope" in d && s(6, o = d.$$scope);
  }, e = F(e), [r, l, u, f, c, i, o, t, v, K];
}
class Se extends ie {
  constructor(e) {
    super(), me(this, e, xe, Re, ge, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, k = window.ms_globals.tree;
function ke(n) {
  function e(s) {
    const r = C(), l = new Se({
      ...s,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const o = {
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
          }, c = t.parent ?? k;
          return c.nodes = [...c.nodes, o], D({
            createPortal: I,
            node: k
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== r), D({
              createPortal: I,
              node: k
            });
          }), o;
        },
        ...s.props
      }
    });
    return r.set(l), l;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(e);
    });
  });
}
function Ie(n) {
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
function M(n) {
  return G(() => Ie(n), [n]);
}
const Oe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Pe(n) {
  return n ? Object.keys(n).reduce((e, s) => {
    const r = n[s];
    return typeof r == "number" && !Oe.includes(s) ? e[s] = r + "px" : e[s] = r, e;
  }, {}) : {};
}
function P(n) {
  const e = [], s = n.cloneNode(!1);
  if (n._reactElement)
    return e.push(I(g.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: g.Children.toArray(n._reactElement.props.children).map((l) => {
        if (g.isValidElement(l) && l.props.__slot__) {
          const {
            portals: t,
            clonedElement: o
          } = P(l.props.el);
          return g.cloneElement(l, {
            ...l.props,
            el: o,
            children: [...g.Children.toArray(l.props.children), ...t]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: e
    };
  Object.keys(n.getEventListeners()).forEach((l) => {
    n.getEventListeners(l).forEach(({
      listener: o,
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, o, i);
    });
  });
  const r = Array.from(n.childNodes);
  for (let l = 0; l < r.length; l++) {
    const t = r[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = P(t);
      e.push(...c), s.appendChild(o);
    } else t.nodeType === 3 && s.appendChild(t.cloneNode());
  }
  return {
    clonedElement: s,
    portals: e
  };
}
function je(n, e) {
  n && (typeof n == "function" ? n(e) : n.current = e);
}
const z = Q(({
  slot: n,
  clone: e,
  className: s,
  style: r
}, l) => {
  const t = X(), [o, c] = Z([]);
  return $(() => {
    var f;
    if (!t.current || !n)
      return;
    let i = n;
    function p() {
      let a = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (a = i.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), je(l, a), s && a.classList.add(...s.split(" ")), r) {
        const _ = Pe(r);
        Object.keys(_).forEach((h) => {
          a.style[h] = _[h];
        });
      }
    }
    let u = null;
    if (e && window.MutationObserver) {
      let a = function() {
        var w, y, v;
        (w = t.current) != null && w.contains(i) && ((y = t.current) == null || y.removeChild(i));
        const {
          portals: h,
          clonedElement: m
        } = P(n);
        return i = m, c(h), i.style.display = "contents", p(), (v = t.current) == null || v.appendChild(i), h.length > 0;
      };
      a() || (u = new window.MutationObserver(() => {
        a() && (u == null || u.disconnect());
      }), u.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", p(), (f = t.current) == null || f.appendChild(i);
    return () => {
      var a, _;
      i.style.display = "", (a = t.current) != null && a.contains(i) && ((_ = t.current) == null || _.removeChild(i)), u == null || u.disconnect();
    };
  }, [n, e, s, r, l]), g.createElement("react-child", {
    ref: t,
    style: {
      display: "contents"
    }
  }, ...o);
});
function Y(n, e, s) {
  return n.filter(Boolean).map((r, l) => {
    var i;
    if (typeof r != "object")
      return e != null && e.fallback ? e.fallback(r) : r;
    const t = {
      ...r.props,
      key: ((i = r.props) == null ? void 0 : i.key) ?? (s ? `${s}-${l}` : `${l}`)
    };
    let o = t;
    Object.keys(r.slots).forEach((p) => {
      if (!r.slots[p] || !(r.slots[p] instanceof Element) && !r.slots[p].el)
        return;
      const u = p.split(".");
      u.forEach((m, w) => {
        o[m] || (o[m] = {}), w !== u.length - 1 && (o = t[m]);
      });
      const f = r.slots[p];
      let a, _, h = (e == null ? void 0 : e.clone) ?? !1;
      f instanceof Element ? a = f : (a = f.el, _ = f.callback, h = f.clone ?? !1), o[u[u.length - 1]] = a ? _ ? (...m) => (_(u[u.length - 1], m), /* @__PURE__ */ E.jsx(z, {
        slot: a,
        clone: h
      })) : /* @__PURE__ */ E.jsx(z, {
        slot: a,
        clone: h
      }) : o[u[u.length - 1]], o = t;
    });
    const c = (e == null ? void 0 : e.children) || "children";
    return r[c] && (t[c] = Y(r[c], e, `${l}`)), t;
  });
}
const Le = ke(({
  getContainer: n,
  getCurrentAnchor: e,
  children: s,
  items: r,
  slotItems: l,
  ...t
}) => {
  const o = M(n), c = M(e);
  return /* @__PURE__ */ E.jsxs(E.Fragment, {
    children: [s, /* @__PURE__ */ E.jsx(te, {
      ...t,
      items: G(() => r || Y(l, {
        clone: !0
      }), [r, l]),
      getContainer: o,
      getCurrentAnchor: c
    })]
  });
});
export {
  Le as Anchor,
  Le as default
};
