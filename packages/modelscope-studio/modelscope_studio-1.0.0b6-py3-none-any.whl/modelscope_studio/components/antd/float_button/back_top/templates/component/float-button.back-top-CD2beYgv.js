import { g as Z, w as C } from "./Index-DwjjiUjq.js";
const h = window.ms_globals.React, V = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.FloatButton;
var M = {
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
var ee = h, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, re = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function z(n, t, s) {
  var r, o = {}, e = null, l = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (l = t.ref);
  for (r in t) oe.call(t, r) && !se.hasOwnProperty(r) && (o[r] = t[r]);
  if (n && n.defaultProps) for (r in t = n.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: te,
    type: n,
    key: e,
    ref: l,
    props: o,
    _owner: re.current
  };
}
S.Fragment = ne;
S.jsx = z;
S.jsxs = z;
M.exports = S;
var p = M.exports;
const {
  SvelteComponent: le,
  assign: T,
  binding_callbacks: L,
  check_outros: ie,
  children: G,
  claim_element: U,
  claim_space: ce,
  component_subscribe: F,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: H,
  empty: N,
  exclude_internal_props: A,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: pe,
  insert_hydration: x,
  safe_not_equal: me,
  set_custom_element_data: K,
  space: he,
  transition_in: R,
  transition_out: P,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: be,
  onDestroy: ye,
  setContext: Ee
} = window.__gradio__svelte__internal;
function W(n) {
  let t, s;
  const r = (
    /*#slots*/
    n[7].default
  ), o = ue(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = H("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = U(e, "SVELTE-SLOT", {
        class: !0
      });
      var l = G(t);
      o && o.l(l), l.forEach(g), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(e, l) {
      x(e, t, l), o && o.m(t, null), n[9](t), s = !0;
    },
    p(e, l) {
      o && o.p && (!s || l & /*$$scope*/
      64) && ge(
        o,
        r,
        e,
        /*$$scope*/
        e[6],
        s ? fe(
          r,
          /*$$scope*/
          e[6],
          l,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (R(o, e), s = !0);
    },
    o(e) {
      P(o, e), s = !1;
    },
    d(e) {
      e && g(t), o && o.d(e), n[9](null);
    }
  };
}
function ve(n) {
  let t, s, r, o, e = (
    /*$$slots*/
    n[4].default && W(n)
  );
  return {
    c() {
      t = H("react-portal-target"), s = he(), e && e.c(), r = N(), this.h();
    },
    l(l) {
      t = U(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), G(t).forEach(g), s = ce(l), e && e.l(l), r = N(), this.h();
    },
    h() {
      K(t, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      x(l, t, c), n[8](t), x(l, s, c), e && e.m(l, c), x(l, r, c), o = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? e ? (e.p(l, c), c & /*$$slots*/
      16 && R(e, 1)) : (e = W(l), e.c(), R(e, 1), e.m(r.parentNode, r)) : e && (_e(), P(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(l) {
      o || (R(e), o = !0);
    },
    o(l) {
      P(e), o = !1;
    },
    d(l) {
      l && (g(t), g(s), g(r)), n[8](null), e && e.d(l);
    }
  };
}
function B(n) {
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
  const c = ae(e);
  let {
    svelteInit: i
  } = t;
  const w = C(B(t)), d = C();
  F(n, d, (a) => s(0, r = a));
  const m = C();
  F(n, m, (a) => s(1, o = a));
  const u = [], f = be("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: I,
    subSlotIndex: b
  } = Z() || {}, y = i({
    parent: f,
    props: w,
    target: d,
    slot: m,
    slotKey: _,
    slotIndex: I,
    subSlotIndex: b,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", y), we(() => {
    w.set(B(t));
  }), ye(() => {
    u.forEach((a) => a());
  });
  function E(a) {
    L[a ? "unshift" : "push"](() => {
      r = a, d.set(r);
    });
  }
  function q(a) {
    L[a ? "unshift" : "push"](() => {
      o = a, m.set(o);
    });
  }
  return n.$$set = (a) => {
    s(17, t = T(T({}, t), A(a))), "svelteInit" in a && s(5, i = a.svelteInit), "$$scope" in a && s(6, l = a.$$scope);
  }, t = A(t), [r, o, d, m, c, i, l, e, E, q];
}
class xe extends le {
  constructor(t) {
    super(), pe(this, t, Ce, ve, me, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, k = window.ms_globals.tree;
function Re(n) {
  function t(s) {
    const r = C(), o = new xe({
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
          }, c = e.parent ?? k;
          return c.nodes = [...c.nodes, l], D({
            createPortal: O,
            node: k
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== r), D({
              createPortal: O,
              node: k
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
const Se = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(n) {
  return n ? Object.keys(n).reduce((t, s) => {
    const r = n[s];
    return typeof r == "number" && !Se.includes(s) ? t[s] = r + "px" : t[s] = r, t;
  }, {}) : {};
}
function j(n) {
  const t = [], s = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(O(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((o) => {
        if (h.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: l
          } = j(o.props.el);
          return h.cloneElement(o, {
            ...o.props,
            el: l,
            children: [...h.Children.toArray(o.props.children), ...e]
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
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, l, i);
    });
  });
  const r = Array.from(n.childNodes);
  for (let o = 0; o < r.length; o++) {
    const e = r[o];
    if (e.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = j(e);
      t.push(...c), s.appendChild(l);
    } else e.nodeType === 3 && s.appendChild(e.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function ke(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const v = V(({
  slot: n,
  clone: t,
  className: s,
  style: r
}, o) => {
  const e = J(), [l, c] = Y([]);
  return Q(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function w() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ke(o, u), s && u.classList.add(...s.split(" ")), r) {
        const f = Ie(r);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var b, y, E;
        (b = e.current) != null && b.contains(i) && ((y = e.current) == null || y.removeChild(i));
        const {
          portals: _,
          clonedElement: I
        } = j(n);
        return i = I, c(_), i.style.display = "contents", w(), (E = e.current) == null || E.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", w(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, s, r, o]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...l);
});
function Oe(n) {
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
function Pe(n) {
  return X(() => Oe(n), [n]);
}
const Te = Re(({
  slots: n,
  children: t,
  target: s,
  ...r
}) => {
  var e;
  const o = Pe(s);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ p.jsx($.BackTop, {
      ...r,
      target: o,
      icon: n.icon ? /* @__PURE__ */ p.jsx(v, {
        clone: !0,
        slot: n.icon
      }) : r.icon,
      description: n.description ? /* @__PURE__ */ p.jsx(v, {
        clone: !0,
        slot: n.description
      }) : r.description,
      tooltip: n.tooltip ? /* @__PURE__ */ p.jsx(v, {
        clone: !0,
        slot: n.tooltip
      }) : r.tooltip,
      badge: {
        ...r.badge,
        count: n["badge.count"] ? /* @__PURE__ */ p.jsx(v, {
          slot: n["badge.count"]
        }) : (e = r.badge) == null ? void 0 : e.count
      }
    })]
  });
});
export {
  Te as FloatButtonBackTop,
  Te as default
};
