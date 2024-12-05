import { g as V, w as v } from "./Index-Bm7zRKAJ.js";
const h = window.ms_globals.React, Y = window.ms_globals.React.forwardRef, Q = window.ms_globals.React.useRef, X = window.ms_globals.React.useState, z = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, k = window.ms_globals.ReactDOM.createPortal, $ = window.ms_globals.antd.message;
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
var ee = h, te = Symbol.for("react.element"), ne = Symbol.for("react.fragment"), re = Object.prototype.hasOwnProperty, oe = ee.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function H(n, t, s) {
  var l, r = {}, e = null, o = null;
  s !== void 0 && (e = "" + s), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (l in t) re.call(t, l) && !se.hasOwnProperty(l) && (r[l] = t[l]);
  if (n && n.defaultProps) for (l in t = n.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: te,
    type: n,
    key: e,
    ref: o,
    props: r,
    _owner: oe.current
  };
}
R.Fragment = ne;
R.jsx = H;
R.jsxs = H;
G.exports = R;
var w = G.exports;
const {
  SvelteComponent: le,
  assign: L,
  binding_callbacks: T,
  check_outros: ie,
  children: U,
  claim_element: K,
  claim_space: ce,
  component_subscribe: j,
  compute_slots: ae,
  create_slot: ue,
  detach: g,
  element: q,
  empty: A,
  exclude_internal_props: N,
  get_all_dirty_from_scope: de,
  get_slot_changes: fe,
  group_outros: _e,
  init: pe,
  insert_hydration: C,
  safe_not_equal: me,
  set_custom_element_data: B,
  space: he,
  transition_in: x,
  transition_out: O,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: ye,
  onDestroy: Ee,
  setContext: be
} = window.__gradio__svelte__internal;
function F(n) {
  let t, s;
  const l = (
    /*#slots*/
    n[7].default
  ), r = ue(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      t = q("svelte-slot"), r && r.c(), this.h();
    },
    l(e) {
      t = K(e, "SVELTE-SLOT", {
        class: !0
      });
      var o = U(t);
      r && r.l(o), o.forEach(g), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      C(e, t, o), r && r.m(t, null), n[9](t), s = !0;
    },
    p(e, o) {
      r && r.p && (!s || o & /*$$scope*/
      64) && ge(
        r,
        l,
        e,
        /*$$scope*/
        e[6],
        s ? fe(
          l,
          /*$$scope*/
          e[6],
          o,
          null
        ) : de(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      s || (x(r, e), s = !0);
    },
    o(e) {
      O(r, e), s = !1;
    },
    d(e) {
      e && g(t), r && r.d(e), n[9](null);
    }
  };
}
function ve(n) {
  let t, s, l, r, e = (
    /*$$slots*/
    n[4].default && F(n)
  );
  return {
    c() {
      t = q("react-portal-target"), s = he(), e && e.c(), l = A(), this.h();
    },
    l(o) {
      t = K(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), U(t).forEach(g), s = ce(o), e && e.l(o), l = A(), this.h();
    },
    h() {
      B(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      C(o, t, c), n[8](t), C(o, s, c), e && e.m(o, c), C(o, l, c), r = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && x(e, 1)) : (e = F(o), e.c(), x(e, 1), e.m(l.parentNode, l)) : e && (_e(), O(e, 1, 1, () => {
        e = null;
      }), ie());
    },
    i(o) {
      r || (x(e), r = !0);
    },
    o(o) {
      O(e), r = !1;
    },
    d(o) {
      o && (g(t), g(s), g(l)), n[8](null), e && e.d(o);
    }
  };
}
function M(n) {
  const {
    svelteInit: t,
    ...s
  } = n;
  return s;
}
function Ce(n, t, s) {
  let l, r, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const c = ae(e);
  let {
    svelteInit: i
  } = t;
  const p = v(M(t)), d = v();
  j(n, d, (a) => s(0, l = a));
  const m = v();
  j(n, m, (a) => s(1, r = a));
  const u = [], f = ye("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: S,
    subSlotIndex: y
  } = V() || {}, E = i({
    parent: f,
    props: p,
    target: d,
    slot: m,
    slotKey: _,
    slotIndex: S,
    subSlotIndex: y,
    onDestroy(a) {
      u.push(a);
    }
  });
  be("$$ms-gr-react-wrapper", E), we(() => {
    p.set(M(t));
  }), Ee(() => {
    u.forEach((a) => a());
  });
  function b(a) {
    T[a ? "unshift" : "push"](() => {
      l = a, d.set(l);
    });
  }
  function J(a) {
    T[a ? "unshift" : "push"](() => {
      r = a, m.set(r);
    });
  }
  return n.$$set = (a) => {
    s(17, t = L(L({}, t), N(a))), "svelteInit" in a && s(5, i = a.svelteInit), "$$scope" in a && s(6, o = a.$$scope);
  }, t = N(t), [l, r, d, m, c, i, o, e, b, J];
}
class xe extends le {
  constructor(t) {
    super(), pe(this, t, Ce, ve, me, {
      svelteInit: 5
    });
  }
}
const W = window.ms_globals.rerender, I = window.ms_globals.tree;
function Re(n) {
  function t(s) {
    const l = v(), r = new xe({
      ...s,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
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
          return c.nodes = [...c.nodes, o], W({
            createPortal: k,
            node: I
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== l), W({
              createPortal: k,
              node: I
            });
          }), o;
        },
        ...s.props
      }
    });
    return l.set(r), r;
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
    const l = n[s];
    return typeof l == "number" && !Se.includes(s) ? t[s] = l + "px" : t[s] = l, t;
  }, {}) : {};
}
function P(n) {
  const t = [], s = n.cloneNode(!1);
  if (n._reactElement)
    return t.push(k(h.cloneElement(n._reactElement, {
      ...n._reactElement.props,
      children: h.Children.toArray(n._reactElement.props.children).map((r) => {
        if (h.isValidElement(r) && r.props.__slot__) {
          const {
            portals: e,
            clonedElement: o
          } = P(r.props.el);
          return h.cloneElement(r, {
            ...r.props,
            el: o,
            children: [...h.Children.toArray(r.props.children), ...e]
          });
        }
        return null;
      })
    }), s)), {
      clonedElement: s,
      portals: t
    };
  Object.keys(n.getEventListeners()).forEach((r) => {
    n.getEventListeners(r).forEach(({
      listener: o,
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, o, i);
    });
  });
  const l = Array.from(n.childNodes);
  for (let r = 0; r < l.length; r++) {
    const e = l[r];
    if (e.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = P(e);
      t.push(...c), s.appendChild(o);
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
const D = Y(({
  slot: n,
  clone: t,
  className: s,
  style: l
}, r) => {
  const e = Q(), [o, c] = X([]);
  return z(() => {
    var m;
    if (!e.current || !n)
      return;
    let i = n;
    function p() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ke(r, u), s && u.classList.add(...s.split(" ")), l) {
        const f = Ie(l);
        Object.keys(f).forEach((_) => {
          u.style[_] = f[_];
        });
      }
    }
    let d = null;
    if (t && window.MutationObserver) {
      let u = function() {
        var y, E, b;
        (y = e.current) != null && y.contains(i) && ((E = e.current) == null || E.removeChild(i));
        const {
          portals: _,
          clonedElement: S
        } = P(n);
        return i = S, c(_), i.style.display = "contents", p(), (b = e.current) == null || b.appendChild(i), _.length > 0;
      };
      u() || (d = new window.MutationObserver(() => {
        u() && (d == null || d.disconnect());
      }), d.observe(n, {
        attributes: !0,
        childList: !0,
        subtree: !0
      }));
    } else
      i.style.display = "contents", p(), (m = e.current) == null || m.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = e.current) != null && u.contains(i) && ((f = e.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [n, t, s, l, r]), h.createElement("react-child", {
    ref: e,
    style: {
      display: "contents"
    }
  }, ...o);
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
  return Z(() => Oe(n), [n]);
}
const Te = Re(({
  slots: n,
  children: t,
  visible: s,
  onVisible: l,
  onClose: r,
  getContainer: e,
  ...o
}) => {
  const c = Pe(e), [i, p] = $.useMessage({
    ...o,
    getContainer: c
  });
  return z(() => (s ? i.open({
    ...o,
    icon: n.icon ? /* @__PURE__ */ w.jsx(D, {
      slot: n.icon
    }) : o.icon,
    content: n.content ? /* @__PURE__ */ w.jsx(D, {
      slot: n.content
    }) : o.content,
    onClose(...d) {
      l == null || l(!1), r == null || r(...d);
    }
  }) : i.destroy(o.key), () => {
    i.destroy(o.key);
  }), [s]), /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), p]
  });
});
export {
  Te as Message,
  Te as default
};
