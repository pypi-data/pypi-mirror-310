import { g as Z, w as v } from "./Index-B8mjiASP.js";
const m = window.ms_globals.React, B = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Y = window.ms_globals.React.useState, Q = window.ms_globals.React.useEffect, X = window.ms_globals.React.useMemo, O = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.Tooltip;
var z = {
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
var ee = m, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), oe = Object.prototype.hasOwnProperty, re = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function G(n, t, r) {
  var l, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) oe.call(t, l) && !se.hasOwnProperty(l) && (o[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: te,
    type: n,
    key: e,
    ref: s,
    props: o,
    _owner: re.current
  };
}
S.Fragment = ne;
S.jsx = G;
S.jsxs = G;
z.exports = S;
var E = z.exports;
const {
  SvelteComponent: le,
  assign: T,
  binding_callbacks: L,
  check_outros: ie,
  children: U,
  claim_element: H,
  claim_space: ce,
  component_subscribe: j,
  compute_slots: ae,
  create_slot: ue,
  detach: h,
  element: K,
  empty: F,
  exclude_internal_props: N,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: pe,
  init: _e,
  insert_hydration: C,
  safe_not_equal: me,
  set_custom_element_data: q,
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
function A(n) {
  let t, r;
  const l = (
    /*#slots*/
    n[7].default
  ), o = ue(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = H(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = U(t);
      o && o.l(s), s.forEach(h), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      C(e, t, s), o && o.m(t, null), n[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && ge(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        r ? fe(
          l,
          /*$$scope*/
          e[6],
          s,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (R(o, e), r = !0);
    },
    o(e) {
      P(o, e), r = !1;
    },
    d(e) {
      e && h(t), o && o.d(e), n[9](null);
    }
  };
}
function ve(n) {
  let t, r, l, o, e = (
    /*$$slots*/
    n[4].default && A(n)
  );
  return {
    c() {
      t = K("react-portal-target"), r = he(), e && e.c(), l = F(), this.h();
    },
    l(s) {
      t = H(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(h), r = ce(s), e && e.l(s), l = F(), this.h();
    },
    h() {
      q(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      C(s, t, c), n[8](t), C(s, r, c), e && e.m(s, c), C(s, l, c), o = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && R(e, 1)) : (e = A(s), e.c(), R(e, 1), e.m(l.parentNode, l)) : e && (pe(), P(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(s) {
      o || (R(e), o = !0);
    },
    o(s) {
      P(e), o = !1;
    },
    d(s) {
      s && (h(t), h(r), h(l)), n[8](null), e && e.d(s);
    }
  };
}
function W(n) {
  const {
    svelteInit: t,
    ...r
  } = n;
  return r;
}
function Ce(n, t, r) {
  let l, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ae(e);
  let {
    svelteInit: i
  } = t;
  const g = v(W(t)), d = v();
  j(n, d, (a) => r(0, l = a));
  const _ = v();
  j(n, _, (a) => r(1, o = a));
  const u = [], f = be("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: x,
    subSlotIndex: w
  } = Z() || {}, b = i({
    parent: f,
    props: g,
    target: d,
    slot: _,
    slotKey: p,
    slotIndex: x,
    subSlotIndex: w,
    onDestroy(a) {
      u.push(a);
    }
  });
  Ee("$$ms-gr-react-wrapper", b), we(() => {
    g.set(W(t));
  }), ye(() => {
    u.forEach((a) => a());
  });
  function y(a) {
    L[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function V(a) {
    L[a ? "unshift" : "push"](() => {
      o = a, _.set(o);
    });
  }
  return n.$$set = (a) => {
    r(17, t = T(T({}, t), N(a))), "svelteInit" in a && r(5, i = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = N(t), [l, o, d, _, c, i, s, e, y, V];
}
class Re extends le {
  constructor(t) {
    super(), _e(this, t, Ce, ve, me, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, I = window.ms_globals.tree;
function Se(n) {
  function t(r) {
    const l = v(), o = new Re({
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
          }, c = e.parent ?? I;
          return c.nodes = [...c.nodes, s], D({
            createPortal: O,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), D({
              createPortal: O,
              node: I
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
const xe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ie(n) {
  return n ? Object.keys(n).reduce((t, r) => {
    const l = n[r];
    return typeof l == "number" && !xe.includes(r) ? t[r] = l + "px" : t[r] = l, t;
  }, {}) : {};
}
function k(n) {
  const t = [], r = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(O(m.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: m.Children.toArray(n._reactElement.props.children).map((o) => {
        if (m.isValidElement(o) && o.props.__slot__) {
          const {
            portals: e,
            clonedElement: s
          } = k(o.props.el);
          return m.cloneElement(o, {
            ...o.props,
            el: s,
            children: [...m.Children.toArray(o.props.children), ...e]
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
      } = k(e);
      t.push(...c), r.appendChild(s);
    } else e.nodeType === 3 && r.appendChild(e.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function Oe(n, t) {
  n && (typeof n == "function" ? n(t) : n.current = t);
}
const Pe = B(({
  slot: n,
  clone: t,
  className: r,
  style: l
}, o) => {
  const e = J(), [s, c] = Y([]);
  return Q(() => {
    var _;
    if (!e.current || !n)
      return;
    let i = n;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), Oe(o, u), r && u.classList.add(...r.split(" ")), l) {
        const f = Ie(l);
        Object.keys(f).forEach((p) => {
          u.style[p] = f[p];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var w, b, y;
        (w = e.current) != null && w.contains(i) && ((b = e.current) == null || b.removeChild(i));
        const {
          portals: p,
          clonedElement: x
        } = k(n);
        return i = x, c(p), i.style.display = "contents", g(), (y = e.current) == null || y.appendChild(i), p.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", g(), (_ = e.current) == null || _.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, r, l, o]), m.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...s);
});
function ke(n) {
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
function M(n) {
  return X(() => ke(n), [n]);
}
const Le = Se(({
  slots: n,
  afterOpenChange: t,
  getPopupContainer: r,
  children: l,
  ...o
}) => {
  const e = M(t), s = M(r);
  return /* @__PURE__ */ E.jsx(E.Fragment, {
    children: /* @__PURE__ */ E.jsx($, {
      ...o,
      afterOpenChange: e,
      getPopupContainer: s,
      title: n.title ? /* @__PURE__ */ E.jsx(Pe, {
        slot: n.title
      }) : o.title,
      children: l
    })
  });
});
export {
  Le as Tooltip,
  Le as default
};
